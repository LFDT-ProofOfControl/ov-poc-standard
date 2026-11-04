"""Outcome-aware trace admission for the frozen bounded component contract.
No case labels, oracle, key material or primitive re-execution. Captured operations
remain trusted-host evidence; checking them does not attest execution against a
malicious emitter. Every scheduled branch has exact required operations/gates.
"""
from common import OPS, digest

class Component:
    def __init__(self, name, events, objects, scheduled):
        self.name=name
        self.events=[e for e in events if e.get("component")==name]
        self.completed=[e for e in self.events if e["kind"]=="complete"]
        self.records={e["name"]:e for e in self.completed}
        if len(self.records)!=len(self.completed):raise ValueError(name+": duplicate operation")
        self.required=set()
        self.objects=objects
        skips=[e for e in self.events if e["kind"]=="not_requested"]
        if not scheduled:
            if len(self.events)!=1 or len(skips)!=1 or skips[0]["outcome"]!="not assessed" or skips[0]["reason"]!="frozen_plan_not_requested":
                raise ValueError(name+": missing or false skip")
        elif skips:
            raise ValueError(name+": scheduled operation skipped")
        self.scheduled=scheduled

    def need(self, name, computed=None, rejection="check_rejected"):
        self.required.add(name)
        if name not in self.records:raise ValueError(self.name+": missing operation "+name)
        r=self.records[name]
        if r["outcome"] not in ("verified","failed"):raise ValueError("non-completed outcome")
        if r["reason"]!=("verified" if r["outcome"]=="verified" else rejection):
            raise ValueError(self.name+": different rejection "+name)
        if computed is not None and r["outcome"]!=("verified" if computed else "failed"):
            raise ValueError(self.name+": outcome contradicts supplied material "+name)
        return r

    def auth(self, role):
        return self.need("auth_"+role,rejection="signature_or_binding_rejected")

    def gate(self, roles):
        missing=[x for x in roles if x not in self.objects]
        gates=[e for e in self.events if e["kind"]=="gate"]
        if missing:
            if len(gates)!=1 or gates[0].get("missing")!=missing or gates[0].get("outcome")!="unavailable" or gates[0].get("reason")!="missing_material":
                raise ValueError(self.name+": missing gate inconsistent with supplied inventory")
        elif gates:
            raise ValueError(self.name+": fabricated missing gate")
        return bool(missing)

    def finish(self, policy=None):
        if set(self.records)!=self.required:raise ValueError(self.name+": extra/omitted branch operations")
        events=[e for e in self.events if e["kind"]=="policy_unevaluable"]
        if policy is None:
            if events:raise ValueError(self.name+": unexpected policy label")
        elif len(events)!=1 or events[0].get("outcome")!="unevaluable" or events[0].get("reason")!="authority_unevaluable" or events[0].get("matching_entries")!=policy:
            raise ValueError(self.name+": unevaluable policy evidence disagrees with lookup")
        allowed={"enter","complete","gate","not_requested","policy_unevaluable"}
        if any(e["kind"] not in allowed for e in self.events):raise ValueError("unexpected component evidence")
        return sorted(self.required)

def verified(*records):
    return all(r["outcome"]=="verified" for r in records)

def validate_execution(events, supplied, acquisition):
    """Enforce exact branch coverage even when a component did not verify."""
    o,t,plan=supplied["objects"],supplied["trust"],supplied["plan"]
    report=o["R"]["payload"]
    result={}
    for name in (*OPS,"Q6"):
        c=Component(name,events,o,name in plan["operations"] and name!="Q6")
        if not c.scheduled:
            result[name]=c.finish()
            continue
        policy=None
        if name=="Q1a":
            c.need("raw_challenge_equality",report["challenge"]==t["challenge"],"challenge_mismatch")
            missing=c.gate(["certificate","collateral"])
            if not missing:
                cert,coll=o["certificate"]["payload"],o["collateral"]["payload"]
                cs,rs=c.auth("certificate"),c.auth("collateral")
                identity=c.need("certificate_identity",cert["subject_id"]=="A" and cert["public_key"]==t["keys"]["A"],"identity_rejected")
                if verified(cs,rs,identity):
                    auth=c.auth("R")
                    c.need("validity",all(p["not_before"]<=t["appraisal_time"]<p["not_after"] for p in (cert,coll)),"validity_rejected")
                    c.need("revocation",coll["subject_id"]=="A" and "A" not in coll["revoked"],"revoked")
                    c.need("authenticated_report_binding",verified(auth) and report["report_id"]==t["report_id"]
                        and report["claim"]==t["claim"] and report["signer_id"]=="A" and report["challenge"]==t["challenge"],"report_binding_rejected")
        elif name=="Q1b":
            if not c.gate(["M"]):
                c.need("measurement_equality",report["measurement"]==o["M"]["measurement"],"observed_inequality")
        elif name=="Q1c":
            c.gate(["M","publication","directory"])
            if "publication" in o:
                c.auth("publication")
                if "M" in o:
                    c.need("publication_binding",o["publication"]["payload"]=={"claim":t["claim"],"measurement":o["M"]["measurement"]},"publication_binding_rejected")
            if "directory" in o:
                auth=c.auth("directory");d=o["directory"]["payload"]
                version=c.need("policy_version",d["policy_version"]==t["policy_version"],"policy_version_rejected")
                if verified(auth,version):
                    matching=[e for e in d["entries"] if e["key_id"]=="RVP" and e["claim"]==t["claim"]
                              and e["not_before"]<=t["appraisal_time"]<e["not_after"]]
                    lookup=c.need("authority_lookup",True)
                    if lookup["details"]!={"matching_entries":matching}:raise ValueError("authority lookup evidence substitution")
                    if len(matching)!=1:policy=matching
                    else:
                        rule=c.need("authority_policy",matching[0]["disposition"]=="allow","policy_rejected")
                        if rule["details"]!={"matching_rule_digest":digest(matching[0])}:raise ValueError("authority policy rule substitution")
        elif name=="Q2":
            missing=c.gate(["S2","inclusion"])
            auth=c.auth("S2") if "S2" in o else None
            if not missing and verified(auth):c.need("inclusion",rejection="proof_rejected")
        elif name=="Q3_direct":
            missing=c.gate(["S1","S2","direct"])
            auth=[c.auth(role) for role in ("S1","S2") if role in o]
            if not missing and verified(*auth):c.need("direct_consistency",rejection="proof_rejected")
        elif name=="Q4":
            missing=c.gate(["S1","S2","W1_head","W1_delivery","W2_head","W2_delivery","edge_3_5","edge_5_7"])
            prereqs=[c.auth(role) for role in ("S1","S2","W1_head","W2_head") if role in o]
            for w in ("W1","W2"):
                if w+"_head" in o and w+"_delivery" in o:
                    prereqs.append(c.need("delivery_"+w,rejection="delivery_rejected"))
                    observed=[e for e in acquisition["events"] if e["source_id"]==w]
                    if len(observed)!=1:raise ValueError("missing/duplicate local acquisition")
                    ev=observed[0]
                    ok=(ev["run_id"]==acquisition["run_id"] and ev["received_ns"]<=acquisition["cutoff"]
                        and ev["head_digest"]==digest(o[w+"_head"]) and ev["delivery_digest"]==digest(o[w+"_delivery"]))
                    captured=c.need("acquisition_"+w,ok,"acquisition_binding_rejected")
                    if captured["details"]!=ev:raise ValueError("local acquisition evidence substitution")
                    prereqs.append(captured)
            if not missing and verified(*prereqs):
                left,right=o["W2_head"]["payload"],o["S2"]["payload"]
                equality=c.need("same_size_W2_S2",left["size"]==right["size"] and left["root"]==right["root"],"authenticated_conflict")
                if verified(equality):
                    c.need("edge_S1_W1",rejection="proof_rejected")
                    c.need("edge_W1_W2",rejection="proof_rejected")
        elif name=="Q5":
            if not c.gate(["time_receipt"]):
                c.auth("time_receipt")
                receipt=o["time_receipt"]["payload"]
                c.need("asserted_time_binding",receipt["log_id"]==t["log_id"] and receipt["report_digest"]==digest(o["R"]),"time_receipt_binding_rejected")
        result[name]=c.finish(policy)
    return result
