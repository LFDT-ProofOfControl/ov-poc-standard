"""Trusted local supervisor. No campaign entrypoint; run_one requires a review token.
The token is an operator assertion, not an authorization/security boundary.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import uuid
from common import encode, digest, strict_load, OPS
from assessor import aggregate, derive_q3, descriptor
from admission import validate_execution

ASSESSOR_FILES=("common.py","merkle.py","assessor.py","entrypoint.py")
MAX_OUTPUT=4*1024*1024

def acquisition_for(pack):
    run_id=uuid.uuid4().hex
    events=[]
    for w in ("W1","W2"):
        if w+"_head" in pack["objects"] and w+"_delivery" in pack["objects"]:
            head=digest(encode(pack["objects"][w+"_head"]))
            delivery=digest(encode(pack["objects"][w+"_delivery"]))
            events.append({"event_id":run_id+":receive:"+str(len(events)),"run_id":run_id,
                "source_id":w,"head_digest":head,"delivery_digest":delivery,
                "received_ns":time.monotonic_ns()})
    return {"run_id":run_id,"events":events,"cutoff":time.monotonic_ns(),
            "scope":"local supplied view acquisition; no remote witness independence"}

def sandbox_profile(stage,venv):
    stage=Path(stage).resolve();venv=Path(venv).resolve()
    # Dedicated venv must contain only pinned runtime dependencies, never input/oracle.
    runtime=Path(sys.base_prefix).resolve()
    dirs=["/System","/usr/lib","/private/var/db/dyld",str(runtime),str(venv),str(stage)]
    rules=["(version 1)","(deny default)","(allow process-exec)","(allow sysctl-read)",
           "(allow file-read-metadata)"]
    for d in dirs:rules.append("(allow file-read* (subpath "+json.dumps(d)+"))")
    for d in ["/","/dev/null","/dev/urandom","/dev/random"]:
        rules.append("(allow file-read* (literal "+json.dumps(d)+"))")
    return "\n".join(rules)+"\n"

def launch(stage,venv,entrypoint,output_dir,timeout=20):
    """One owned child, no retry; preserve all output before validating it."""
    stage=Path(stage).resolve();output_dir=Path(output_dir);output_dir.mkdir()
    profile=sandbox_profile(stage,venv)
    profile_path=output_dir/"sandbox.sb";profile_path.write_text(profile)
    command=["/usr/bin/sandbox-exec","-f",str(profile_path.resolve()),
             str(Path(venv).resolve()/"bin/python"),"-I","-B",str(stage/entrypoint)]
    timed_out=False
    with (output_dir/"stdout.jsonl").open("wb") as out,(output_dir/"stderr.txt").open("wb") as err:
        child=subprocess.Popen(command,cwd=stage,env={"PATH":"/usr/bin:/bin","LANG":"C"},
            stdin=subprocess.DEVNULL,stdout=out,stderr=err,close_fds=True)
        try:code=child.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out=True;child.kill();code=child.wait()
    meta={"returncode":code,"timed_out":timed_out,"attempts":1,"command":command,
          "profile_sha256":digest(profile.encode()),"stdout_bytes":(output_dir/"stdout.jsonl").stat().st_size,
          "stderr_bytes":(output_dir/"stderr.txt").stat().st_size}
    (output_dir/"process.json").write_text(json.dumps(meta,indent=2)+"\n")
    # The output bound is a validation bound, not OS disk-resource containment.
    return meta

def validate_capture(raw,stderr,code,pack,acquisition):
    if code!=0 or stderr or not raw or len(raw)>MAX_OUTPUT or not raw.endswith(b"\n"):
        raise ValueError("incomplete/failed capture")
    events=[]
    for line in raw.splitlines():
        e=json.loads(line)
        if encode(e)!=line:raise ValueError("noncanonical or duplicate-key event")
        if e.get("seq")!=len(events) or not isinstance(e.get("monotonic_ns"),int):
            raise ValueError("sequence")
        if events and e["monotonic_ns"]<events[-1]["monotonic_ns"]:raise ValueError("clock order")
        events.append(e)
    if events[0]["kind"]!="start" or events[-1]["kind"]!="result":raise ValueError("missing envelope")
    if sum(e["kind"]=="start" for e in events)!=1 or sum(e["kind"]=="result" for e in events)!=1:
        raise ValueError("duplicate envelope")
    start=events[0];r=events[-1]["result"];b=start["binding"]
    if acquisition["cutoff"]>start["monotonic_ns"]:raise ValueError("acquisition after assessment start")
    from assessor import Assessor
    wanted=Assessor(pack,acquisition).binding
    if b!=wanted or r["binding"]!=b or start["plan"]!=pack["plan"]:
        raise ValueError("capture context substitution")
    if start["inventory"]!={k:digest(v) for k,v in pack["objects"].items()}:raise ValueError("input substitution")
    pending={};completed=[];counts={c:{"enters":0,"completions":0} for c in (*OPS,"Q6","Q3_from_Q4")}
    components={c:[] for c in (*OPS,"Q6")}
    for e in events[1:-1]:
        kind=e["kind"];c=e.get("component")
        if kind=="enter":
            if c not in counts or e["operation_id"] in pending or e["operation_id"] in [x["operation_id"] for x in completed]:
                raise ValueError("duplicate/unknown operation")
            if e["binding"]!=b:raise ValueError("cross-context enter")
            pending[e["operation_id"]]=e;counts[c]["enters"]+=1
        elif kind=="complete":
            enter=pending.pop(e["operation_id"],None)
            if enter is None:raise ValueError("completion without entry")
            if any(enter[k]!=e[k] for k in ("component","name","input_digests","binding")):
                raise ValueError("operation binding drift")
            if e["outcome"] not in ("verified","failed"):raise ValueError("completion outcome")
            rec={k:v for k,v in e.items() if k not in ("kind","seq","monotonic_ns")}
            completed.append(rec);counts[c]["completions"]+=1
            if c in components:components[c].append(rec)
        elif kind in ("gate","not_requested","policy_unevaluable"):
            if c not in components:raise ValueError("unknown gate")
            components[c].append(e)
        elif kind=="derivation_blocked":
            if c!="Q3_from_Q4":raise ValueError("wrong derivation")
        else:raise ValueError("error/unknown trace event")
    if pending or counts!=r["coverage"]:raise ValueError("unmatched/misreported operations")
    if set(r["components"])!=set(components):raise ValueError("component inventory")
    for c,parts in components.items():
        scheduled=c in pack["plan"]["operations"]
        if not parts:raise ValueError("missing component evidence")
        if not scheduled:
            if counts[c]["enters"] or len(parts)!=1 or parts[0]["kind"]!="not_requested":
                raise ValueError("unscheduled execution")
        elif any(p.get("kind")=="not_requested" for p in parts):raise ValueError("scheduled skip")
        expected=aggregate(parts)
        if any(r["components"][c][k]!=expected[k] for k in ("outcome","reason")):
            raise ValueError("summary inconsistent with trace")
    execution_admission=validate_execution(events,pack,acquisition)
    d=r["q3_derivation"]
    if d["state"]=="completed":
        heads={k:descriptor(pack["objects"][k]) for k in ("S1","S2","W1_head","W2_head")}
        derived=derive_q3(completed,b,heads)
        links={kind:{k:e[k] for k in ("seq","operation_id","monotonic_ns")}
               for kind in ("enter","completion") for e in events
               if e["kind"]==("complete" if kind=="completion" else kind) and e.get("component")=="Q3_from_Q4"}
        candidates=[x for x in completed if x["component"]=="Q3_from_Q4"]
        if (r["components"]["Q4"]["outcome"]!="verified" or len(candidates)!=1
            or candidates[0]["details"]!=derived or d["provenance"]!={**derived,**links}
            or d["record"]!=candidates[0] or d["enters"]!=1 or d["completions"]!=1):
            raise ValueError("unsupported derived claim")
    elif counts["Q3_from_Q4"]!={"enters":0,"completions":0} or d["enters"] or d["completions"]:
        raise ValueError("blocked derivation executed")
    routes=[]
    if r["components"]["Q3_direct"]["outcome"]=="verified":routes.append("direct")
    if d["state"]=="completed":routes.append("Q4_adjacent_edges")
    if r["q3_proposition"]["supporting_routes"]!=routes or r["q3_proposition"]["status"]!=("supported" if routes else "not established"):
        raise ValueError("unsupported proposition")
    incl=r["components"]["Q2"]["outcome"]=="verified"
    obs=incl and bool(routes) and r["components"]["Q4"]["outcome"]=="verified"
    if r["claims"]["PA-incl"]!=("supported" if incl else "not established") or r["claims"]["PA-obs"]!=("supported" if obs else "not established"):
        raise ValueError("unsupported inclusion/observation claim")
    return {"events":events,"result":r,"capture_sha256":digest(raw),
            "supplied":pack,"acquisition":acquisition,"execution_admission":execution_admission}

def run_one(supplied_path,work_dir,venv,review_token):
    if not review_token:raise PermissionError("Implementation/run-plan review required")
    work_dir=Path(work_dir);work_dir.mkdir()  # Refuse overwrite / retry reuse.
    raw=Path(supplied_path).read_bytes();pack=strict_load(raw);acq=acquisition_for(pack)
    stage=work_dir/"restricted";stage.mkdir()
    here=Path(__file__).resolve().parent
    for f in ASSESSOR_FILES:shutil.copyfile(here/f,stage/f)
    (stage/"supplied.json").write_bytes(raw);(stage/"acquisition.json").write_bytes(encode(acq))
    (work_dir/"acquisition.json").write_bytes(encode(acq))
    (work_dir/"stage-inventory.json").write_bytes(encode({f.name:digest(f.read_bytes()) for f in stage.iterdir()}))
    meta=launch(stage,venv,"entrypoint.py",work_dir/"capture")
    validated=validate_capture((work_dir/"capture/stdout.jsonl").read_bytes(),
            (work_dir/"capture/stderr.txt").read_bytes(),meta["returncode"],pack,acq)
    (work_dir/"validation.json").write_bytes(encode({"capture_sha256":validated["capture_sha256"],
        "review_token":review_token,"state":"CAPTURE_VALIDATED_UNGRADED"}))
    return validated
