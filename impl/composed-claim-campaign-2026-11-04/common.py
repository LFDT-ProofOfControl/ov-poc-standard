"""Canonical supplied formats and fixed-role Ed25519 verification."""
import hashlib
import json
import re
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

ROLES = ("V", "A", "RVP", "AR", "LO", "W1", "W2")
OPS = ("Q1a", "Q1b", "Q1c", "Q2", "Q3_direct", "Q4", "Q5")
KIND = {"R":"report", "certificate":"certificate", "collateral":"collateral",
        "publication":"publication", "directory":"directory", "S1":"head", "S2":"head",
        "W1_head":"head", "W2_head":"head", "W1_delivery":"delivery",
        "W2_delivery":"delivery", "time_receipt":"time_receipt"}
FIELDS = {
 "report": {"report_id":"s","claim":"s","measurement":"h","challenge":"h","signer_id":"s"},
 "certificate":{"subject_id":"s","public_key":"h","not_before":"i","not_after":"i"},
 "collateral":{"subject_id":"s","not_before":"i","not_after":"i","revoked":"ids"},
 "publication":{"claim":"s","measurement":"h"},
 "directory":{"policy_version":"s","entries":"entries"},
 "entry":{"key_id":"s","claim":"s","not_before":"i","not_after":"i","disposition":"s"},
 "head":{"log_id":"s","size":"i","root":"h","timestamp":"i","key_id":"s"},
 "delivery":{"source_id":"s","challenge":"h","log_id":"s","head_digest":"h"},
 "time_receipt":{"log_id":"s","report_digest":"h","logical_time":"i"},
 "M":{"measurement":"h"},
 "inclusion":{"index":"i","size":"i","nodes":"nodes"},
 "consistency":{"from_size":"i","to_size":"i","nodes":"nodes"},
}

def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode("ascii")

def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else encode(value)).hexdigest()

def exact(obj, keys):
    if not isinstance(obj, dict) or set(obj) != set(keys):
        raise ValueError("unexpected object fields")

def integer(v):
    return type(v) is int and 0 <= v <= 2**53-1

def hexbytes(v, n=32):
    if not isinstance(v, str) or not re.fullmatch("[0-9a-f]{%d}" % (n*2), v):
        raise ValueError("invalid fixed hex")
    return bytes.fromhex(v)

def text(v):
    return isinstance(v, str) and 0 < len(v) <= 256 and v.isascii()

def fields(obj, spec):
    exact(obj, spec)
    for k, kind in spec.items():
        v = obj[k]
        if kind == "s":
            if not text(v): raise ValueError("invalid ASCII text")
        elif kind == "i":
            if not integer(v): raise ValueError("invalid integer")
        elif kind == "h": hexbytes(v)
        elif kind in ("nodes", "ids", "entries"):
            if not isinstance(v, list) or len(v) > (64 if kind=="nodes" else 16):
                raise ValueError("invalid bounded list")
            for e in v:
                if kind == "nodes": hexbytes(e)
                elif kind == "ids":
                    if not text(e): raise ValueError("invalid ID")
                else:
                    fields(e, FIELDS["entry"])
                    if e["disposition"] not in ("allow", "deny"): raise ValueError("disposition")
        else: raise ValueError("unknown schema type")
    if "not_before" in obj and obj["not_before"] >= obj["not_after"]:
        raise ValueError("empty or reversed interval")
    for k in ("size", "from_size", "to_size"):
        if k in obj and not 1 <= obj[k] <= 1024: raise ValueError("tree size bound")

def signing_bytes(kind, payload):
    return b"AARM-COMPOSED-v1:" + kind.encode("ascii") + b"\0" + encode(payload)

def verify(env, key_id, keys):
    if env["key_id"] != key_id:
        return False
    try:
        Ed25519PublicKey.from_public_bytes(hexbytes(keys[key_id])).verify(
            hexbytes(env["signature"],64), signing_bytes(env["kind"],env["payload"]))
        return True
    except InvalidSignature:
        return False

def validate_input(v):
    exact(v, ("objects","trust","plan"))
    o,t,p = v["objects"],v["trust"],v["plan"]
    if not isinstance(o,dict) or len(o)>17 or "R" not in o:
        raise ValueError("object inventory")
    allowed=set(KIND)|{"M","inclusion","direct","edge_3_5","edge_5_7"}
    if set(o)-allowed: raise ValueError("undeclared input role")
    for role,obj in o.items():
        if role in KIND:
            exact(obj,("kind","key_id","payload","signature"))
            if obj["kind"] != KIND[role] or not text(obj["key_id"]):
                raise ValueError("wrong envelope kind/identity")
            hexbytes(obj["signature"],64);fields(obj["payload"],FIELDS[obj["kind"]])
        else:
            fields(obj,FIELDS["consistency" if role in ("direct","edge_3_5","edge_5_7") else role])
    exact(t,("keys","claim","log_id","challenge","report_id","appraisal_time","policy_version"))
    exact(t["keys"],ROLES)
    for k in ROLES: hexbytes(t["keys"][k])
    for k in ("claim","log_id","report_id","policy_version"):
        if not text(t[k]): raise ValueError("trust text")
    hexbytes(t["challenge"])
    if not integer(t["appraisal_time"]): raise ValueError("appraisal time")
    exact(p,("operations","derivation"))
    if not isinstance(p["operations"],list) or len(set(p["operations"]))!=len(p["operations"]):
        raise ValueError("plan duplicates")
    if p["operations"] not in [list(OPS),[x for x in OPS if x not in ("Q3_direct","Q4")]]:
        raise ValueError("unfrozen schedule")
    if p["derivation"] != "after_verified_Q4": raise ValueError("derivation schedule")
    return v

def strict_load(raw):
    if len(raw)>1024*1024: raise ValueError("input too large")
    def pairs(xs):
        d={}
        for k,v in xs:
            if k in d: raise ValueError("duplicate JSON key")
            d[k]=v
        return d
    def reject(v): raise ValueError("noninteger numeric encoding")
    v=json.loads(raw,object_pairs_hook=pairs,parse_float=reject,parse_constant=reject)
    def walk(x):
        if isinstance(x,dict):
            for k,v in x.items():
                if not isinstance(k,str) or not k.isascii(): raise ValueError("nonASCII key")
                walk(v)
        elif isinstance(x,list):
            for y in x: walk(y)
        elif type(x) is int:
            if not integer(x): raise ValueError("integer bound")
        elif isinstance(x,str):
            if not x.isascii(): raise ValueError("nonASCII value")
        else: raise ValueError("null/bool/nonvalue input")
    walk(v)
    if encode(v)!=raw: raise ValueError("noncanonical JSON")
    return validate_input(v)
