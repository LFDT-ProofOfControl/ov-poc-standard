"""Prepared prerequisite harness. Execution requires a separately accepted run plan."""
import hashlib
import json
from pathlib import Path
import shutil

CONTROL_FILES = ["control_probe.py","common.py","merkle.py","assessor.py",
                 "ED25519-VECTOR.json","MERKLE-VECTOR.json"]
EXPECTED = {
    "ed25519_positive","ed25519_invalid_signature_rejected",
    "merkle_inclusion_positive","merkle_invalid_inclusion_rejected",
    "consistency_3_7_positive","consistency_3_7_invalid_node_rejected",
    "consistency_3_5_positive","consistency_3_5_invalid_node_rejected",
    "consistency_5_7_positive","consistency_5_7_invalid_node_rejected",
    "permitted_Q2_component","oracle_read_denied","case_label_read_denied",
    "generator_knowledge_read_denied","symlink_escape_read_denied",
    "write_denied","network_denied","fork_denied","inherited_api_environment_absent"
}

def run_prerequisites(root, venv, output):
    # Imports and calls occur only during a future separately authorized execution.
    from supervisor import acquisition_for, launch, MAX_OUTPUT
    from common import strict_load, encode
    from runtime_preflight import validate_disjoint, validate_runtime_read_roots
    import sys
    root, venv, output = validate_disjoint(root,venv,output)
    validate_runtime_read_roots(root,output,
        [sys.base_prefix,"/System","/usr/lib","/private/var/db/dyld"])
    control = output/"prerequisites"
    control.mkdir()
    stage = control/"restricted"
    stage.mkdir()
    canaries = control/"outside-stage"
    canaries.mkdir()
    (canaries/"case-label.txt").write_text("P0: public isolation-control label\n")
    (canaries/"generator-knowledge.txt").write_text("Public synthetic canary; no signing key or generator data\n")
    oracle = root/"oracle/EXPECTED-OUTCOMES.json"
    if not oracle.is_file():
        raise ValueError("Missing oracle denial target")
    for name in CONTROL_FILES:
        shutil.copyfile(root/name,stage/name)
    raw = (root/"fixtures/P0/supplied.json").read_bytes()
    (stage/"supplied.json").write_bytes(raw)
    acquisition = acquisition_for(strict_load(raw))
    (stage/"acquisition.json").write_bytes(encode(acquisition))
    (stage/"escape").symlink_to(canaries/"generator-knowledge.txt")
    targets = {"oracle":str(oracle),"case_label":str(canaries/"case-label.txt"),
               "generator_knowledge":str(canaries/"generator-knowledge.txt"),
               "symlink_escape":str(stage/"escape")}
    (stage/"control-paths.json").write_text(json.dumps(targets,sort_keys=True)+"\n")
    inventory = {}
    for p in stage.iterdir():
        inventory[p.name] = ({"symlink_target":str(p.readlink())} if p.is_symlink()
                             else {"sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
    (control/"stage-inventory.json").write_text(json.dumps(inventory,indent=2)+"\n")
    meta = launch(stage,venv,"control_probe.py",control/"capture")
    stdout = (control/"capture/stdout.jsonl").read_bytes()
    stderr = (control/"capture/stderr.txt").read_bytes()
    if meta["returncode"] != 0 or meta["timed_out"] or stderr or not stdout or len(stdout)>MAX_OUTPUT:
        raise ValueError("Fresh primitive/isolation prerequisite failed; capture retained")
    record = json.loads(stdout)
    if set(record["checks"]) != EXPECTED or not all(value is True for value in record["checks"].values()):
        raise ValueError("Missing or failed prerequisite")
    if (record["full_appraisals"],record["grade_calls"],record["signing_keys_generated"]) != (0,0,0):
        raise ValueError("Prerequisite scope mismatch")
    events = record["Q2_component_events"]
    if ([e["kind"] for e in events] != ["enter","complete","enter","complete"] or
        [e["name"] for e in events] != ["auth_S2","auth_S2","inclusion","inclusion"]):
        raise ValueError("Incomplete permitted-component trace")
    result = {"state":"READY","checks":record["checks"],
              "capture_sha256":hashlib.sha256(stdout).hexdigest(),
              "profile_sha256":meta["profile_sha256"],"component_invocations":1,
              "full_appraisals":0,"grade_calls":0,
              "scope":"Fresh local control only; trusted operator/host, no independent witness or hardware claim"}
    (control/"RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    return result
