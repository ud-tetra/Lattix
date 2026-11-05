#!/usr/bin/env python3
"""Validate Discovery record structure, references, and captured byte integrity."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from discovery import EVIDENCE, SESSION_STATUS, digest, identifier

REQUIRED = {
    "session": {"session_id", "runtime", "task", "goal", "base_revision", "status", "claims", "checks", "finding", "next_action"},
    "task": {"task_id", "goal", "owned_paths", "dependencies", "status"},
    "candidate": {"candidate_id", "session_id", "question", "status", "evidence", "assumptions", "physical_mapping", "target_exposure", "fitted_choices", "sources", "baseline", "result", "next_discriminant"},
    "run": {"session_id", "run_id", "evidence", "summary", "command", "source", "inputs", "files"},
    "source_import": {"sources"},
}


def safe_file(folder, relative):
    relative = Path(relative)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Captured path escapes its manifest directory")
    path = folder / relative
    if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(folder.resolve()):
        raise ValueError("Missing, symlinked, or escaping captured file")
    return path


def validate(root):
    root = Path(root).resolve()
    errors = []
    records = 0
    patterns = ("sessions/*/record.json", "tasks/*.json", "candidates/*/candidate.json",
                "artifacts/*/*/manifest.json", "sources/imports/*/provenance.json")
    for pattern in patterns:
        for path in sorted(root.glob(pattern)):
            try:
                obj = json.loads(path.read_text(encoding="utf-8"))
                kind = obj.get("record_type")
                version = obj.get("schema_version")
                if kind not in REQUIRED or version not in ({1, 2} if kind == "run" else {1}):
                    raise ValueError("Unknown record type or schema version")
                missing = REQUIRED[kind] - obj.keys()
                if missing:
                    raise ValueError("Missing fields: " + ", ".join(sorted(missing)))
                if kind == "session":
                    identifier(obj["session_id"])
                    if path.parent.name != obj["session_id"] or obj["status"] not in SESSION_STATUS:
                        raise ValueError("Session path or status mismatch")
                    if not isinstance(obj["claims"], dict) or not isinstance(obj["checks"], list):
                        raise ValueError("Invalid claims/checks fields")
                if kind in {"candidate", "run"}:
                    session = identifier(obj["session_id"])
                    if not (root / "sessions" / session / "record.json").is_file():
                        raise ValueError("Referenced session does not exist")
                if kind == "task":
                    if path.stem != identifier(obj["task_id"]):
                        raise ValueError("Task ID/path mismatch")
                    if obj["status"] not in {"planned", "active", "complete", "parked", "abandoned"}:
                        raise ValueError("Invalid task status")
                    for owned in obj["owned_paths"]:
                        if not isinstance(owned, str) or not owned or Path(owned).is_absolute() or ".." in Path(owned).parts:
                            raise ValueError("Invalid owned path")
                    for dependency in obj["dependencies"]:
                        if not (root / "tasks" / f"{identifier(dependency)}.json").is_file():
                            raise ValueError("Unknown task dependency")
                if kind == "candidate":
                    if path.parent.name != identifier(obj["candidate_id"]):
                        raise ValueError("Candidate ID/path mismatch")
                    if obj["status"] not in {"HYPOTHESIS", "ACTIVE", "PARKED", "FAILED", "EXPORT_CANDIDATE"}:
                        raise ValueError("Invalid candidate workflow status")
                    if not obj["evidence"] or not set(obj["evidence"]) <= EVIDENCE:
                        raise ValueError("Invalid evidence labels")
                if kind == "run":
                    if obj["evidence"] not in EVIDENCE or not obj["files"]:
                        raise ValueError("Invalid evidence or empty outputs")
                    if path.parent.name != identifier(obj["run_id"]) or path.parent.parent.name != obj["session_id"]:
                        raise ValueError("Run path mismatch")
                    if not isinstance(obj["source"].get("dirty"), bool) or not obj["source"].get("revision"):
                        raise ValueError("Invalid source revision/dirty state")
                    if not isinstance(obj["inputs"], list):
                        raise ValueError("Run inputs must be an array")
                    input_names = set()
                    input_ids = set()
                    input_files = set()
                    for item in obj["inputs"]:
                        if not isinstance(item, dict) or not isinstance(item.get("name"), str) or not item["name"]:
                            raise ValueError("Invalid input name/metadata")
                        if not isinstance(item.get("sha256"), str) or not re.fullmatch("[0-9a-f]{64}", item["sha256"]):
                            raise ValueError("Invalid input SHA-256")
                        if type(item.get("size_bytes")) is not int or item["size_bytes"] < 0:
                            raise ValueError("Invalid input size")
                        if version == 1:
                            if item["name"] in input_names:
                                raise ValueError("Ambiguous legacy input names; recapture with schema version 2")
                            input_names.add(item["name"])
                            continue
                        input_id = identifier(item["input_id"])
                        if input_id in input_ids:
                            raise ValueError("Duplicate input ID")
                        input_ids.add(input_id)
                        if not isinstance(item["path"], str) or not item["path"].startswith("inputs/"):
                            raise ValueError("Captured input path must be inside inputs/")
                        target = safe_file(path.parent, item["path"])
                        if target in input_files:
                            raise ValueError("Duplicate captured input path")
                        input_files.add(target)
                        if digest(target) != item["sha256"] or target.stat().st_size != item["size_bytes"]:
                            raise ValueError("Captured input digest/size mismatch: " + item["path"])
                        if item["source_location"] == "repository":
                            source = item["source_path"]
                            if not isinstance(source, str) or not source or Path(source).is_absolute() or ".." in Path(source).parts:
                                raise ValueError("Invalid repository input source path")
                        elif item["source_location"] != "external" or item["source_path"] is not None:
                            raise ValueError("Invalid external input source metadata")
                    if version == 2:
                        actual_inputs = {item for item in (path.parent / "inputs").rglob("*") if item.is_file() or item.is_symlink()}
                        if actual_inputs != input_files:
                            raise ValueError("Unmanifested or missing captured input")
                    entries = obj["files"]
                elif kind == "source_import":
                    entries = obj["sources"]
                else:
                    entries = []
                listed = set()
                for entry in entries:
                    target = safe_file(path.parent, entry["path"])
                    if target in listed:
                        raise ValueError("Duplicate manifest file")
                    listed.add(target)
                    if not re.fullmatch("[0-9a-f]{64}", entry["sha256"]) or digest(target) != entry["sha256"]:
                        raise ValueError("SHA-256 mismatch: " + entry["path"])
                    if target.stat().st_size != entry["size_bytes"]:
                        raise ValueError("Size mismatch: " + entry["path"])
                if kind == "run":
                    actual = set((path.parent / "files").rglob("*"))
                    actual = {item for item in actual if item.is_file() or item.is_symlink()}
                    if actual != listed:
                        raise ValueError("Unmanifested or missing output file")
                records += 1
            except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
                errors.append(f"{path.relative_to(root)}: {error}")
    for folder in (root / "artifacts").glob("*/*"):
        if folder.is_dir() and not (folder / "manifest.json").is_file():
            errors.append(f"{folder.relative_to(root)}: missing finalized run manifest")
    # Local Markdown links should resolve; URLs and fragment-only links are external.
    for path in root.rglob("*.md"):
        if ".git" in path.parts or path.relative_to(root).parts[0] == "artifacts" or path.is_relative_to(root / "sources" / "imports"):
            continue
        for destination in re.findall(r"\]\(([^\s)]+)\)", path.read_text(encoding="utf-8")):
            destination = destination.split("#", 1)[0]
            if destination and ":" not in destination and not (path.parent / destination).exists():
                errors.append(f"{path.relative_to(root)}: unresolved local link {destination}")
    return records, errors


def main():
    root = Path(__file__).resolve().parents[1]
    records, errors = validate(root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"PASS: {records} records; manifest digests and local documentation links valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
