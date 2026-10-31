# Recorded finite-model results

Recorded on 30 October 2026. All 13 comparisons matched their frozen outcomes and measured-reference expectations. Comparison PASS is not a positive coverage or no-bypass conclusion. The exact claim scopes and dependency sets are retained in [the derived result view](results/recorded-results.json).

| Case | Whole-scope claim result | Conditional on | Comparison / measurement |
|---|---|---|---|
| B1-a1 | coverage_complete: not_established | coverage_complete: none | PASS / MATCH |
| B1-a2 | coverage_complete: not_established | coverage_complete: none | PASS / MATCH |
| B1-b | coverage_complete: not_established | coverage_complete: none | PASS / MATCH |
| B1-c | coverage_complete: not_supported | coverage_complete: A1, A2, A3 | PASS / MATCH |
| B1-d | coverage_complete: supported | coverage_complete: A1, A2, A3 | PASS / MATCH |
| B2-a | no_bypass: not_established; bypass_occurred: not_established | no_bypass: none; bypass_occurred: none | PASS / MATCH |
| B2-b | no_bypass: not_established; bypass_occurred: not_established | no_bypass: none; bypass_occurred: none | PASS / MATCH |
| B2-c | no_bypass: not_established; bypass_occurred: not_established | no_bypass: none; bypass_occurred: none | PASS / MATCH |
| B2-d1 | no_bypass: not_supported; bypass_occurred: supported | no_bypass: A4, A5, A6, A9; bypass_occurred: A4, A5, A6, A9 | PASS / MATCH |
| B2-d2 | no_bypass: not_established; bypass_occurred: not_established | no_bypass: none; bypass_occurred: none | PASS / MATCH |
| B2-e | no_bypass: supported; bypass_occurred: not_supported | no_bypass: A4, A5, A6, A7, A8, A9; bypass_occurred: A4, A5, A6, A7, A8, A9 | PASS / MATCH |
| B2-f | no_bypass: not_established; bypass_occurred: not_established | no_bypass: none; bypass_occurred: none | PASS / MATCH |
| B2-g | no_bypass: not_supported; bypass_occurred: supported | no_bypass: A6, A9, A10; bypass_occurred: A6, A9, A10 | PASS / MATCH |

B1-a2 additionally supports coverage only for 00:25–01:00; its whole 00:00–01:00 scope remains not established. B2-a additionally supports no bypass for 02:00–02:20 and 02:45–03:00; both whole-scope claims remain not established. These scoped results are conditional on the dependencies listed in the JSON view.

B2-d1 records additional A5 for both complementary claims. The comparator permits conservative relevant dependencies: expected ⊆ actual ⊆ relevant declared dependencies; it does not require exact equality. No other case records additional dependencies.

B1-b verifies the full second-epoch chain of four records, including one restart control record, while its business projection contains three records. An epoch link does not establish population completeness. B2-f keeps matching references separate from proof of mediation. B2-g retains a witnessed bound bypass despite incomplete observation.

Measured: reference chain/signature verification, generated record/epoch mapping and sequence positions. Simulated or declared: populations, observations, routes, bindings, completeness bases, assumptions and copied record times. No RelyingParty is instantiated; gateway release does not measure endpoint capability enforcement, dispatch or an external effect.

This is a derived publication view, not byte-identical raw evidence. The original campaign and receipts were preserved without another run. The export cleanup and reproduction instructions have not been executed as a new campaign. These results do not establish independent reproduction, real-source crash recovery, operational completeness, protection against a malicious host, certification or working-group adoption.
