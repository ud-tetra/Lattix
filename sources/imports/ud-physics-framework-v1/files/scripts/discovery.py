#!/usr/bin/env python3
"""Dependency-free session records, explicit artifact capture, and task claims."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

EVIDENCE = {"HYPOTHESIS", "ANALOGY", "FIT", "CONDITIONAL", "EXACT", "NUMERICAL", "EMPIRICAL", "FAILED", "OPEN"}
SESSION_STATUS = {"active", "handoff", "complete", "blocked", "abandoned"}


def now():
    return datetime.now(timezone.utc).isoformat()


def identifier(value):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,119}", value):
        raise ValueError("Identifiers use 1–120 letters, digits, underscores, or hyphens.")
    return value


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path, value, exclusive=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x" if exclusive else "w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write("\n")


def git(root, *args, data=None):
    result = subprocess.run(["git", "-C", str(root), *args], input=data, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def source_state(root):
    try:
        return {"revision": git(root, "rev-parse", "HEAD"),
                "dirty": bool(git(root, "status", "--porcelain"))}
    except RuntimeError:
        return {"revision": "UNCOMMITTED_INITIALIZATION", "dirty": True}


def remote_claim(root, task):
    ref = "refs/heads/claims/" + identifier(task)
    rows = git(root, "ls-remote", "--heads", "origin", ref).splitlines()
    return rows[0].split()[0] if rows else None


def claim_payload(root, task, sha):
    ref = "refs/heads/claims/" + identifier(task)
    git(root, "fetch", "--no-write-fetch-head", "origin", ref)
    payload = json.loads(git(root, "show", sha + ":claim.json"))
    if payload.get("task") != task or payload.get("status", "held") not in {"held", "released"}:
        raise ValueError("Invalid live claim metadata")
    return payload


def claim_commit(root, claim, parent=None):
    """Create an audit commit without changing the runtime's work branch."""
    blob = git(root, "hash-object", "-w", "--stdin", data=json.dumps(claim, sort_keys=True))
    tree = git(root, "mktree", data=f"100644 blob {blob}\tclaim.json\n")
    parents = ["-p", parent] if parent else []
    return git(root, "-c", "user.name=UD Discovery coordination", "-c",
               "user.email=discovery@users.noreply.github.com", "commit-tree", tree, *parents,
               data=f"Claim {claim['task']} {claim.get('status', 'held')} for {claim['session']}\n")


def publish_claim(root, claim):
    """Acquire an absent ref or compare-and-swap a released marker."""
    task = identifier(claim["task"])
    ref = "refs/heads/claims/" + task
    previous = remote_claim(root, task)
    if previous and claim_payload(root, task, previous).get("status", "held") != "released":
        raise RuntimeError("Task claim is held; acquisition rejected.")
    claim = dict(claim, status="held", protocol_version=2)
    if previous:
        claim["previous_claim_sha"] = previous
    sha = claim_commit(root, claim, previous)
    git(root, "push", "--porcelain", f"--force-with-lease={ref}:{previous or ''}", "origin", f"{sha}:{ref}")
    return sha


def delete_claim(root, task, expected):
    """Legacy Git-only conditional deletion; normal releases use audit markers."""
    ref = "refs/heads/claims/" + identifier(task)
    if remote_claim(root, task) != expected:
        raise RuntimeError("Live claim differs from this session's recorded claim; release rejected.")
    git(root, "push", "--porcelain", f"--force-with-lease={ref}:{expected}", "origin", f":{ref}")


def release_claim(root, task, expected, session):
    ref = "refs/heads/claims/" + identifier(task)
    if remote_claim(root, task) != expected:
        raise RuntimeError("Live claim changed; release rejected.")
    claim = claim_payload(root, task, expected)
    if claim.get("session") != session or claim.get("status", "held") != "held":
        raise RuntimeError("Release requires the current held claim's owning session.")
    claim.update(status="released", protocol_version=2, released_at=now(), released_from_sha=expected)
    marker = claim_commit(root, claim, expected)
    git(root, "push", "--porcelain", f"--force-with-lease={ref}:{expected}", "origin", f"{marker}:{ref}")
    return marker


class Store:
    def __init__(self, root):
        self.root = Path(root).resolve()

    def session_path(self, session):
        return self.root / "sessions" / identifier(session) / "record.json"

    def session(self, session):
        return json.loads(self.session_path(session).read_text(encoding="utf-8"))

    def bootstrap(self, runtime, task, goal, session=None):
        session = identifier(session or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-") + uuid.uuid4().hex[:12])
        state = source_state(self.root)
        record = {"record_type": "session", "schema_version": 1, "session_id": session,
                  "runtime": runtime, "task": identifier(task), "goal": goal, "created_at": now(),
                  "base_revision": state["revision"], "source_dirty_at_boot": state["dirty"],
                  "status": "active", "claims": {}, "checks": [], "finding": "", "next_action": ""}
        write_json(self.session_path(session), record, exclusive=True)
        (self.session_path(session).parent / "journal.md").write_text(
            f"# Session {session}\n\nBoot attempt: {record['created_at']}\n\nRuntime: {runtime}\n\nTask: {task}\n\nGoal: {goal}\n\nOwnership: UNCLAIMED until remote claim acquisition succeeds.\n", encoding="utf-8")
        return session

    def note(self, session, text):
        self.session(session)
        with (self.session_path(session).parent / "journal.md").open("a", encoding="utf-8") as stream:
            stream.write(f"\n## {now()}\n\n{text}\n")

    def checkpoint(self, session, status, finding, next_action):
        if status not in SESSION_STATUS:
            raise ValueError("Invalid session status")
        record = self.session(session)
        record.update(status=status, finding=finding, next_action=next_action,
                      checkpoint_at=now(), checkpoint_source=source_state(self.root))
        write_json(self.session_path(session), record)
        self.note(session, f"Checkpoint ({status}): {finding}\n\nNext: {next_action}")

    def new_task(self, task, goal, paths, dependencies):
        task = identifier(task)
        for path in paths:
            if Path(path).is_absolute() or ".." in Path(path).parts or not path or path == ".":
                raise ValueError("Owned paths must be nonempty repository-relative paths")
        for dependency in dependencies:
            identifier(dependency)
        write_json(self.root / "tasks" / f"{task}.json", {
            "record_type": "task", "schema_version": 1, "task_id": task, "goal": goal,
            "owned_paths": paths, "dependencies": dependencies, "status": "planned"}, exclusive=True)

    def new_candidate(self, session, candidate, question):
        self.session(session)
        candidate = identifier(candidate)
        write_json(self.root / "candidates" / candidate / "candidate.json", {
            "record_type": "candidate", "schema_version": 1, "candidate_id": candidate,
            "session_id": session, "question": question, "status": "HYPOTHESIS",
            "evidence": ["HYPOTHESIS"], "assumptions": [], "physical_mapping": "OPEN",
            "target_exposure": "NOT_RECORDED", "fitted_choices": [], "sources": [],
            "baseline": "OPEN", "result": "OPEN", "next_discriminant": "OPEN"}, exclusive=True)
        self.note(session, f"Created candidate {candidate}: {question}")

    def capture(self, session, run, evidence, summary, command, inputs, artifacts):
        self.session(session)
        identifier(run)
        if evidence not in EVIDENCE:
            raise ValueError("Invalid evidence label")
        if not artifacts:
            raise ValueError("At least one explicit artifact is required")
        originals = []
        names = set()
        for path in artifacts:
            path = Path(path)
            if path.is_symlink() or not path.is_file():
                raise ValueError("Artifacts must be explicit regular files, not symlinks")
            if path.name in names:
                raise ValueError("Artifact basenames must be unique within a run")
            if path.stat().st_size > 10 * 1024 * 1024:
                raise ValueError("Artifact exceeds 10 MiB; use a separately configured durable destination")
            names.add(path.name)
            originals.append(path)
        input_records = []
        input_sources = []
        for index, path in enumerate(inputs, start=1):
            path = Path(path)
            if path.is_symlink() or not path.is_file():
                raise ValueError("Inputs must be explicit regular files")
            if path.stat().st_size > 10 * 1024 * 1024:
                raise ValueError("Input exceeds 10 MiB; use a separately configured durable destination")
            resolved = path.resolve()
            inside = resolved.is_relative_to(self.root)
            input_records.append({"input_id": f"input-{index:03d}", "name": path.name,
                                  "path": f"inputs/{index:03d}-{path.name}",
                                  "source_location": "repository" if inside else "external",
                                  "source_path": resolved.relative_to(self.root).as_posix() if inside else None})
            input_sources.append(path)
        state = source_state(self.root)
        folder = self.root / "artifacts" / session / run
        folder.parent.mkdir(parents=True, exist_ok=True)
        folder.mkdir()  # exclusive: a finalized run cannot be overwritten
        try:
            (folder / "files").mkdir()
            if input_sources:
                (folder / "inputs").mkdir()
            for path, metadata in zip(input_sources, input_records):
                destination = folder / metadata["path"]
                shutil.copyfile(path, destination)
                metadata.update(sha256=digest(destination), size_bytes=destination.stat().st_size)
            files = []
            for path in originals:
                destination = folder / "files" / path.name
                shutil.copyfile(path, destination)
                files.append({"path": "files/" + path.name, "sha256": digest(destination), "size_bytes": destination.stat().st_size})
            manifest = {"record_type": "run", "schema_version": 2, "session_id": session,
                        "run_id": run, "created_at": now(), "evidence": evidence,
                        "summary": summary, "command": command, "command_execution": "RECORDED_NOT_EXECUTED_BY_CAPTURE",
                        "source": state, "inputs": input_records, "files": files}
            write_json(folder / "manifest.json", manifest, exclusive=True)
        except Exception:
            shutil.rmtree(folder)
            raise
        self.note(session, f"Captured {folder.relative_to(self.root)} ({evidence}): {summary}")
        return folder

    def claim(self, session, task):
        record = self.session(session)
        task = identifier(task)
        if record["task"] != task:
            raise ValueError("Session task and requested claim differ")
        task_record = json.loads((self.root / "tasks" / f"{task}.json").read_text())
        for dependency in task_record["dependencies"]:
            dep = json.loads((self.root / "tasks" / f"{identifier(dependency)}.json").read_text())
            if dep["status"] != "complete":
                raise ValueError(f"Dependency {dependency} is not complete")
        claim = {"record_type": "claim", "schema_version": 1, "task": task, "session": session,
                 "created_at": now(), "base_revision": record["base_revision"],
                 "owned_paths": task_record["owned_paths"]}
        sha = publish_claim(self.root, claim)
        record["claims"][task] = {"ref": "refs/heads/claims/" + task, "sha": sha, "status": "held"}
        write_json(self.session_path(session), record)
        self.note(session, f"Acquired task claim {task} at {sha}")
        return sha

    def release(self, session, task):
        record = self.session(session)
        claim = record["claims"].get(identifier(task))
        if not claim or claim["status"] != "held":
            raise ValueError("No held claim recorded for this session")
        marker = release_claim(self.root, task, claim["sha"], session)
        claim["status"] = "released"
        claim["release_marker_sha"] = marker
        claim["released_at"] = now()
        write_json(self.session_path(session), record)
        self.note(session, f"Released claim {task} with audit marker {marker}; coordination ref retained.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    commands = parser.add_subparsers(dest="action", required=True)
    boot = commands.add_parser("bootstrap")
    boot.add_argument("--session")
    for name in ("runtime", "task", "goal"):
        boot.add_argument("--" + name, required=True)
    task = commands.add_parser("new-task")
    task.add_argument("--id", required=True)
    task.add_argument("--goal", required=True)
    task.add_argument("--path", action="append", required=True)
    task.add_argument("--depends-on", action="append", default=[])
    candidate = commands.add_parser("new-candidate")
    candidate.add_argument("--session", required=True)
    candidate.add_argument("--id", required=True)
    candidate.add_argument("--question", required=True)
    note = commands.add_parser("note")
    note.add_argument("--session", required=True)
    note.add_argument("--text", required=True)
    checkpoint = commands.add_parser("checkpoint")
    checkpoint.add_argument("--session", required=True)
    checkpoint.add_argument("--status", choices=sorted(SESSION_STATUS), required=True)
    checkpoint.add_argument("--finding", required=True)
    checkpoint.add_argument("--next", required=True)
    capture = commands.add_parser("capture")
    for name in ("session", "run", "summary", "command"):
        capture.add_argument("--" + name, required=True)
    capture.add_argument("--evidence", choices=sorted(EVIDENCE), required=True)
    capture.add_argument("--input", action="append", default=[])
    capture.add_argument("--artifact", action="append", required=True)
    for action in ("claim", "release"):
        item = commands.add_parser(action)
        item.add_argument("--session", required=True)
        item.add_argument("--task", required=True)
    args = parser.parse_args(argv)
    store = Store(args.root)
    try:
        if args.action == "bootstrap":
            result = store.bootstrap(args.runtime, args.task, args.goal, args.session)
        elif args.action == "new-task":
            result = store.new_task(args.id, args.goal, args.path, args.depends_on)
        elif args.action == "new-candidate":
            result = store.new_candidate(args.session, args.id, args.question)
        elif args.action == "note":
            result = store.note(args.session, args.text)
        elif args.action == "checkpoint":
            result = store.checkpoint(args.session, args.status, args.finding, args.next)
        elif args.action == "capture":
            result = store.capture(args.session, args.run, args.evidence, args.summary, args.command, args.input, args.artifact)
        else:
            result = getattr(store, args.action)(args.session, args.task)
        print(result if result is not None else "Recorded")
        return 0
    except (OSError, ValueError, RuntimeError, KeyError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
