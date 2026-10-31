#!/usr/bin/env python3
"""Artifact-link checker. Never launches code or creates measurements."""
import argparse
import base64
import calendar
import datetime
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

PLAN_SCHEMA = "bjorn-implementation/orchestration-plan/v1"
PRODUCER_SCHEMA = "bjorn-implementation/producer-receipt/v1"
MANIFEST_SCHEMA = "bjorn-implementation/orchestration-manifest/v1"
MAX_BYTES = 16777216


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key")
            result[key] = value
        return result

    def reject(value):
        raise ValueError("non-finite JSON constant")

    def finite_float(value):
        need(len(value) <= 128, "JSON float token exceeds 128 characters")
        number = float(value)
        need(math.isfinite(number), "non-finite JSON float")
        return number

    doc = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                     parse_constant=reject, parse_float=finite_float)
    need(isinstance(doc, dict), "JSON document must be one object")
    return doc


def safe_path(path):
    path = Path(path)
    need(path.is_absolute() and ".." not in path.parts, "absolute non-traversing path required")
    for part in [path, *path.parents]:
        need(not part.is_symlink(), "symlink rejected")
    return path


def read_bytes(path):
    path = safe_path(path)
    with os.fdopen(os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)), "rb") as handle:
        info = os.fstat(handle.fileno())
        need(stat.S_ISREG(info.st_mode) and info.st_size <= MAX_BYTES, "invalid file type/size")
        raw = handle.read(MAX_BYTES + 1)
    need(len(raw) <= MAX_BYTES, "file exceeds limit")
    return raw


def pinned_document(reference):
    need(set(reference) == {"path", "sha256"}, "document reference needs path and SHA-256")
    raw = read_bytes(reference["path"])
    need(digest(raw)["sha256"] == reference["sha256"], "document pin mismatch")
    return strict_json(raw), raw


def check_digest(block, raw, label):
    need(isinstance(block, dict) and type(block.get("bytes")) is int, label + " invalid digest")
    actual = digest(raw)
    need(block.get("bytes") == actual["bytes"] and block.get("sha256") == actual["sha256"],
         label + " digest mismatch")


def identifier(value):
    need(isinstance(value, str) and re.fullmatch(r"[a-f0-9]{32}", value), "invalid run ID")
    return value


def instant(value):
    need(isinstance(value, str), "timestamp must be a UTC string")
    match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,9}))?Z", value)
    need(match is not None, "timestamp must be an actual UTC instant ending in Z")
    parts = [int(x) for x in match.groups()[:6]]
    date = datetime.datetime(*parts, tzinfo=datetime.timezone.utc)
    return calendar.timegm(date.utctimetuple()) * 1000000000 + int((match.group(7) or "0").ljust(9, "0"))


def check_named_code(pins, paths, label):
    need(isinstance(pins, list) and pins and isinstance(paths, dict), label + " files required")
    names = []
    for pin in pins:
        name = pin.get("path")
        need(isinstance(name, str) and name and not PurePosixPath(name).is_absolute()
             and str(PurePosixPath(name)) == name and ".." not in PurePosixPath(name).parts,
             label + " invalid logical path")
        names.append(name)
    need(len(names) == len(set(x.casefold() for x in names)) and set(names) == set(paths),
         label + " path inventory mismatch")
    for pin in pins:
        check_digest(pin, read_bytes(paths[pin["path"]]), label + ":" + pin["path"])


def check_orchestration(spec):
    need(set(spec) == {"plan", "producer_receipt", "assessor_receipt", "input", "outcome",
                       "measured", "expected", "code"}, "unexpected binding spec fields")
    plan, plan_raw = pinned_document(spec["plan"])
    need(plan.get("schema") == PLAN_SCHEMA and plan.get("phase") == "pre_execution",
         "pre-execution plan required")
    orchestration_id = identifier(plan.get("run_id"))
    assigned = instant(plan.get("assigned_at"))
    mode = plan.get("mode")
    need(mode in {"executed", "fixture_only"}, "unsupported comparison mode")
    ids = plan["component_run_ids"]
    need(set(ids) == {"producer", "assessor", "comparator"}, "component IDs incomplete")
    identifier(ids["assessor"]); identifier(ids["comparator"])
    if mode == "executed":
        identifier(ids["producer"])
    else:
        need(ids["producer"] is None, "fixture-only producer ID must be null")
    all_ids = [orchestration_id] + [v for v in ids.values() if v is not None]
    need(len(all_ids) == len(set(all_ids)), "orchestration/component IDs must be distinct")
    pins, code = plan["pins"], spec["code"]
    need(set(pins) == {"adapter", "reference_code", "assessor_code", "launcher", "expected", "comparator"},
         "plan pins incomplete")
    need(set(code) == {"adapter", "reference_code", "assessor_code", "launcher", "comparator"},
         "actual code paths incomplete")
    expected_raw = read_bytes(spec["expected"])
    strict_json(expected_raw)
    check_digest(pins["expected"], expected_raw, "frozen expected")
    need(isinstance(pins["comparator"].get("version"), str) and pins["comparator"]["version"],
         "comparator version required")
    check_digest(pins["comparator"], read_bytes(code["comparator"]), "comparator code")
    check_digest(pins["launcher"], read_bytes(code["launcher"]), "launcher code")
    check_named_code(pins["assessor_code"], code["assessor_code"], "assessor code")
    input_raw, outcome_raw = read_bytes(spec["input"]), read_bytes(spec["outcome"])
    strict_json(input_raw); strict_json(outcome_raw)
    assessor, assessor_raw = pinned_document(spec["assessor_receipt"])
    need(type(assessor.get("schema_version")) is int and assessor["schema_version"] == 1
         and assessor.get("profile") == "s3-bjorn-isolated-python-v1"
         and assessor.get("module") == "assessor", "isolated assessor receipt required; probes rejected")
    need(assessor.get("orchestration") == {"run_id": orchestration_id, "plan": digest(plan_raw)}
         and assessor.get("run_id") == ids["assessor"], "assessor orchestration/component link mismatch")
    need(assessor.get("status") == "completed" and type(assessor.get("attach_exit_code")) is int
         and assessor["attach_exit_code"] == 0 and assessor.get("capture_failure") is None
         and type(assessor.get("start_attempts")) is int and assessor["start_attempts"] == 1,
         "assessor run did not complete once")
    state = assessor["container_after_capture"]["State"]
    need(state.get("Running") is False and type(state.get("ExitCode")) is int and state["ExitCode"] == 0,
         "assessor container did not exit successfully")
    cleanup = assessor.get("cleanup", {}).get("exit_code")
    need(type(cleanup) is int and cleanup == 0, "assessor cleanup unsuccessful")
    assessor_start, assessor_end = instant(state["StartedAt"]), instant(state["FinishedAt"])
    need(assigned <= assessor_start <= assessor_end, "assessor precedes plan or has invalid chronology")
    check_digest(assessor.get("input"), input_raw, "assessor consumed input")
    check_digest(assessor.get("stdout"), outcome_raw, "assessor captured outcome")
    captured = base64.b64decode(assessor["stdout"]["base64"], validate=True)
    need(captured == outcome_raw, "outcome differs from exact captured stdout")
    need(assessor.get("launcher") == pins["launcher"] and assessor.get("program_files") == pins["assessor_code"],
         "assessor executed code pins mismatch")
    producer_digest, measured_digest = None, None
    if mode == "fixture_only":
        need(spec["producer_receipt"] is None and spec["measured"] is None
             and pins["adapter"] is None and pins["reference_code"] is None
             and code["adapter"] is None and code["reference_code"] is None,
             "fixture-only must not include a measurement producer or measurement")
    else:
        need(spec["producer_receipt"] is not None and spec["measured"] is not None, "producer links missing")
        check_digest(pins["adapter"], read_bytes(code["adapter"]), "adapter code")
        reference = pins["reference_code"]
        need(isinstance(reference.get("revision"), str) and re.fullmatch(r"[a-f0-9]{40}", reference["revision"]),
             "reference code revision pin required")
        check_named_code(reference["files"], code["reference_code"], "reference code")
        producer, producer_raw = pinned_document(spec["producer_receipt"])
        need(producer.get("schema") == PRODUCER_SCHEMA and producer.get("phase") == "measurement_producer",
             "actual measurement producer receipt required")
        need(producer.get("orchestration") == {"run_id": orchestration_id, "plan": digest(plan_raw)}
             and producer.get("run_id") == ids["producer"], "producer orchestration/component link mismatch")
        need(producer.get("status") == "completed" and type(producer.get("exit_code")) is int
             and producer["exit_code"] == 0, "producer did not complete")
        need(assigned <= instant(producer["started_at"]) <= instant(producer["finished_at"]) <= assessor_start,
             "producer/plan/assessor chronology mismatch")
        need(producer.get("code") == {"adapter": pins["adapter"], "reference_code": reference},
             "producer code pins mismatch")
        measured_raw = read_bytes(spec["measured"])
        measured = strict_json(measured_raw)
        check_digest(producer["outputs"].get("measured"), measured_raw, "producer measured artifact")
        check_digest(producer["outputs"].get("assessor_input"), input_raw, "producer frozen input")
        need(producer.get("input_frozen_before_assessment") is True, "producer input-freeze record missing")
        need(measured.get("schema") == "bjorn-implementation/measured/v0"
             and measured.get("input_sha256") == digest(input_raw)["sha256"]
             and measured.get("orchestration_run_id") == orchestration_id
             and measured.get("producer_run_id") == ids["producer"], "measurement artifact identity mismatch")
        producer_digest, measured_digest = digest(producer_raw), digest(measured_raw)
    return {
        "schema": MANIFEST_SCHEMA, "status": "ARTIFACT_LINKS_VERIFIED",
        "run_id": orchestration_id, "component_run_ids": ids, "plan": digest(plan_raw),
        "mode": mode, "producer_receipt": producer_digest, "assessor_receipt": digest(assessor_raw),
        "input": digest(input_raw), "outcome": digest(outcome_raw), "measured": measured_digest,
        "measurement_status": "NOT_RUN" if mode == "fixture_only" else "PRODUCER_ARTIFACT_BOUND",
        "pins": pins, "comparison_run_id": ids["comparator"], "comparison_executed": False,
        "checker": digest(Path(__file__).read_bytes()),
        "claims": {"receipts_modified": False, "measurement_created": False,
                   "subject_code_executed": False, "semantic_comparison_performed": False},
        "trust_model": "Trusted local harness record. IDs, digests and timestamps do not prove provenance against a malicious host.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        output = safe_path(args.output)
        need(not output.exists(), "output must be fresh")
        manifest = check_orchestration(strict_json(read_bytes(args.spec)))
        with output.open("x", encoding="utf-8") as handle:
            json.dump(manifest, handle, indent=2, sort_keys=True)
            handle.write("\n")
    except (OSError, ValueError, TypeError, KeyError, AttributeError, RecursionError) as exc:
        print(json.dumps({"schema": MANIFEST_SCHEMA, "status": "ERROR", "error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps({"status": manifest["status"], "manifest": str(output),
                      "sha256": digest(output.read_bytes())["sha256"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
