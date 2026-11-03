"""Synthetic declared-input model; see CONTRACT.md for scope and exclusions.

No live source, provenance authentication, timestamp selection or
persistence is implemented. Export changes are recorded in PROVENANCE.md.
"""

from collections import defaultdict
from copy import deepcopy
import hashlib
import json


def serialized(value):
    """The explicit serialization used only by this bounded fixture model."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(serialized(value)).hexdigest()


def reconcile(obligations, records, unresolved):
    """Keep supplied presence separate from identity admissibility."""
    by_id = defaultdict(set)
    supplied = set()
    for rid, key, content in records:
        by_id[rid].add((rid, key, content))
        supplied.add(key)

    conflicts = []
    admitted = defaultdict(set)
    unmatched = []
    for rid, variants in sorted(by_id.items()):
        bindings = {record[1] for record in variants}
        if len(variants) > 1:
            conflicts.append({
                "record_id": rid,
                "variants": [list(record) for record in sorted(variants)],
                "affected_declared_units": sorted(bindings & obligations.keys()),
                "unmatched_units": sorted(key for key in bindings
                                          if key not in obligations
                                          or obligations[key] == "false"),
            })
        for record in sorted(variants):
            key = record[1]
            if key not in obligations or obligations[key] == "false":
                unmatched.append({
                    "record": list(record),
                    "reason": "undeclared" if key not in obligations else "inactive",
                })
            elif len(variants) == 1:
                admitted[key].add(rid)

    required = {key for key, trigger in obligations.items() if trigger == "true"}
    return {
        "missing": sorted(required - supplied),
        "no_admissible_record": sorted(key for key in required if not admitted[key]),
        "undetermined": sorted(key for key, trigger in obligations.items()
                               if trigger == "unknown"),
        "duplicates": sorted(key for key, ids in admitted.items() if len(ids) > 1),
        "conflicts": conflicts,
        "unmatched": unmatched,
        "unresolved": sorted(set(unresolved)),
    }


def assess(assessment_id, cutoff, snapshot, premises, trigger_basis,
           previous=None, change=None):
    """Bind a declared assessment; do not attest its truth or creation time.

    The only linked mode in this slice is a late receipt under unchanged
    declarations. A different premise set needs a distinct future design.
    These local consistency guards are not adversarial input admission.
    """
    references = {
        key: {"artifact": "premises.json#/" + key,
              "version": premises[key]["version"], "sha256": digest(premises[key])}
        for key in ("obligation_rules", "phase_profile", "identity_policy")
    }
    previous_ref = None
    original_cutoff = cutoff
    if previous is not None:
        if assessment_id == previous["assessment_id"]:
            raise ValueError("Successor must have a distinct assessment identity")
        if change is None or change["kind"] != "late_receipt":
            raise ValueError("Only the declared late_receipt supplement is modeled")
        same_context = (
            previous["references"] == references
            and previous["model_version"] == premises["model_version"]
            and previous["scope"] == premises["scope"]
            and previous["trigger_basis"] == trigger_basis
            and previous["input_snapshot"]["obligations"] == snapshot["obligations"]
            and previous["input_snapshot"]["unresolved"] == snapshot["unresolved"]
        )
        if not same_context:
            raise ValueError("Late receipt must not silently change assessment premises")
        if snapshot["records"] != previous["input_snapshot"]["records"] + change["added_records"]:
            raise ValueError("Late receipt snapshot must preserve prior records and identify additions")
        previous_ref = {"assessment_id": previous["assessment_id"],
                        "sha256": digest(previous)}
        original_cutoff = previous["original_cutoff"]
    elif change is not None:
        raise ValueError("A supplement requires its original assessment")

    return deepcopy({
        "assessment_id": assessment_id,
        "model_version": premises["model_version"],
        "scope": premises["scope"],
        "references": references,
        "original_cutoff": original_cutoff,
        "cutoff": cutoff,
        "clock_basis": "Synthetic UTC declarations; not a trusted clock",
        "trigger_basis": trigger_basis,
        "input_snapshot": snapshot,
        "input_sha256": digest(snapshot),
        "previous_assessment_ref": previous_ref,
        "change": change,
        "findings": reconcile(**snapshot),
        "provenance_status": "SUPPLIED_SYNTHETIC_DECLARATIONS_NOT_VERIFIED",
    })
