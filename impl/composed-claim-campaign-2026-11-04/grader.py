"""Separate post-capture grader; never staged for the assessor."""
import json
from pathlib import Path
from common import digest, encode
from supervisor import validate_capture

ORACLE_SHA256="8fb4042fe1747763ef318ecb417e6a39a2f51ead5f3205cf5c2af68087ba7a94"

def _compare(case_id,validated,oracle_path):
    raw=Path(oracle_path).read_bytes()
    if digest(raw)!=ORACLE_SHA256:raise ValueError("changed accepted oracle")
    oracle=json.loads(raw);cases=[x for x in oracle["cases"] if x["id"]==case_id]
    if len(cases)!=1:raise ValueError("unknown case")
    expected=cases[0];result=validated["result"];mismatches=[]
    try:
        raw_capture=b"".join(encode(e)+b"\n" for e in validated["events"])
        checked=validate_capture(raw_capture,b"",0,validated["supplied"],validated["acquisition"])
        if checked["result"]!=result or checked["capture_sha256"]!=validated["capture_sha256"]:
            raise ValueError("graded summary/capture substitution")
    except (ValueError,KeyError,TypeError) as exc:
        mismatches.append("execution admission:"+str(exc))
    for k,v in expected["expected_components"].items():
        if result["components"][k]["outcome"]!=v:mismatches.append("component:"+k)
    for k,v in expected["expected_claims"].items():
        if result["claims"].get(k)!=v:mismatches.append("claim:"+k)
    for k in ("status","supporting_routes"):
        if result["q3_proposition"][k]!=expected["expected_q3_proposition"][k]:
            mismatches.append("q3_proposition:"+k)
    for k in ("state","outcome","reason","enters","completions"):
        if result["q3_derivation"][k]!=expected["expected_q3_derivation"][k]:
            mismatches.append("q3_derivation:"+k)
    completed=[e for e in validated["events"] if e["kind"]=="complete"]
    entered=[e for e in validated["events"] if e["kind"]=="enter"]
    def has(c,n,outcome=None,reason=None):
        return any(e["component"]==c and e["name"]==n and
          (outcome is None or e["outcome"]==outcome) and
          (reason is None or e["reason"]==reason) for e in completed)
    requirements={
      "Q1a":{"auth_R","auth_certificate","auth_collateral","certificate_identity","validity","revocation","authenticated_report_binding","raw_challenge_equality"},
      "Q1b":{"measurement_equality"},
      "Q1c":{"auth_publication","publication_binding","auth_directory","policy_version","authority_lookup","authority_policy"},
      "Q2":{"auth_S2","inclusion"},
      "Q3_direct":{"auth_S1","auth_S2","direct_consistency"},
      "Q4":{"auth_S1","auth_S2","auth_W1_head","auth_W2_head","delivery_W1","delivery_W2","acquisition_W1","acquisition_W2","same_size_W2_S2","edge_S1_W1","edge_W1_W2"},
      "Q5":{"auth_time_receipt","asserted_time_binding"}}
    for component,names in requirements.items():
        if expected["expected_components"][component]=="verified":
            for name in names:
                if not has(component,name,"verified"):mismatches.append("missing verified operation:"+component+":"+name)
    # Non-verified rows still require the available independent successes and
    # the exact intended rejection. Case IDs exist only in this separate grader.
    nonverified={
      "T2-A":{"Q1a":{"raw_challenge_equality":"verified"}},
      "T2-B":{"Q1c":{n:"verified" for n in ("auth_directory","policy_version","authority_lookup","authority_policy")}},
      "T2-C":{"Q1c":{n:"verified" for n in ("auth_publication","publication_binding")}},
      "T3-U":{"Q1c":{n:"verified" for n in ("auth_publication","publication_binding","auth_directory","policy_version","authority_lookup")}},
      "T3-R":{"Q1c":{**{n:"verified" for n in ("auth_publication","publication_binding","auth_directory","policy_version","authority_lookup")},"authority_policy":"failed"}},
      "T3-N":{"Q1b":{"measurement_equality":"failed"}},
      "T5-M":{"Q3_direct":{"auth_S2":"verified"},"Q4":{"auth_S2":"verified"}},
      "N2":{"Q2":{"auth_S2":"verified","inclusion":"failed"}},
      "N3":{"Q3_direct":{"auth_S1":"verified","auth_S2":"verified","direct_consistency":"failed"}},
      "N4":{"Q2":{"auth_S2":"failed"},"Q3_direct":{"auth_S1":"verified","auth_S2":"failed"},
            "Q4":{**{n:"verified" for n in ("auth_S1","auth_W1_head","auth_W2_head","delivery_W1","delivery_W2","acquisition_W1","acquisition_W2")},"auth_S2":"failed"}},
      "N5":{"Q4":{**{n:"verified" for n in ("auth_S1","auth_S2","auth_W1_head","auth_W2_head","delivery_W1","delivery_W2","acquisition_W1","acquisition_W2")},"same_size_W2_S2":"failed"}}}
    for component,required in nonverified.get(case_id,{}).items():
        for name,outcome in required.items():
            if not has(component,name,outcome):mismatches.append("missing intended operation:"+component+":"+name+":"+outcome)
    if expected["expected_q3_derivation"]["state"]=="completed":
        if set(oracle["q3_record_contract"]["route_trace_fields"])-set(result["q3_derivation"]["provenance"]):
            mismatches.append("missing derivation provenance")
    elif result["q3_derivation"].get("mathematical_relation_rejected") is not False:
        mismatches.append("unexecuted relation incorrectly rejected")
    if case_id in ("N2","N3"):
        c,n=("Q2","inclusion") if case_id=="N2" else ("Q3_direct","direct_consistency")
        if not has(c,n,"failed","proof_rejected"):mismatches.append("missing executed invalid proof")
    if case_id=="N4":
        forbidden={"inclusion","direct_consistency","edge_S1_W1","edge_W1_W2","same_size_W2_S2"}
        if any(e["name"] in forbidden for e in entered):mismatches.append("dependent operation entered")
        if not has("Q4","auth_W2_head","verified"):mismatches.append("W2 authenticity lost")
    if case_id in ("T5-M","T5-S"):
        if any(e["name"] in {"direct_consistency","edge_S1_W1","edge_W1_W2","same_size_W2_S2"} for e in entered):
            mismatches.append("missing/skipped operation entered")
    if case_id=="T3-N" and not has("Q1b","measurement_equality","failed","observed_inequality"):
        mismatches.append("missing measured inequality")
    if case_id=="T3-R" and not has("Q1c","authority_policy","failed","policy_rejected"):
        mismatches.append("missing policy rejection")
    if case_id=="N5" and not has("Q4","same_size_W2_S2","failed","authenticated_conflict"):
        mismatches.append("missing authenticated conflict")
    return {"case":case_id,"status":"MATCH" if not mismatches else "MISMATCH",
        "mismatches":mismatches,"oracle_sha256":digest(raw),"capture_sha256":validated["capture_sha256"],
        "scope":"synthetic bounded appraisal only; no actual-environment attestation or Tier"}


def grade_capture(case_id,run_dir,supplied_path,oracle_path):
    from common import strict_load
    run_dir=Path(run_dir)
    pack=strict_load(Path(supplied_path).read_bytes())
    acquisition=json.loads((run_dir/"acquisition.json").read_bytes())
    process=json.loads((run_dir/"capture/process.json").read_bytes())
    validated=validate_capture((run_dir/"capture/stdout.jsonl").read_bytes(),
        (run_dir/"capture/stderr.txt").read_bytes(),process["returncode"],pack,acquisition)
    return _compare(case_id,validated,oracle_path)
