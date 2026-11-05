"""Structural Lattix profile and benchmark checks, not scientific certification."""
from __future__ import annotations

import json
import re
from pathlib import Path

from lattix import digest, identifier

ROLES = {"maintainer", "researcher", "reviewer", "integrator"}
LANES = {"C12A", "C12B", "C12C"}
MODES = {"CPU_REFERENCE", "WEBGPU_HARDWARE", "ENGINE_ADAPTER", "NOT_RUN"}


def roster(root):
    obj = json.loads((Path(root) / "config/contributors.json").read_text())
    if obj.get("schema_version") != 1 or not isinstance(obj.get("contributors"), list):
        raise ValueError("Invalid contributor registry")
    result = {}
    for user in obj["contributors"]:
        actor = identifier(user["id"])
        if actor in result or not user.get("github") or not user.get("roles"):
            raise ValueError("Duplicate or incomplete contributor")
        if not set(user["roles"]) <= ROLES:
            raise ValueError("Unknown contributor role")
        result[actor] = user
    return result


def resolve_profile(root, actor=None, role="researcher", model="unknown"):
    root = Path(root)
    local = root / "config/runtime.local.json"
    if actor is None and local.exists():
        settings = json.loads(local.read_text())
        actor, role, model = settings["actor"], settings["role"], settings.get("model", "unknown")
    if (root / "config/contributors.json").exists():
        users = roster(root)
        if actor not in users or role not in users[actor]["roles"]:
            raise ValueError("A registered actor and allowed role are required; see docs/MULTI_USER.md")
    elif actor is None:
        # Compatibility with the upstream isolated Store API/test sandboxes only.
        return {"actor": "unconfigured", "role": "researcher", "model": model,
                "identity_verification": "NOT_AUTHENTICATED"}
    if role not in ROLES:
        raise ValueError("Unknown runtime role")
    return {"actor": identifier(actor), "role": role, "model": model or "unknown",
            "identity_verification": "DECLARED_NOT_AUTHENTICATED"}


def required_text(obj, names):
    for name in names:
        if not isinstance(obj.get(name), str) or not obj[name].strip() or obj[name].startswith("REPLACE"):
            raise ValueError("Missing substantive field: " + name)


def repo_file(root, relative):
    if not isinstance(relative, str) or not relative:
        raise ValueError("Missing repository file path")
    p = Path(relative)
    if p.is_absolute() or ".." in p.parts:
        raise ValueError("Repository file path escapes root")
    result = root / p
    if result.is_symlink() or not result.is_file() or not result.resolve().is_relative_to(root.resolve()):
        raise ValueError("Missing or escaping repository file")
    return result


def protocol_check(obj):
    if obj.get("record_type") != "preregistration" or obj.get("schema_version") != 1:
        raise ValueError("Invalid preregistration schema")
    identifier(obj["protocol_id"])
    if obj.get("lane") not in LANES or obj.get("status") not in {"draft", "frozen"}:
        raise ValueError("Invalid protocol lane/status")
    if obj["status"] == "frozen":
        required_text(obj, ("workload", "acceptance_rule", "exclusions", "timing_scope", "repetitions", "target_exposure"))
        if not obj.get("source_refs"):
            raise ValueError("Frozen protocol requires source references")


def receipt_check(root, obj):
    if obj.get("record_type") != "benchmark_receipt" or obj.get("schema_version") != 1:
        raise ValueError("Invalid benchmark receipt schema")
    identifier(obj["receipt_id"])
    session = identifier(obj["session_id"])
    repo_file(root, f"sessions/{session}/record.json")
    if obj.get("lane") not in LANES or obj.get("status") not in {"NOT_RUN", "PASS", "FAIL", "INCONCLUSIVE"}:
        raise ValueError("Invalid benchmark lane/status")
    ex = obj["execution"]
    if ex.get("mode") not in MODES:
        raise ValueError("Invalid execution mode")
    if not isinstance(obj.get("metrics"), list) or not isinstance(obj.get("limitations"), list):
        raise ValueError("Metrics and limitations must be arrays")
    if obj["status"] == "NOT_RUN":
        if ex["mode"] != "NOT_RUN" or obj["metrics"]:
            raise ValueError("NOT_RUN cannot contain measured metrics")
        return
    if ex["mode"] == "NOT_RUN":
        raise ValueError("An executed receipt needs an execution mode")
    required_text(ex, ("source_revision", "device", "software", "timing_method", "synchronization"))
    if not re.fullmatch(r"[0-9a-f]{40}", ex["source_revision"]):
        raise ValueError("Executed receipt requires a full source commit SHA")
    required_text(obj, ("determinism_scope",))
    protocol = obj["protocol"]
    path = repo_file(root, protocol["path"])
    if not path.is_relative_to(root / "benchmarks/preregistrations"):
        raise ValueError("Protocol must be in benchmarks/preregistrations")
    if digest(path) != protocol["sha256"]:
        raise ValueError("Protocol digest mismatch")
    p = json.loads(path.read_text())
    protocol_check(p)
    if p["status"] != "frozen" or p["lane"] != obj["lane"]:
        raise ValueError("Receipt requires a matching frozen protocol lane")
    if not re.fullmatch(r"[0-9a-f]{40}", protocol.get("preregistration_revision", "")):
        raise ValueError("Full preregistration commit SHA required")
    manifest_path = repo_file(root, obj["artifact_manifest"])
    if not manifest_path.is_relative_to(root / "artifacts"):
        raise ValueError("Receipt requires an artifact run manifest")
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("record_type") != "run" or manifest.get("session_id") != session:
        raise ValueError("Artifact manifest session/type mismatch")
    if not obj["metrics"]:
        raise ValueError("Executed receipt requires raw measurements or failure metrics")
    for metric in obj["metrics"]:
        required_text(metric, ("name", "unit"))
        # Strings such as NaN or Infinity are not numeric measurements.
        import math
        value = metric.get("value")
        if type(value) not in {int, float} or not math.isfinite(value):
            raise ValueError("Metric must be a finite numeric value")
    if obj["lane"] == "C12B":
        if not obj.get("quality_gates"):
            raise ValueError("C12B requires explicit quality gates")
        for gate in obj["quality_gates"]:
            required_text(gate, ("name", "rule"))
            if gate.get("status") not in {"PASS", "FAIL", "NOT_RUN"}:
                raise ValueError("Invalid quality gate status")
        if obj["status"] == "PASS" and any(g["status"] != "PASS" for g in obj["quality_gates"]):
            raise ValueError("C12B PASS requires all declared quality gates to pass")
    if obj["lane"] == "C12C":
        if ex["mode"] != "ENGINE_ADAPTER":
            raise ValueError("C12C measurements require an engine adapter")
        transfer = obj.get("transfer") or {}
        required_text(transfer, ("path", "synchronization", "effort_method"))
        for key in ("bytes_per_frame", "copies_per_frame", "implementation_hours"):
            value = transfer.get(key)
            if type(value) not in {int, float} or not math.isfinite(value) or value < 0:
                raise ValueError("C12C requires nonnegative measured " + key)
        if transfer["path"] == "zero-copy":
            if transfer["copies_per_frame"] != 0:
                raise ValueError("Zero-copy conflicts with measured copies")
            repo_file(root, transfer.get("evidence_path"))


def validate_program(root):
    errors = []
    root = Path(root).resolve()
    config = root / "config/contributors.json"
    if config.exists():
        try:
            users = roster(root)
            for path in (root / "sessions").glob("*/record.json"):
                obj = json.loads(path.read_text())
                p = obj.get("profile", {})
                if p.get("actor") not in users or p.get("role") not in users[p["actor"]]["roles"]:
                    raise ValueError("Session profile is not in contributor registry: " + str(path.relative_to(root)))
        except (ValueError, OSError, KeyError, TypeError) as error:
            errors.append("config/contributors.json: " + str(error))
    for directory, check in (("preregistrations", protocol_check), ("receipts", lambda o: receipt_check(root, o))):
        for path in (root / "benchmarks" / directory).rglob("*.json"):
            try:
                obj = json.loads(path.read_text())
                check(obj)
                key = "protocol_id" if directory == "preregistrations" else "receipt_id"
                if path.stem != obj[key]:
                    raise ValueError("Benchmark ID/path mismatch")
            except (ValueError, OSError, KeyError, TypeError, AttributeError) as error:
                errors.append(f"{path.relative_to(root)}: {error}")
    return errors
