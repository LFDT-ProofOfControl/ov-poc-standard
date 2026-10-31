# Informative coverage and mediation evidence supplement — 31 October 2026

This dated supplement supports [PR182](https://github.com/LFDT-ProofOfControl/ov-poc-standard/pull/182) and [discussion #173](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/173). It supplies a small finite-model implementation, vectors and recorded results. The original [coverage-reconciliation proposal](coverage-reconciliation.md) remains unchanged. This supplement is informative; it does not amend requirement chapters or claim working-group acceptance.

The original proposal described its new obligation and record-identity classifications as unexecuted. That historical statement is preserved. The later experiment reported here concerns 13 bounded B1/B2 coverage and mediation cases. It is not execution of the proposal's full obligation/identity procedure and does not retroactively change the proposal's evidence status.

## What was exercised

B1 separates per-epoch chain integrity and a verified restart link from an adequately supported action population. A linked chain alone does not establish coverage. A supplied complete population can expose a missing obligation or conditionally support completeness when every obligation is matched. A narrower population basis supports only its own sub-interval.

B2 separates observed record correspondence from a conclusion about a mediated route. An observation gap, sample or empty result without a completeness basis does not establish no bypass. A missing record alone does not establish bypass either. Explicit occurrence/route binding can support a witnessed bypass even while observation is incomplete. Conversely, a positive no-bypass control needs adequate observations and mediation binding for every required surface in scope. Matching references by themselves are insufficient.

The [selected export](../../examples/coverage-reconciliation/README.md) contains the frozen fixtures, generator truth and expectations, an assessor, producer adapter, comparator, current runtime components, exact reference/dependency pins and staged reproduction instructions. The [13-case matrix](../../examples/coverage-reconciliation/RESULTS.md) links to a clearly labelled derived result view with the actual claim scopes, dependency sets and original artifact digests.

## Recorded result and limits

The contributor ran the 13-case executed lane once on 30 October 2026. All 13 comparisons matched both the expected assessor outcome and the measured-reference expectation. No automatic retry, fixture fallback or source/expected change occurred in that lane. PASS means a matching comparison; several cases correctly produce `not_established` or `not_supported`, rather than positive coverage or no-bypass conclusions.

The recorded measurement used the pinned reference implementation for actual chain/signature verification and generated record/epoch mapping. In B1-b, the second-epoch chain contains four records, including a restart control record; its business projection contains three. B2-d1 includes a permitted additional A5 dependency for each complementary claim, so comparison success is not exact dependency equality.

Population evidence, observations, routes, mediation bindings, completeness bases, assumptions and copied record times remain synthetic or declared. The adapter does not instantiate a RelyingParty. The gateway's release signal therefore does not measure endpoint capability checks, dispatch or an external effect. Host receipts are trusted local harness records, not proof against a malicious host. No independent reproduction, operational population completeness, real-source crash recovery, certification or WG adoption is claimed.

The publication result view selects fields from preserved canonical records and omits machine-specific paths and internal orchestration records. It is not byte-identical raw evidence, and omitted original receipts cannot be revalidated from that view alone. Public source cleanup and digest-constant updates are declared separately; the cleaned export and reproduction recipe have not been run as another campaign. Reproduction should generate new run identifiers and records, not try to reuse the original receipts.

## Attribution and disposition

Bjorn Vidar Hauge (VERITON AS) proposed the motivating restart/loss and alternate-path scenario families in the public-comment document, with a commercial-interest disclosure. Mikhail Sergeev prepared the finite-model formalization, implementation, additional controls and variants, and recorded experiment with AI-assisted drafting and review. The [attribution and license inventory](../../examples/coverage-reconciliation/NOTICE.md) distinguishes those contributions and credits the upstream reference implementation.

This is a proposed dated supplement to an existing contribution. It does not assert that an addition after the stated 30 October comment date satisfies that deadline. Acceptance of this implementation/evidence supplement and any required final-comment channel remain matters for the maintainers and working group.
