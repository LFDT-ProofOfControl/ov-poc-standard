"""Restricted assessor: no builder, oracle, case IDs or private-key interface."""
import copy
import json
import sys
import time
from common import encode,digest,verify,OPS
from merkle import inclusion,consistency

class Trace:
    def __init__(self,binding,emit=None):
        self.binding=copy.deepcopy(binding);self.events=[];self.records=[];self.emit=emit
    def event(self,kind,**data):
        e={"seq":len(self.events),"monotonic_ns":time.monotonic_ns(),"kind":kind,**data}
        self.events.append(copy.deepcopy(e))
        if self.emit:self.emit(e)
        return e
    def op(self,component,name,fn,inputs,reason="check_rejected",details=None):
        op_id=self.binding["run_id"]+":"+str(len(self.events))
        self.event("enter",operation_id=op_id,component=component,name=name,algorithm="slice-v1",
                   input_digests=inputs,binding=self.binding)
        try:
            ok=fn()
            if type(ok) is not bool:raise TypeError("operation must return computed bool")
        except Exception as exc:
            self.event("error",operation_id=op_id,error_type=type(exc).__name__)
            raise
        rec={"operation_id":op_id,"component":component,"name":name,
             "outcome":"verified" if ok else "failed","reason":"verified" if ok else reason,
             "input_digests":list(inputs),"binding":copy.deepcopy(self.binding),
             "details":copy.deepcopy(details() if callable(details) else (details or {}))}
        self.records.append(rec);self.event("complete",**rec)
        return rec
    def gate(self,component,missing):
        rec={"outcome":"unavailable","reason":"missing_material","missing":list(missing)}
        self.event("gate",component=component,**rec);return rec
    def skip(self,component):
        r={"outcome":"not assessed","reason":"frozen_plan_not_requested"}
        self.event("not_requested",component=component,**r);return r

def aggregate(parts):
    for status in ["failed","unavailable","unevaluable","not assessed"]:
        for p in parts:
            if p["outcome"]==status:
                return {"outcome":status,"reason":p["reason"],"subchecks":parts}
    return {"outcome":"verified","reason":"verified","subchecks":parts}

def descriptor(env):
    p=env["payload"]
    return {"artifact_digest":digest(env),"log_id":p["log_id"],"size":p["size"],
            "root":p["root"],"key_id":p["key_id"]}

def derive_q3(records,binding,heads):
    """Require actual completed, exact-bound Q4 support, not its summary label."""
    need=["auth_S1","auth_S2","auth_W1_head","auth_W2_head","delivery_W1","delivery_W2",
          "acquisition_W1","acquisition_W2","same_size_W2_S2","edge_S1_W1","edge_W1_W2"]
    selected=[]
    for name in need:
        candidates=[r for r in records if r["component"]=="Q4" and r["name"]==name]
        if len(candidates)!=1:raise ValueError("missing/duplicate supporting operation")
        r=candidates[0]
        if r["outcome"]!="verified" or r["binding"]!=binding:
            raise ValueError("unverified or cross-context support")
        selected.append(r)
    if len({r["operation_id"] for r in selected})!=len(selected) or any(
        not r["operation_id"].startswith(binding["run_id"]+":") for r in selected):
        raise ValueError("reused/cross-run operation ID")
    by={r["name"]:r for r in selected}
    for role in heads:
        r=by["auth_"+role]
        if r["input_digests"]!=[heads[role]["artifact_digest"]] or r["details"]!=heads[role]:
            raise ValueError("authentication endpoint substitution")
    for name,left,right in [("edge_S1_W1","S1","W1_head"),("edge_W1_W2","W1_head","W2_head"),
                            ("same_size_W2_S2","W2_head","S2")]:
        r=by[name]
        if r["details"].get("left")!=heads[left] or r["details"].get("right")!=heads[right]:
            raise ValueError("broken endpoint join")
        expected_inputs=[heads[left]["artifact_digest"],heads[right]["artifact_digest"]]
        if name!="same_size_W2_S2":expected_inputs.append(r["details"]["proof_digest"])
        if r["input_digests"]!=expected_inputs:raise ValueError("proof/endpoint input substitution")
    if [heads[k]["size"] for k in ("S1","W1_head","W2_head","S2")]!=[3,5,7,7]:
        raise ValueError("unexpected bounded shape")
    if heads["W2_head"]["root"]!=heads["S2"]["root"]:raise ValueError("unequal final roots")
    if any(h["log_id"]!=binding["log_id"] or h["key_id"]!="LO" for h in heads.values()):
        raise ValueError("log/trust identity mismatch")
    if not binding["trust_config_digest"] or binding["tree_algorithm"]!="RFC9162-SHA256":
        raise ValueError("missing algorithm/trust binding")
    if set(binding["observed_view_set"])!={"W1","W2"} or len(binding["acquisition_trace_ids"])!=2:
        raise ValueError("missing obtained set")
    for w in ("W1","W2"):
        a=by["acquisition_"+w]["details"]
        if (a["source_id"]!=w or a["head_digest"]!=heads[w+"_head"]["artifact_digest"]
            or a["run_id"]!=binding["run_id"] or a["received_ns"]>binding["cutoff"]
            or a["event_id"] not in binding["acquisition_trace_ids"]):
            raise ValueError("acquisition/scope reuse")
        if by["delivery_"+w]["input_digests"]!=[a["delivery_digest"],a["head_digest"]]:
            raise ValueError("delivery input substitution")
    return {"derivation_id":binding["run_id"]+":Q3_from_Q4","rule_version":"prefix-transitivity-v1",
            "supporting_operation_ids":[x["operation_id"] for x in selected],
            "input_digests":[digest(x) for x in selected],
            "log_id":binding["log_id"],"trust_config_digest":binding["trust_config_digest"],
            "tree_algorithm":binding["tree_algorithm"],
            "S1_artifact_digest":heads["S1"]["artifact_digest"],
            "S1_size_root":[heads["S1"]["size"],heads["S1"]["root"]],
            "S2_artifact_digest":heads["S2"]["artifact_digest"],
            "S2_size_root":[heads["S2"]["size"],heads["S2"]["root"]],
            "joined_edge_endpoint_digests":[[heads[a]["artifact_digest"],heads[b]["artifact_digest"]]
                for a,b in [("S1","W1_head"),("W1_head","W2_head"),("W2_head","S2")]],
            "report_digest":binding["report_digest"],
            "appraisal_run_challenge":{k:binding[k] for k in ("run_id","report_id","challenge","appraisal_time")},
            "observed_view_set":binding["observed_view_set"],
            "acquisition_trace_ids":binding["acquisition_trace_ids"],"cutoff":binding["cutoff"]}

class Assessor:
    def __init__(self,supplied,acquisition,emit=None):
        self.o=supplied["objects"];self.t=supplied["trust"];self.plan=supplied["plan"];self.acq=acquisition
        self.report_digest=digest(self.o["R"])
        self.binding={"run_id":acquisition["run_id"],"log_id":self.t["log_id"],
          "trust_config_digest":digest(self.t),"tree_algorithm":"RFC9162-SHA256",
          "report_digest":self.report_digest,"report_id":self.t["report_id"],
          "challenge":self.t["challenge"],"appraisal_time":self.t["appraisal_time"],
          "observed_view_set":[e["source_id"] for e in acquisition["events"]],
          "acquisition_trace_ids":[e["event_id"] for e in acquisition["events"]],
          "cutoff":acquisition["cutoff"]}
        self.trace=Trace(self.binding,emit);self.results={}
    def check(self,c,n,fn,roles,reason="check_rejected",details=None):
        return self.trace.op(c,n,fn,[digest(self.o[x]) for x in roles],reason,details)
    def missing(self,c,roles):
        absent=[x for x in roles if x not in self.o]
        return [self.trace.gate(c,absent)] if absent else []
    def auth(self,c,role,key):
        env=self.o[role]
        return self.check(c,"auth_"+role,lambda:verify(env,key,self.t["keys"]) and
            (env["kind"]!="head" or (env["payload"]["log_id"]==self.t["log_id"] and
                                     env["payload"]["key_id"]=="LO")),
            [role],"signature_or_binding_rejected",
            descriptor(env) if env["kind"]=="head" else {})
    def q1a(self):
        c="Q1a";r=self.o["R"]["payload"];a=[self.check(c,"raw_challenge_equality",
            lambda:r["challenge"]==self.t["challenge"],["R"],"challenge_mismatch")]
        missing=self.missing(c,["certificate","collateral"])
        if missing:return aggregate(a+missing)
        cert=self.o["certificate"]["payload"];coll=self.o["collateral"]["payload"]
        sigs=[self.auth(c,"certificate","V"),self.auth(c,"collateral","V")];a+=sigs
        a.append(self.check(c,"certificate_identity",lambda:cert["subject_id"]=="A" and
                            cert["public_key"]==self.t["keys"]["A"],["certificate"],"identity_rejected"))
        if all(x["outcome"]=="verified" for x in sigs) and a[-1]["outcome"]=="verified":
            report_auth=self.auth(c,"R","A");a.append(report_auth)
            a.append(self.check(c,"validity",lambda:all(p["not_before"]<=self.t["appraisal_time"]<p["not_after"]
                 for p in [cert,coll]),["certificate","collateral"],"validity_rejected"))
            a.append(self.check(c,"revocation",lambda:coll["subject_id"]=="A" and "A" not in coll["revoked"],
                                ["collateral"],"revoked"))
            a.append(self.check(c,"authenticated_report_binding",lambda:report_auth["outcome"]=="verified" and r["report_id"]==self.t["report_id"]
                and r["claim"]==self.t["claim"] and r["signer_id"]=="A"
                and r["challenge"]==self.t["challenge"],["R"],"report_binding_rejected"))
        return aggregate(a)
    def q1b(self):
        m=self.missing("Q1b",["M"])
        return aggregate(m or [self.check("Q1b","measurement_equality",lambda:
            self.o["R"]["payload"]["measurement"]==self.o["M"]["measurement"],["R","M"],
            "observed_inequality",{"left":self.o["R"]["payload"]["measurement"],"right":self.o.get("M",{}).get("measurement")})])
    def q1c(self):
        c="Q1c";a=self.missing(c,["M","publication","directory"])
        if "publication" in self.o:
            sig=self.auth(c,"publication","RVP");a.append(sig)
            if "M" in self.o:
                a.append(self.check(c,"publication_binding",lambda:self.o["publication"]["payload"]==
                   {"claim":self.t["claim"],"measurement":self.o["M"]["measurement"]},
                   ["publication","M"],"publication_binding_rejected"))
        if "directory" in self.o:
            sig=self.auth(c,"directory","AR");a.append(sig);p=self.o["directory"]["payload"]
            version=self.check(c,"policy_version",lambda:p["policy_version"]==self.t["policy_version"],
                               ["directory"],"policy_version_rejected");a.append(version)
            if sig["outcome"]==version["outcome"]=="verified":
                applicable=[]
                def lookup():
                    applicable.extend(e for e in p["entries"] if e["key_id"]=="RVP" and e["claim"]==self.t["claim"]
                        and e["not_before"]<=self.t["appraisal_time"]<e["not_after"])
                    return True
                self.check(c,"authority_lookup",lookup,["directory"],details=lambda:{"matching_entries":applicable})
                if len(applicable)!=1:
                    r={"outcome":"unevaluable","reason":"authority_unevaluable",
                       "matching_entries":applicable};self.trace.event("policy_unevaluable",component=c,**r);a.append(r)
                else:a.append(self.check(c,"authority_policy",lambda:applicable[0]["disposition"]=="allow",
                       ["directory"],"policy_rejected",{"matching_rule_digest":digest(applicable[0])}))
        return aggregate(a)
    def q2(self):
        c="Q2";a=self.missing(c,["S2","inclusion"])
        if "S2" in self.o:a.append(self.auth(c,"S2","LO"))
        if any(p["outcome"]!="verified" for p in a):return aggregate(a)
        p=self.o["inclusion"];head=self.o["S2"]["payload"]
        a.append(self.check(c,"inclusion",lambda:p["size"]==head["size"] and inclusion(
          bytes.fromhex(self.report_digest),p["index"],p["size"],[bytes.fromhex(x) for x in p["nodes"]],
          bytes.fromhex(head["root"])),["R","S2","inclusion"],"proof_rejected"))
        return aggregate(a)
    def edge(self,c,name,left,right,proof):
        l,r=descriptor(self.o[left]),descriptor(self.o[right]);p=self.o[proof]
        return self.check(c,name,lambda:p["from_size"]==l["size"] and p["to_size"]==r["size"] and
          consistency(l["size"],r["size"],bytes.fromhex(l["root"]),bytes.fromhex(r["root"]),
                      [bytes.fromhex(x) for x in p["nodes"]]),[left,right,proof],"proof_rejected",
                      {"left":l,"right":r,"proof_digest":digest(p)})
    def q3(self):
        c="Q3_direct";a=self.missing(c,["S1","S2","direct"])
        for role in ("S1","S2"):
            if role in self.o:a.append(self.auth(c,role,"LO"))
        if all(x["outcome"]=="verified" for x in a):a.append(self.edge(c,"direct_consistency","S1","S2","direct"))
        return aggregate(a)
    def q4(self):
        c="Q4";a=self.missing(c,["S1","S2","W1_head","W1_delivery","W2_head","W2_delivery","edge_3_5","edge_5_7"])
        for role in ("S1","S2","W1_head","W2_head"):
            if role in self.o:a.append(self.auth(c,role,"LO"))
        for w in ("W1","W2"):
            if w+"_delivery" in self.o and w+"_head" in self.o:
                env=self.o[w+"_delivery"]
                want={"source_id":w,"challenge":self.t["challenge"],"log_id":self.t["log_id"],
                      "head_digest":digest(self.o[w+"_head"])}
                a.append(self.check(c,"delivery_"+w,lambda env=env,w=w,want=want:
                  verify(env,w,self.t["keys"]) and env["payload"]==want,[w+"_delivery",w+"_head"],
                  "delivery_rejected"))
                events=[e for e in self.acq["events"] if e["source_id"]==w]
                if len(events)!=1:raise ValueError("missing or duplicate trusted acquisition trace")
                ev=events[0]
                a.append(self.check(c,"acquisition_"+w,lambda ev=ev,w=w:
                  ev["run_id"]==self.binding["run_id"] and ev["received_ns"]<=self.acq["cutoff"]
                  and ev["head_digest"]==digest(self.o[w+"_head"])
                  and ev["delivery_digest"]==digest(self.o[w+"_delivery"]),
                  [w+"_head",w+"_delivery"],"acquisition_binding_rejected",ev))
        if any(x["outcome"]!="verified" for x in a):return aggregate(a)
        l,r=descriptor(self.o["W2_head"]),descriptor(self.o["S2"])
        a.append(self.check(c,"same_size_W2_S2",lambda:l["size"]==r["size"] and l["root"]==r["root"],
          ["W2_head","S2"],"authenticated_conflict",{"left":l,"right":r}))
        if a[-1]["outcome"]=="verified":
            a.append(self.edge(c,"edge_S1_W1","S1","W1_head","edge_3_5"))
            a.append(self.edge(c,"edge_W1_W2","W1_head","W2_head","edge_5_7"))
        return aggregate(a)
    def q5(self):
        a=self.missing("Q5",["time_receipt"])
        if not a:
            a.append(self.auth("Q5","time_receipt","LO"))
            p=self.o["time_receipt"]["payload"]
            a.append(self.check("Q5","asserted_time_binding",lambda:p["log_id"]==self.t["log_id"] and
                p["report_digest"]==self.report_digest,["R","time_receipt"],"time_receipt_binding_rejected"))
        return aggregate(a)
    def component(self,c):
        if c=="Q6" or c not in self.plan["operations"]:return self.trace.skip(c)
        return {"Q1a":self.q1a,"Q1b":self.q1b,"Q1c":self.q1c,"Q2":self.q2,"Q3_direct":self.q3,
                "Q4":self.q4,"Q5":self.q5}[c]()
    def derivation(self):
        q4=self.results["Q4"]
        if q4["outcome"]=="verified":
            heads={k:descriptor(self.o[k]) for k in ("S1","S2","W1_head","W2_head")}
            payload={}
            support=[r for r in self.trace.records if r["component"]=="Q4"]
            def execute_derivation():
                payload.update(derive_q3(support,self.binding,heads))
                return True
            r=self.trace.op("Q3_from_Q4","prefix_transitivity",execute_derivation,
                            [digest(x) for x in support],details=lambda:payload)
            return {"state":"completed","outcome":"verified","reason":"verified_adjacent_prefix_relations_and_equal_final_roots",
                    "enters":1,"completions":1,"record":r,"provenance":{**payload,
                       "enter":{k:self.trace.events[-2][k] for k in ("seq","operation_id","monotonic_ns")},
                       "completion":{k:self.trace.events[-1][k] for k in ("seq","operation_id","monotonic_ns")}}}
        if q4["outcome"]=="not assessed":
            state,reason="not_requested","frozen_plan_not_requested"
        elif q4["outcome"]=="unavailable":state,reason="blocked","missing_S1_and_authenticated_views"
        elif q4["reason"]=="authenticated_conflict":state,reason="blocked","authenticated_equal_size_conflict"
        else:state,reason="blocked","requested_S2_authentication_rejected_Q4_edges_not_evaluated"
        self.trace.event("derivation_blocked",component="Q3_from_Q4",state=state,reason=reason)
        return {"state":state,"outcome":None,"reason":reason,"enters":0,"completions":0,
                "mathematical_relation_rejected":False}
    def run(self):
        self.trace.event("start",inventory={k:digest(v) for k,v in self.o.items()},
                         plan=self.plan,binding=self.binding)
        for c in (*OPS,"Q6"):self.results[c]=self.component(c)
        derived=self.derivation()
        routes=[]
        if self.results["Q3_direct"]["outcome"]=="verified":routes.append("direct")
        if derived["state"]=="completed":routes.append("Q4_adjacent_edges")
        proposition={"status":"supported" if routes else "not established","supporting_routes":routes,
                     "scope":"Requested endpoints, same appraisal; no negative mathematical inference."}
        incl=self.results["Q2"]["outcome"]=="verified"
        obs=incl and bool(routes) and self.results["Q4"]["outcome"]=="verified"
        claims={"PA-incl":"supported" if incl else "not established","PA-obs":"supported" if obs else "not established",
          "PB":"not established for an actual environment","PC":"not established for an actual environment",
          "PA-reach":"not established","PA-time":"not established","PA-future":"not established"}
        result={"components":self.results,"q3_proposition":proposition,"q3_derivation":derived,
                "claims":claims,"binding":self.binding,"coverage":{c:{"enters":sum(e["kind"]=="enter" and e.get("component")==c for e in self.trace.events),
                  "completions":sum(e["kind"]=="complete" and e.get("component")==c for e in self.trace.events)}
                  for c in (*OPS,"Q6","Q3_from_Q4")}}
        self.trace.event("result",result=result)
        return result
