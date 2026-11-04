"""One future sandbox component/primitive/denial control; never a full appraisal."""
import errno
import json
import os
from pathlib import Path
import socket
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from common import strict_load
from assessor import Assessor
from merkle import inclusion, consistency

def main():
    checks = {}
    def require(name, value):
        checks[name] = bool(value)
        if not value:
            raise RuntimeError(name)
    ed = json.loads(Path("ED25519-VECTOR.json").read_text())
    key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(ed["public_key"]))
    signature = bytes.fromhex(ed["signature"])
    message = bytes.fromhex(ed["message"])
    key.verify(signature, message)
    require("ed25519_positive", True)
    invalid = bytes([signature[0] ^ 1]) + signature[1:]
    try:
        key.verify(invalid, message)
    except InvalidSignature:
        require("ed25519_invalid_signature_rejected", True)
    else:
        require("ed25519_invalid_signature_rejected", False)
    vector = json.loads(Path("MERKLE-VECTOR.json").read_text())
    nodes, proofs = vector["nodes"], vector["proofs"]
    entry = bytes.fromhex(vector["entries"][1])
    path = [bytes.fromhex(x) for x in proofs["inclusion_1_7"]]
    require("merkle_inclusion_positive", inclusion(entry,1,7,path,bytes.fromhex(nodes["R7"])))
    bad = [bytes([path[0][0]^1])+path[0][1:]] + path[1:]
    require("merkle_invalid_inclusion_rejected", not inclusion(entry,1,7,bad,bytes.fromhex(nodes["R7"])))
    for name, old, new in [("consistency_3_7",3,7),("consistency_3_5",3,5),("consistency_5_7",5,7)]:
        path = [bytes.fromhex(x) for x in proofs[name]]
        require(name+"_positive", consistency(old,new,bytes.fromhex(nodes["R"+str(old)]),bytes.fromhex(nodes["R"+str(new)]),path))
        bad = [bytes([path[0][0]^1])+path[0][1:]] + path[1:]
        require(name+"_invalid_node_rejected", not consistency(old,new,bytes.fromhex(nodes["R"+str(old)]),bytes.fromhex(nodes["R"+str(new)]),bad))
    supplied = strict_load(Path("supplied.json").read_bytes())
    acquisition = json.loads(Path("acquisition.json").read_text())
    events = []
    assessor = Assessor(supplied, acquisition, events.append)
    assessor.q2()
    # A component operation only; Assessor.run and the grader are never invoked.
    completed = [event for event in events if event["kind"]=="complete"]
    require("permitted_Q2_component", len(completed)==2 and
            {event["name"] for event in completed}=={"auth_S2","inclusion"} and
            all(event["outcome"]=="verified" for event in completed))
    canaries = json.loads(Path("control-paths.json").read_text())
    def denied(name, action):
        try:
            action()
        except OSError as exc:
            require(name, exc.errno in (errno.EPERM, errno.EACCES))
        else:
            require(name, False)
    for name in ["oracle","case_label","generator_knowledge","symlink_escape"]:
        denied(name+"_read_denied", lambda n=name: Path(canaries[n]).read_bytes())
    denied("write_denied", lambda: Path("forbidden-write.txt").write_bytes(b"public control"))
    def network():
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            sock.connect(("127.0.0.1",9))
    denied("network_denied", network)
    def fork():
        child = os.fork()
        if child == 0:
            os._exit(0)
        os.waitpid(child,0)
    denied("fork_denied", fork)
    require("inherited_api_environment_absent",
            not any("OPENAI" in name.upper() or "API_KEY" in name.upper() for name in os.environ))
    print(json.dumps({"checks":checks,"Q2_component_events":events,
                      "full_appraisals":0,"grade_calls":0,"signing_keys_generated":0},sort_keys=True))

if __name__ == "__main__":
    main()
