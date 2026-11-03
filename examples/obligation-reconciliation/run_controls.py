"""Compare supplied frozen expectations; emit all outcomes. See PROVENANCE.md."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

from reconcile import assess, reconcile, serialized


def run_controls():
    root = Path(__file__).resolve().parent
    fixtures = json.loads((root / "controls.json").read_text())
    premises = json.loads((root / "premises.json").read_text())
    rows = []
    for case in fixtures["cases"]:
        snapshot = deepcopy(case["input"])
        actual = reconcile(**snapshot)
        checks = {"expected_findings": actual == case["expected"],
                  "input_unchanged": snapshot == case["input"]}
        rows.append({"case": case["case"], "actual": actual,
                     "expected": case["expected"], "checks": checks,
                     "comparison": "PASS" if all(checks.values()) else "FAIL"})

    # The two explicitly supplied snapshot states above are distinct from A0/A1.
    # Reconciliation must leave each state untouched; no late-arrival claim follows.
    linked = fixtures["linked"]
    original_input = deepcopy(linked["initial"]["input"])
    later_input = deepcopy(linked["successor"]["input"])
    original = assess(linked["initial"]["assessment_id"], linked["initial"]["cutoff"],
                      original_input, premises, linked["trigger_basis"])
    original_bytes = serialized(original)
    original_copy = deepcopy(original)
    later = assess(linked["successor"]["assessment_id"], linked["successor"]["cutoff"],
                   later_input, premises, linked["trigger_basis"],
                   previous=original, change=linked["change"])
    checks = {
        "original_expected": original["findings"] == linked["initial"]["expected"],
        "successor_expected": later["findings"] == linked["successor"]["expected"],
        "original_bytes_unchanged": serialized(original) == original_bytes,
        "original_object_unchanged": original == original_copy,
        "input_objects_unchanged": (original_input == linked["initial"]["input"]
                                    and later_input == linked["successor"]["input"]),
        "separate_identity": original["assessment_id"] != later["assessment_id"],
        "previous_link_exact": later["previous_assessment_ref"] == {
            "assessment_id": linked["initial"]["assessment_id"],
            "sha256": hashlib.sha256(original_bytes).hexdigest()},
        "original_cutoff_preserved": (original["original_cutoff"] == linked["initial"]["cutoff"]
                                      == later["original_cutoff"]),
        "current_cutoffs_retained": (original["cutoff"] == linked["initial"]["cutoff"]
                                     and later["cutoff"] == linked["successor"]["cutoff"]),
        "same_premises_and_trigger_basis": (original["references"] == later["references"]
                                            and original["trigger_basis"] == later["trigger_basis"]),
        "snapshot_bindings_exact": all(a["input_sha256"] == hashlib.sha256(
            serialized(a["input_snapshot"])).hexdigest() for a in [original, later]),
        "added_evidence_retained": later["change"] == linked["change"],
        "outcomes_remain_unresolved": (original["findings"]["unresolved"]
                                       == later["findings"]["unresolved"]
                                       == linked["initial"]["expected"]["unresolved"]),
        "references_bind_included_premise_bytes": all(
            ref["sha256"] == hashlib.sha256(serialized(premises[key])).hexdigest()
            and ref["version"] == premises[key]["version"]
            for key, ref in original["references"].items()),
    }
    rows.append({"case": linked["case"], "original": original, "successor": later,
                 "checks": checks, "comparison": "PASS" if all(checks.values()) else "FAIL"})
    return {"schema": "obligation-reconciliation-results/1", "cases": rows,
            "passed": sum(row["comparison"] == "PASS" for row in rows),
            "failed": sum(row["comparison"] == "FAIL" for row in rows),
            "scope": "18 synthetic controls; contributor-authored expectations; no full proposal coverage"}


if __name__ == "__main__":
    result = run_controls()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(1 if result["failed"] else 0)
