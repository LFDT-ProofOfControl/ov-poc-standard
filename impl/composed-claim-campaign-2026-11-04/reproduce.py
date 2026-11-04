"""Export-only reproduction orchestration; not executed during export preparation."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import sys
import uuid
from runtime_preflight import validate_disjoint, require_new_output, validate_runtime_read_roots, verify_installed_inventory
from datetime import datetime, timezone

ORDER = ["P0","T2-A","T2-B","T2-C","T3-U","T3-R","T3-N","T5-M","T5-S","N2","N3","N4","N5"]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def now():
    return datetime.now(timezone.utc).isoformat()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--venv", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--review-token", required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    venv = Path(args.venv).resolve()
    output = Path(args.output).resolve()
    if not args.review_token:
        raise SystemExit("Nonempty review assertion required")
    root, venv, output = validate_disjoint(root,venv,output)
    require_new_output(args.output)
    validate_runtime_read_roots(root,output,
        [sys.base_prefix,"/System","/usr/lib","/private/var/db/dyld"])
    if Path(sys.prefix).resolve() != venv:
        raise SystemExit("Invoke this script with the selected environment Python")
    runtime = json.loads((root/"RUNTIME.json").read_text())
    if platform.system() != "Darwin" or platform.machine() != "arm64" or platform.mac_ver()[0] != "15.7.9":
        raise SystemExit("Recorded macOS runtime required; no platform fallback")
    if platform.python_version() != "3.14.6" or sha(Path(sys.executable).resolve().read_bytes()) != runtime["executable_sha256"]:
        raise SystemExit("Python version/executable pin mismatch")
    if not Path("/usr/bin/sandbox-exec").is_file():
        raise SystemExit("Required sandbox launcher unavailable")
    inventory = json.loads((root/"INVENTORY.json").read_text())
    repo_root = root.parent.parent
    for item in inventory["files"]:
        p = repo_root/item["path"]
        if p.stat().st_size != item["bytes"] or sha(p.read_bytes()) != item["sha256"]:
            raise SystemExit("Export pin mismatch: "+item["path"])
    for package in runtime["package_pins"]:
        if importlib.metadata.version(package["name"]) != package["version"]:
            raise SystemExit("Dependency version mismatch")
    installed = json.loads((root/"INSTALLED-DEPENDENCIES.json").read_text())
    site = venv/"lib/python3.14/site-packages"
    installed_result = verify_installed_inventory(site,installed["files"],installed["excluded"])
    for case in ORDER:
        if not (root/"fixtures"/case/"supplied.json").is_file():
            raise SystemExit("Missing frozen supplied input")
    # Supervisor and grader are deliberately outside assessor staging.
    sys.path.insert(0, str(root))
    from supervisor import run_one
    from grader import grade_capture
    from prerequisites import run_prerequisites
    output.mkdir()
    ledger = output/"attempt-ledger.jsonl"
    rows = []
    def append(record):
        with ledger.open("ab") as stream:
            stream.write((json.dumps(record,sort_keys=True)+"\n").encode())
            stream.flush()
            os.fsync(stream.fileno())
    append({"event":"start","at":now(),"order":ORDER,"review_token":args.review_token,
            "export_inventory_sha256":sha((root/"INVENTORY.json").read_bytes()),
            "maximum_attempts":13,"maximum_concurrent":1,"retries":0})
    halt = None
    append({"event":"prerequisites_intent","at":now(),
            "installed_inventory":installed_result,"full_appraisals":0,"grade_calls":0})
    try:
        prerequisites = run_prerequisites(root,venv,output)
        if prerequisites["state"] != "READY":
            raise ValueError("Prerequisites not READY")
        append({"event":"prerequisites_finish","at":now(),"state":"READY",
                "capture_sha256":prerequisites["capture_sha256"]})
    except Exception as exc:
        halt = {"phase":"prerequisites","exception_type":type(exc).__name__,"message":str(exc)}
        (output/"prerequisite-failure.json").write_text(json.dumps(halt,indent=2)+"\n")
        append({"event":"prerequisites_finish","at":now(),"state":"NOT_READY","error":halt})
    for position, case in enumerate(ORDER, 1):
        if halt is not None:
            rows.append({"case":case,"state":"NOT_RUN","reason":"earlier prerequisite or attempt incomplete"})
            continue
        run = output/str(uuid.uuid4())
        supplied = root/"fixtures"/case/"supplied.json"
        append({"event":"attempt_intent","at":now(),"case":case,"position":position,
                "run_directory":run.name,"supplied_sha256":sha(supplied.read_bytes())})
        row = {"case":case,"run_directory":run.name,"assessor_attempts":1,"grade_attempts":0}
        try:
            captured = run_one(supplied,run,venv,args.review_token)
            (run/"assessor-result.json").write_text(json.dumps(captured["result"],indent=2)+"\n")
            append({"event":"grade_intent","at":now(),"case":case,
                    "capture_sha256":captured["capture_sha256"]})
            row["grade_attempts"] = 1
            grade = grade_capture(case,run,supplied,root/"oracle/EXPECTED-OUTCOMES.json")
            (run/"grade.json").write_text(json.dumps(grade,indent=2)+"\n")
            row.update({"state":grade["status"],"capture_sha256":captured["capture_sha256"],
                        "mismatches":grade["mismatches"]})
        except Exception as exc:
            halt = {"case":case,"exception_type":type(exc).__name__,"message":str(exc)}
            row.update({"state":"INCOMPLETE","error":halt})
        rows.append(row)
        append({"event":"finish","at":now(),**row})
    result = {"schema":"composed-export-reproduction/1","at":now(),"rows":rows,
              "halt":halt,"retries":0,"historical_result":False}
    (output/"RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    append({"event":"end","at":now(),"halt":halt})
    print(json.dumps({"output":str(output),"states":[row["state"] for row in rows]}))
    return 1 if halt or any(row["state"]!="MATCH" for row in rows) else 0

if __name__ == "__main__":
    raise SystemExit(main())
