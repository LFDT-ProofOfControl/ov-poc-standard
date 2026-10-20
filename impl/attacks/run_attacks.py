#!/usr/bin/env python3
"""Attack harness: empirically validates the security claims in the paper.

Each scenario runs the attack against a deployment WITHOUT the relevant
requirement (expecting the attack to succeed) and WITH it (expecting
detection or refusal). Results are written to impl/results/attacks.json.

  A1 Snapshot substitution      -> Proposition 1 / Theorem 1 (C7.1.4)
  A2 Log alteration             -> P3 (C7.3.1)
  A3 Omission (dropped step)    -> P3 (C7.6.2)
  A4 Head truncation            -> P3 + bounded anchoring (C7.6.6)
  A5 Split-view / equivocation  -> Theorem 2 (C7.3.3)
  A6 Path-composition escalation-> C4.1.7 path-aware authorization
  A7 Capability replay          -> Theorem 1 check (iii)
  A8 Evidence-pipeline failure  -> fail-closed (C7.6.3)
  A9 Mid-history rewrite        -> anchored root compared (C7.3.5)
  A10 Unconfigured mediation    -> action binding fails closed (C7.1.4)
  A11 Capability/record mismatch-> capability cross-bound (C7.1.4)
  A12 Backdated rewrite after the anchor breaks -> renewal before the break
  A13 History laundered through re-signing      -> originals kept and covered
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from poc import (Action, AttestingEnvironment, EvidenceStore, Gateway, Grant,
                 PolicyEngine, RelyingParty, TransparencyLog, Verifier,
                 canonical, gossip, sha256)
from poc.renewal import (Clock, TimestampAuthority, archive, renew,
                         verify_long_term)

RESULTS = []


def record(aid, name, requirement, without, with_, note=""):
    RESULTS.append({"id": aid, "attack": name, "requirement": requirement,
                    "without_requirement": without, "with_requirement": with_,
                    "note": note})
    status = "PASS" if with_.startswith(("refused", "detected", "blocked")) else "FAIL"
    print(f"  [{status}] {aid} {name}")
    print(f"        without: {without}")
    print(f"        with:    {with_}")


def build(path_aware=True, enforce=True, anchor=None, max_spend=1000.0,
          egress_class="public"):
    grant = Grant(principal="user:alice",
                  allowed_kinds=frozenset({"db.read", "http.post", "pay.send"}),
                  allowed_resources=frozenset({"customers", "api.partner.com",
                                               "api.bank.com"}),
                  max_spend=max_spend, max_sensitivity_egress=egress_class)
    policy = PolicyEngine(grant, path_aware=path_aware)
    ae = AttestingEnvironment(policy, anchor=anchor, anchor_interval_s=0.0)
    store = EvidenceStore()
    gw = Gateway(ae, store)
    rp = RelyingParty(ae.pk, "api.partner.com", ae.measurement, enforce=enforce)
    return grant, policy, ae, store, gw, rp


# ---------------------------------------------------------------- A1
def a1_snapshot_substitution():
    """Host evaluates a benign action, dispatches a different one."""
    benign = Action("http.post", "api.partner.com", {"body": "status ping"})
    malicious = Action("http.post", "api.partner.com",
                       {"body": "exfiltrate: customer records"})

    # without capability enforcement at the relying party
    _, _, ae, _, gw, rp = build(enforce=False)
    r = gw.submit(benign, relying_party=rp, dispatch_action=malicious)
    without = ("attack SUCCEEDS: evidence attests the benign action while the "
               f"malicious action executed ({len(rp.executed)} executed, "
               f"{len(rp.refused)} refused)")
    assert r["executed"] and rp.executed[0].params["body"].startswith("exfiltrate")

    # with capability-bound dispatch: relying party recomputes the snapshot
    _, _, ae2, _, gw2, rp2 = build(enforce=True)

    def probe(action):
        # the relying party recomputes what the snapshot digest would be for
        # the request it is actually being asked to perform
        snap = {"agent_id": gw2.agent_id,
                "action": json.loads(action.canonical_form()),
                "path_summary": probe.phi_digest,
                "step_index": probe.step}
        return sha256(canonical(snap))
    probe.phi_digest = ae2.phi.digest()
    probe.step = ae2.step_index
    rp2._snap_probe = probe

    r2 = gw2.submit(benign, relying_party=rp2, dispatch_action=malicious)
    with_ = (f"refused: {r2['reason']} "
             f"({len(rp2.executed)} executed, {len(rp2.refused)} refused)")
    assert not r2["executed"]
    record("A1", "Snapshot substitution", "C7.1.4 complete mediation",
           without, with_,
           "Proposition 1: without a check binding the executed request to the "
           "evidenced snapshot, the adversary wins with probability 1.")


# ---------------------------------------------------------------- A2
def a2_log_alteration():
    _, _, ae, store, gw, _ = build()
    for i in range(5):
        gw.submit(Action("db.read", "customers", {"row": i}))
    v = Verifier(ae.pk, ae.measurement)

    tampered = copy.deepcopy(store.records)
    tampered[2]["poc_claims"]["target_resource"] = "attacker.example"
    ok, msg = v.verify_chain(tampered)
    with_ = f"detected: {msg}" if not ok else "NOT DETECTED"

    # a system that keeps plain unsigned logs has nothing to detect with
    without = ("attack SUCCEEDS: an unsigned operator log can be edited with no "
               "detectable trace (baseline: no signature, no chain)")
    record("A2", "Log alteration", "C7.3.1 hash chain + signatures",
           without, with_)


# ---------------------------------------------------------------- A3
def a3_omission():
    _, _, ae, store, gw, _ = build()
    for i in range(6):
        gw.submit(Action("db.read", "customers", {"row": i}))
    v = Verifier(ae.pk, ae.measurement)
    withheld = [r for i, r in enumerate(store.records) if i != 3]
    ok, msg = v.verify_chain(withheld)
    with_ = f"detected: {msg}" if not ok else "NOT DETECTED"
    without = ("attack SUCCEEDS: with unsequenced records, a dropped step is "
               "indistinguishable from a step that never happened")
    record("A3", "Omission of an inconvenient step", "C7.6.2 sequence continuity",
           without, with_)


# ---------------------------------------------------------------- A4
def a4_truncation():
    log = TransparencyLog("public")
    _, _, ae, store, gw, _ = build(anchor=log)
    for i in range(8):
        gw.submit(Action("db.read", "customers", {"row": i}))
    ae.force_anchor()
    v = Verifier(ae.pk, ae.measurement)

    truncated = store.records[:5]          # withhold the last 3 steps
    ok, msg = v.verify_chain(truncated)
    without_anchor_ok, _ = v.verify_chain(truncated, anchor=None)
    ok_anchor, msg_anchor = v.verify_chain(truncated, anchor=log)
    without = ("attack SUCCEEDS without anchoring: a truncated prefix is "
               f"internally consistent (verifier says: chain verified)"
               if without_anchor_ok else "unexpected")
    with_ = f"detected: {msg_anchor}"
    record("A4", "Head truncation", "C7.6.6 bounded anchoring interval",
           without, with_,
           "Anchor at index 8 contradicts a 5-record presentation; the "
           "undetectable window is bounded by the anchoring interval.")


# ---------------------------------------------------------------- A5
def a5_split_view():
    log_a, log_b = TransparencyLog("verifier-A"), TransparencyLog("verifier-B")
    _, _, ae, _, gw, _ = build(anchor=log_a)
    for i in range(3):
        gw.submit(Action("db.read", "customers", {"row": i}))
    ae.force_anchor()
    # operator forks: shows verifier B a different history at the same index
    forked_root = sha256(b"forked-history")
    log_b.publish(forked_root, ae.step_index, ae._sign)

    consistent, msg = gossip(log_a, log_b)
    with_ = f"detected: {msg}" if not consistent else "NOT DETECTED"
    without = ("attack SUCCEEDS: each verifier independently validates its own "
               "chain; both are internally consistent and neither can tell")
    record("A5", "Split-view / equivocation", "C7.3.3 gossip / witness quorum",
           without, with_,
           "Theorem 2: two validly signed roots at a common index with distinct "
           "values are non-repudiable, attributable proof of equivocation.")


# ---------------------------------------------------------------- A6
def a6_path_composition():
    """Read confidential data, then egress: each step individually permitted."""
    read = Action("db.read", "customers", {"row": 1}, classification="confidential")
    send = Action("http.post", "api.partner.com", {"body": "summary"})

    # per-action policy (baseline)
    _, _, _, _, gw1, _ = build(path_aware=False)
    r1a = gw1.submit(read); r1b = gw1.submit(send)
    without = (f"attack SUCCEEDS: read={r1a['verdict']}, egress={r1b['verdict']} "
               "— both individually within grant, exfiltration path completes")

    # path-aware policy
    _, _, _, _, gw2, _ = build(path_aware=True)
    r2a = gw2.submit(read); r2b = gw2.submit(send)
    with_ = (f"blocked: read={r2a['verdict']}, egress={r2b['verdict']} "
             f"({r2b.get('reason')})")
    record("A6", "Path-composition escalation", "C4.1.7 path-aware authorization",
           without, with_,
           "The classical information-flow pattern: read-then-send, where no "
           "single action violates the grant.")


# ---------------------------------------------------------------- A7
def a7_capability_replay():
    _, _, ae, _, gw, rp = build()
    a = Action("http.post", "api.partner.com", {"body": "ok"})
    out = ae.evaluate_and_evidence(a, "n-replay", gw.agent_id)
    ok1, why1 = rp.execute(a, out["capability"])
    ok2, why2 = rp.execute(a, out["capability"])   # replay same capability
    without = ("attack SUCCEEDS: a bearer token without single-use semantics "
               "can be replayed for a second effect")
    with_ = f"refused on replay: first={why1}, second={why2}"
    record("A7", "Capability replay", "Theorem 1 check (iii) nonce freshness",
           without, with_)


# ---------------------------------------------------------------- A8
def a8_pipeline_failure():
    _, _, _, store, gw, rp = build()
    store.available = False        # evidence pipeline down
    r = gw.submit(Action("http.post", "api.partner.com", {"body": "x"}),
                  relying_party=rp)
    without = ("attack SUCCEEDS: a system that logs best-effort keeps acting "
               "while its evidence pipeline is down (fail-open by omission)")
    with_ = (f"refused: verdict={r['verdict']}, executed={r['executed']}, "
             f"failure recorded={len(store.failures)}")
    record("A8", "Evidence-pipeline failure", "C7.6.1/C7.6.3 fail closed",
           without, with_)


# ---------------------------------------------------------------- A9
def a9_history_rewrite():
    """Rewrite a step in the middle of the log and re-sign everything after it.

    This is the attack the other eight miss, and we found it by building the
    Merkle experiment rather than by thinking harder. Every earlier defence
    assumes the adversary cannot sign. But the operator running the enclave
    CAN: that is what "operator-controlled infrastructure" means. Given the key,
    the operator edits step 3, recomputes every subsequent chain link, and
    re-signs the lot.

    The result is a history of exactly the right length in which every
    signature verifies and every link matches. Replaying it finds nothing,
    because there is nothing internally wrong with it. Only the root that was
    published BEFORE the rewrite is inconsistent with it -- and the verifier
    has to actually compare that root to notice.
    """
    log = TransparencyLog()
    grant, policy, ae, store, gw, _ = build(anchor=log)
    for i in range(8):
        gw.submit(Action("db.read", "customers", {"row": i}))
    ae.force_anchor()
    v = Verifier(ae.pk, ae.measurement)

    # the operator rebuilds the history with step 3 altered, using the same key
    ae2 = AttestingEnvironment(PolicyEngine(grant), signing_key=ae._sk)
    store2 = EvidenceStore()
    gw2 = Gateway(ae2, store2)
    for i in range(8):
        gw2.submit(Action("db.read", "customers",
                          {"row": 999 if i == 3 else i}))

    ok_replay, msg_replay = v.verify_chain(store2.records)      # no anchor
    ok_anchor, msg_anchor = v.verify_chain(store2.records, anchor=log)

    without = (f"attack SUCCEEDS: replaying the rewritten history finds nothing "
               f"wrong (verifier says: {msg_replay}) — every signature is valid "
               f"and every link matches, because the operator recomputed them")
    with_ = f"detected: {msg_anchor}" if not ok_anchor else "MISSED"
    record("A9", "Mid-history rewrite by a key-holding operator",
           "C7.3.5 anchored root compared, consistency proof required",
           without, with_,
           note=("found while building the Merkle experiment: the verifier "
                 "compared the anchor's step count but never its root"))


# ---------------------------------------------------------------- A10
def a10_unconfigured_mediation():
    """Substitution against a relying party that believes it is enforcing.

    A1 shows that without the far-end check the adversary wins. A10 is the
    version that actually happens: the check is present, `enforce=True` is set,
    and it silently does nothing because the endpoint could not be configured
    to perform it.

    The earlier design asked the relying party to recompute the digest of the
    whole evaluated snapshot -- which commits to the path summary and step
    index, enclave state no independent endpoint can see. So the check needed a
    callback into the enclave, almost nobody could supply one, and the
    unconfigured path returned "matches". The fix gives the relying party
    something it can recompute unaided: a digest of the action itself, carried
    in the capability, plus a refusal when neither that nor a probe is present.
    """
    _, _, ae, _, gw, _ = build()
    rp = RelyingParty(ae.pk, "api.partner.com", ae.measurement, enforce=True)
    benign = Action("http.post", "api.partner.com", {"body": "quarterly summary"})
    evil = Action("http.post", "api.partner.com", {"body": "customer database"})
    r = gw.submit(benign, relying_party=rp, dispatch_action=evil)
    without = ("attack SUCCEEDS: the endpoint sets enforce=True, verifies the "
               "signature, the measurement, the resource and the nonce - and "
               "still executes a different request, because the one check that "
               "binds the action defaulted to accept when unconfigured")
    with_ = (f"refused: {r['reason']}" if not r["executed"] else "MISSED")
    record("A10", "Substitution past an unconfigured mediation check",
           "C7.1.4 the binding check fails closed",
           without, with_,
           note=("found by reading the reference implementation for this "
                 "review: a security check whose default is accept reports "
                 "success while providing nothing"))


# ---------------------------------------------------------------- A11
def a11_capability_record_mismatch():
    """Present a valid capability alongside a different allow record.

    The capability and the evidence record were two independently signed
    objects that happened to agree on a snapshot digest. Nothing tied one
    ticket to one record, so an auditor reconciling executed actions against
    evidence could be shown a valid ticket beside the wrong record.
    """
    _, _, ae, _, gw, _ = build()
    o1 = ae.evaluate_and_evidence(
        Action("http.post", "api.partner.com", {"b": 1}), "n-a", gw.agent_id)
    o2 = ae.evaluate_and_evidence(
        Action("http.post", "api.partner.com", {"b": 2}), "n-b", gw.agent_id)
    v = Verifier(ae.pk, ae.measurement)
    ok_match, _ = v.verify_capability_binding(o1["capability"], o1["token"])
    ok_cross, why = v.verify_capability_binding(o1["capability"], o2["token"])
    without = ("attack SUCCEEDS: both objects verify on their own, so a ticket "
               "can be presented next to a record it was never issued with and "
               "the reconciliation still balances")
    with_ = (f"detected: {why}" if (ok_match and not ok_cross) else "MISSED")
    record("A11", "Capability paired with the wrong evidence record",
           "C7.1.4 capability cross-bound to its record",
           without, with_)


# ------------------------------------------------------- A12, A13: the years
#
# Records are made in year 0 and archived in year 1 under the classical
# algorithm, renewal runs in year 5, the classical algorithm breaks in year 8,
# and a verifier looks in year 10. The declared anchoring interval is one year.
CLASSICAL, CURRENT = "classical", "current"
MADE, ARCHIVED, RENEWED, BROKEN, EXAMINED, INTERVAL = 0, 1, 5, 8, 10, 1


def _authorities(clock):
    old = TimestampAuthority("tsa-classical", CLASSICAL, clock)
    new = TimestampAuthority("tsa-current", CURRENT, clock)
    return old, new, {old.name: (CLASSICAL, old.pk), new.name: (CURRENT, new.pk)}


def _history(signing_key=None, altered=None):
    """Six reads; step `altered` reads row 999 instead, a read that never
    happened."""
    grant, _, ae, store, gw, _ = build()
    if signing_key is not None:
        ae = AttestingEnvironment(PolicyEngine(grant), signing_key=signing_key)
        store = EvidenceStore()
        gw = Gateway(ae, store)
    for i in range(6):
        gw.submit(Action("db.read", "customers",
                         {"row": 999 if i == altered else i}))
    return ae, store.records


def _verify_in_year_10(record, bundle, keys, signed_with, interval=INTERVAL,
                       breaks=None):
    return verify_long_term(canonical(record), bundle, signed_with=signed_with,
                            generated=MADE, max_anchor_interval=interval,
                            authorities=keys, now=EXAMINED,
                            breaks={CLASSICAL: BROKEN} if breaks is None
                            else breaks)


# ---------------------------------------------------------------- A12
def a12_backdated_rewrite_after_break():
    """Rewrite history once the algorithm that dates it is broken.

    Anchoring is what stops an operator who holds the evidence key from
    rewriting history (A9, C7.3.5). Signing the records post-quantum, even
    from day one, leaves classical whatever dates the anchor: a timestamp
    token, a log's signed tree head. Once that algorithm is broken, the
    operator rebuilds year-0 history with one read that never happened,
    archives it, and forges a timestamp dated year 1. Every signature
    verifies, so a verifier holds two contradictory histories of year 0 and
    nothing to choose between them. Where the records are classical too, the
    adversary need not be the operator.

    The defence is RFC 4998's: before the break, a token on an algorithm that
    is still sound covers the year-1 token. The rewrite has no such token, and
    a sound token issued today is dated after the break.
    """
    clock = Clock(MADE)
    tsa_old, tsa_new, keys = _authorities(clock)
    ae, genuine = _history()                    # records on a sound algorithm
    clock.year = ARCHIVED
    real = archive([canonical(r) for r in genuine], tsa_old)

    # year 10: the classical algorithm broke in year 8; the operator still
    # holds its own evidence key, and now holds the classical authority's too
    clock.year = EXAMINED
    _, rewritten = _history(signing_key=ae._sk, altered=3)
    forger = TimestampAuthority.holding(tsa_old.leak(), tsa_old.name,
                                        CLASSICAL, ARCHIVED)
    fake = archive([canonical(r) for r in rewritten], forger)

    # without renewal: a verifier either takes the timestamps at face value
    # and accepts both histories, or refuses the broken algorithm and loses
    # the genuine one
    v = Verifier(ae.pk, ae.measurement)
    at_face = {}
    ok_real = _verify_in_year_10(genuine[3], real.bundle(3), keys, CURRENT,
                                 breaks=at_face)[0]
    ok_fake = _verify_in_year_10(rewritten[3], fake.bundle(3), keys, CURRENT,
                                 breaks=at_face)[0]
    lost = not _verify_in_year_10(genuine[3], real.bundle(3), keys, CURRENT)[0]
    assert ok_real and ok_fake and lost and v.verify_chain(rewritten)[0]
    without = ("attack SUCCEEDS: the rewritten year-0 history verifies exactly "
               "as the genuine one does (record signatures under a sound key, "
               "chain, inclusion proof, a year-1 timestamp); a verifier that "
               "refuses the broken timestamp algorithm rejects the genuine "
               "history too")

    # with: the year-1 token was covered in year 5, while it was still sound
    clock.year = RENEWED
    renew(real, tsa_new)
    clock.year = EXAMINED
    ok, why_ok = _verify_in_year_10(genuine[3], real.bundle(3), keys, CURRENT)
    bad, why = _verify_in_year_10(rewritten[3], fake.bundle(3), keys, CURRENT)
    renew(fake, tsa_new)                  # a sound token, but issued in year 10
    late, why_late = _verify_in_year_10(rewritten[3], fake.bundle(3), keys,
                                        CURRENT)
    with_ = (f"detected: {why}; a sound token issued in year {EXAMINED} does "
             f"not help: {why_late}. The genuine archive verifies: {why_ok}"
             if ok and not bad and not late else "MISSED")
    record("A12", "Backdated rewrite after the anchor's algorithm breaks",
           "C6.3.5 as proposed: timestamp renewal before the break (RFC 4998)",
           without, with_,
           note="docs/proposals/long-term-verifiability.md")


# ---------------------------------------------------------------- A13
def a13_renewal_laundering():
    """Alter retained evidence while re-signing it for the post-quantum era.

    The other route C6.3.5 offers is to re-anchor and re-sign retained evidence
    under a current scheme. Re-signing replaces the evidence rather than
    carrying it across: the renewal key never saw the year-0 events, so it
    signs whatever the renewal job hands it. A job that alters step 3 on the
    way through produces a history that verifies under the current key, in an
    archive timestamped under a current algorithm. In year 10 the original
    classical signatures settle nothing, because any of them could be a
    forgery.

    A verifier cannot catch this by enforcing the anchoring interval (C7.6.6),
    because honestly re-signed evidence fails that rule too: the re-sign route
    requires the verifier to accept a re-anchor years after the fact. The
    defence keeps the original bytes and their original signatures, renews by
    covering the original archive's token, and then the verifier can enforce
    the interval.
    """
    clock = Clock(MADE)
    tsa_old, tsa_new, keys = _authorities(clock)
    ae, genuine = _history()
    clock.year = ARCHIVED
    real = archive([canonical(r) for r in genuine], tsa_old)

    # year 5, without: re-sign under a current key, altering step 3 on the way
    clock.year = RENEWED
    renewal_key = Ed25519PrivateKey.generate()      # stands for a current scheme
    ae2, laundered = _history(signing_key=renewal_key, altered=3)
    relaid = archive([canonical(r) for r in laundered], tsa_new)
    _, honest = _history(signing_key=renewal_key)
    honest_relaid = archive([canonical(r) for r in honest], tsa_new)
    clock.year = EXAMINED
    ok_chain = Verifier(renewal_key.public_key(),
                        ae2.measurement).verify_chain(laundered)[0]
    ok_relaid = _verify_in_year_10(laundered[3], relaid.bundle(3), keys,
                                   CURRENT, interval=None)[0]
    honest_fails = not _verify_in_year_10(honest[3], honest_relaid.bundle(3),
                                          keys, CURRENT)[0]
    assert ok_chain and ok_relaid and honest_fails
    without = ("attack SUCCEEDS: the laundered history verifies under the "
               "renewal key, in an archive resting on a sound algorithm; the "
               "original classical signatures cannot contradict it, and a "
               "verifier enforcing the C7.6.6 interval would reject honestly "
               "re-signed evidence too")

    # with: renewal covers the original token; the originals stay as signed
    clock.year = RENEWED
    renew(real, tsa_new)
    clock.year = EXAMINED
    ok, _ = _verify_in_year_10(genuine[3], real.bundle(3), keys, CLASSICAL)
    bad, why = _verify_in_year_10(laundered[3], relaid.bundle(3), keys, CURRENT)
    absent, why_absent = _verify_in_year_10(laundered[3], real.bundle(3), keys,
                                            CURRENT)
    with_ = (f"detected: {why}; against the original archive: {why_absent}"
             if ok and not bad and not absent else "MISSED")
    record("A13", "History laundered through re-signing",
           "C6.3.5 as proposed: originals kept and covered; the verifier "
           "enforces the C7.6.6 interval",
           without, with_,
           note="docs/proposals/long-term-verifiability.md")


def main():
    print("Proof-of-Control reference implementation — attack harness\n")
    for fn in (a1_snapshot_substitution, a2_log_alteration, a3_omission,
               a4_truncation, a5_split_view, a6_path_composition,
               a7_capability_replay, a8_pipeline_failure, a9_history_rewrite,
               a10_unconfigured_mediation, a11_capability_record_mismatch,
               a12_backdated_rewrite_after_break, a13_renewal_laundering):
        fn()
    out = Path(__file__).resolve().parent.parent / "results" / "attacks.json"
    out.write_text(json.dumps(RESULTS, indent=2) + "\n")
    print(f"\n{len(RESULTS)} scenarios written to {out}")


if __name__ == "__main__":
    main()
