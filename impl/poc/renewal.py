"""Long-term verifiability: evidence that must still verify after the
algorithms that date or sign it are broken.

WHY THIS FILE EXISTS. Evidence is examined long after it is made; the paper
sizes storage for evidence kept "for the seven years a regulator might ask
about". C6.3.5 meets the signature horizon in one of two ways: sign
post-quantum, or "re-anchor and re-sign retained evidence under a current
scheme before the projection lapses". Each leaves a hole, and attacks A12 and
A13 show what each one costs.

  1. Post-quantum record signatures, even from day one, leave classical
     whatever DATES the evidence: a timestamp token, a log's signed tree head,
     the hardware quote. Anchoring is what stops a key-holding operator from
     rewriting history (A9). Once the anchor's algorithm is broken, the
     operator rewrites history and dates a forged anchor before the rewrite,
     and every signature verifies (A12). Where the records are classical too,
     the adversary need not be the operator.

  2. Re-signing does not carry old evidence across the break: it replaces it.
     A re-signing step that does not verify the originals is a statement by
     whoever ran it, which is authenticated documentation in C8's terms. A
     renewal job that alters a record while it re-signs produces a history
     that verifies under the new key (A13).

THE CONSTRUCTION. RFC 4998 (Evidence Record Syntax) standardized the answer in
2007, after Bayer, Haber and Stornetta (1993). This module implements the part
of it the argument needs.

  archive   A Merkle tree (RFC 6962 hashing, merkle.py) over the evidence
            records exactly as they were signed, original signatures included,
            and a timestamp token over its root.
  renew     Before the algorithm under the newest token is retired, a token
            from an authority on another algorithm timestamps the previous
            token's bytes (RFC 4998 section 5.2, timestamp renewal). Nothing is
            re-signed and nothing is replaced: the chain only grows.
  verify    The record is in the root; each token covers the one before it;
            the root was first timestamped within the declared anchoring
            interval of the record's generation (C7.6.6); and every token whose
            algorithm is broken, or whose authority's key is compromised, by the
            time of verification is covered by a later token issued BEFORE that
            (RFC 4998 section 5.3). The newest token must still be sound.

Renewal has to happen while the old algorithm is still sound, and that is the
whole argument: a token issued in year 5 shows the year-1 token existed in year
5, and in year 5 nobody could forge a year-1 token. Induction from the newest
token, which is sound today, carries that back to the record.

WHAT IS MODELLED. Every key is Ed25519, so the harness keeps its single
dependency. Each authority carries the NAME of the algorithm it stands for, and
a break is modelled operationally: from the break on, the adversary holds that
algorithm's private keys, which is what "forgeable" means to a verifier. An
honest authority dates by the shared Clock; only a key holder can choose the
date. Time is an integer number of years, so every scenario is deterministic.
A break is known only once disclosed, so the dates a verifier passes in
`breaks` and `compromised` should be its most conservative estimates, not the
disclosure dates. One authority stands in for the renewal anchor; C6.3.5 as
proposed requires an open one (a log with monitors, a ledger, or a quorum).
Hash-tree renewal (RFC 4998 section 5.2, needed only if SHA-256 itself weakens)
is out of scope.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey,
)

from .core import canonical
from .merkle import MerkleTree, leaf_hash, verify_inclusion

__all__ = ["Clock", "TimestampAuthority", "Archive", "archive", "renew",
           "issue_token", "verify_long_term"]


def _digest(obj: dict) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()


def issue_token(sk: Ed25519PrivateKey, tsa: str, alg: str, digest: str,
                t: int) -> dict:
    """A token binding `digest` to year `t`: RFC 3161's job, reduced to the
    fields the argument needs. Whoever holds `sk` can date it any year they
    like, which is exactly what a broken algorithm hands an adversary."""
    body = {"tsa": tsa, "alg": alg, "digest": digest, "t": t}
    return {**body, "signature": sk.sign(canonical(body)).hex()}


class Clock:
    """The year as honest parties see it. Scenarios advance it."""

    def __init__(self, year: int = 0):
        self.year = year


class TimestampAuthority:
    """Issues tokens under one named algorithm, dated by its clock. The key
    leaves only through `leak()`, which is how a break is modelled."""

    def __init__(self, name: str, alg: str, clock: Clock):
        self.name = name
        self.alg = alg
        self.clock = clock
        self._sk = Ed25519PrivateKey.generate()
        self.pk: Ed25519PublicKey = self._sk.public_key()

    @classmethod
    def holding(cls, sk: Ed25519PrivateKey, name: str, alg: str,
                year: int) -> "TimestampAuthority":
        """Whoever holds an authority's key is that authority, and dates its
        tokens whatever year it likes."""
        tsa = cls.__new__(cls)
        tsa.name, tsa.alg, tsa.clock = name, alg, Clock(year)
        tsa._sk, tsa.pk = sk, sk.public_key()
        return tsa

    def stamp(self, digest: str) -> dict:
        return issue_token(self._sk, self.name, self.alg, digest,
                           self.clock.year)

    def leak(self) -> Ed25519PrivateKey:
        """The algorithm is broken: from here on, anyone can sign as us."""
        return self._sk


@dataclass
class Archive:
    """One archived set and its timestamp chain (RFC 4998's evidence record,
    reduced to a single archive timestamp chain)."""
    records: list[bytes]
    tree: MerkleTree
    chain: list[dict] = field(default_factory=list)

    @property
    def root(self) -> str:
        return self.tree.root().hex()

    def bundle(self, index: int) -> dict:
        """What a relying party retains for record `index`, and all it needs:
        the inclusion proof, the root, and the whole token chain."""
        return {"index": index, "tree_size": self.tree.size,
                "proof": [p.hex() for p in self.tree.inclusion_proof(index)],
                "root": self.root, "chain": [dict(t) for t in self.chain]}


def archive(records: list[bytes], tsa: TimestampAuthority) -> Archive:
    """Archive records exactly as signed, and timestamp the root."""
    tree = MerkleTree()
    for r in records:
        tree.append(r)
    a = Archive(list(records), tree)
    a.chain.append(tsa.stamp(a.root))
    return a


def renew(a: Archive, tsa: TimestampAuthority) -> None:
    """Timestamp renewal: a token on another algorithm covers the newest
    token's bytes. The archived records are not touched."""
    a.chain.append(tsa.stamp(_digest(a.chain[-1])))


def verify_long_term(record: bytes, bundle: dict, *, signed_with: str,
                     generated: int, max_anchor_interval: int | None,
                     authorities: dict[str, tuple[str, Ed25519PublicKey]],
                     breaks: dict[str, int], now: int,
                     compromised: dict[str, int] | None = None
                     ) -> tuple[bool, str]:
    """Did `record` exist, signed, before anything it rests on was broken?

    The record's own signature is verified by the caller under the evidence
    key in force when it was generated (Verifier does that), and the caller
    supplies that signature's algorithm and the generation year, because the
    scenarios' years are not the token's `iat`. This function establishes WHEN
    the record existed, which is what turns a mathematically valid signature
    into evidence once its algorithm is forgeable.

    `authorities` maps a timestamp authority's name to its published
    (algorithm, key). `breaks` maps an algorithm, and `compromised` an
    authority, to the year from which the verifier treats it as forgeable.
    `max_anchor_interval=None` is a verifier that does not enforce C7.6.6,
    which is what accepting a later re-anchor of old evidence requires.
    """
    chain = bundle["chain"]
    if not chain:
        return False, "no timestamp covers the archive"
    compromised = compromised or {}

    def unsound_from(tok: dict) -> int | None:
        years = [y for y in (breaks.get(tok["alg"]), compromised.get(tok["tsa"]))
                 if y is not None and y <= now]
        return min(years) if years else None

    proof = [bytes.fromhex(p) for p in bundle["proof"]]
    if not verify_inclusion(bundle["index"], bundle["tree_size"],
                            leaf_hash(record), proof,
                            bytes.fromhex(bundle["root"])):
        return False, "record is not in the archived root"
    if chain[0]["digest"] != bundle["root"]:
        return False, "the first token does not cover the archived root"
    for i in range(1, len(chain)):
        if chain[i]["digest"] != _digest(chain[i - 1]):
            return False, f"token {i} does not cover token {i - 1}"
        if chain[i]["t"] < chain[i - 1]["t"]:
            return False, f"token {i} is dated before the token it covers"
    if chain[0]["t"] < generated:
        return False, "the first token is dated before the record was generated"
    if chain[-1]["t"] > now:
        return False, f"token {len(chain) - 1} is dated in the future"

    for i, tok in enumerate(chain):
        published = authorities.get(tok["tsa"])
        if published is None or published[0] != tok["alg"]:
            return False, f"token {i} names an unknown authority or algorithm"
        body = {k: v for k, v in tok.items() if k != "signature"}
        try:
            published[1].verify(bytes.fromhex(tok["signature"]), canonical(body))
        except InvalidSignature:
            return False, f"token {i} signature invalid"

    if max_anchor_interval is not None and \
            chain[0]["t"] - generated > max_anchor_interval:
        return False, (f"first timestamped in year {chain[0]['t']}, "
                       f"{chain[0]['t'] - generated} years after the record "
                       f"was generated; the declared anchoring interval is "
                       f"{max_anchor_interval}")

    # Existence before every break. Token i is credible only if token i+1,
    # itself credible, was issued while token i could not yet be forged.
    for i, tok in enumerate(chain):
        year = unsound_from(tok)
        if year is None:
            continue
        why = f"token {i} ({tok['tsa']}, {tok['alg']}) is forgeable from year {year}"
        nxt = chain[i + 1] if i + 1 < len(chain) else None
        if nxt is None:
            return False, f"{why}, and nothing covers it"
        if nxt["t"] >= year:
            return False, (f"{why}, and the token covering it was issued in "
                           f"year {nxt['t']}, after that")
    year = breaks.get(signed_with)
    if year is not None and year <= now and chain[0]["t"] >= year:
        return False, (f"the record's {signed_with} signature is not shown "
                       f"to predate that algorithm's break in year {year}")
    return True, (f"existence shown back to year {chain[0]['t']} through "
                  f"{len(chain)} token(s); newest rests on {chain[-1]['alg']}")
