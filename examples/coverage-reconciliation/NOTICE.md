# Attribution and license inventory

Mikhail Sergeev prepared the finite-model formalization, controls and variants, implementation, recorded experiment and publication supplement with AI-assisted drafting and review. The experiment is a contributor-run use of the public reference implementation, not an independent reproduction.

Bjorn Vidar Hauge (VERITON AS) suggested the two motivating scenario families in the [Proof-of-Control public-comment document](https://docs.google.com/document/d/1EiiGDwLXvMxoSHp3Ru56AhR2u9gNd-6Fjs_CKZ4kU-w/edit): loss before a writer followed by restart, and an alternate path with an observation gap. His source comment disclosed a commercial interest and proposed tests; it did not report these executed results. B1-a1/B1-b and B2-a formalize those motivating ideas. B1-a2, B2-b/B2-c/B2-d2/B2-f/B2-g are bounded contributor variants. B1-c/B1-d and B2-d1/B2-e are additional contributor controls. These additions and conclusions are not attributed to Bjorn or presented as his endorsement.

The [reference implementation](https://github.com/LFDT-ProofOfControl/ov-poc-standard/tree/93d0e282fc177d5df741de4cdd6a0d0dacf1955a/impl) is from Advanced AI Society and the Proof-of-Control contributors. Its repository declares Apache-2.0. No reference source is vendored here. The adapter mirrors the construction in `impl/attacks/run_attacks.py:build`, with a grant that also permits `source.restart`, and uses the pinned public implementation for generation and verification. It adds finite-model record mapping and measurement output; it does not add a RelyingParty or implement endpoint dispatch. Applicable upstream attribution is retained here. The pinned tree has no separate implementation NOTICE file.

This supplement and selected export are prepared for contribution under Apache-2.0, consistent with [upstream contribution terms](https://github.com/LFDT-ProofOfControl/ov-poc-standard/blob/93d0e282fc177d5df741de4cdd6a0d0dacf1955a/CONTRIBUTING.md). See the full [license](LICENSE). Source changes for publication are listed in PROVENANCE.json. The original code, vectors and experimental records are preserved by the contributor. Trademarks and certification claims are not granted by this example.

No interpreter, dependency wheel, installed package or image payload is distributed. The exact recorded producer dependencies are listed below; metadata pins and the target-specific wheel set are in dependencies.json.

| Dependency | Version | License expression from official release metadata |
|---|---|---|
| [cryptography](https://pypi.org/pypi/cryptography/50.0.2/json) | 50.0.2 | Apache-2.0 OR BSD-3-Clause |
| [cffi](https://pypi.org/pypi/cffi/2.1.1/json) | 2.1.1 | MIT-0 |
| [pycparser](https://pypi.org/pypi/pycparser/3.12/json) | 3.12 | BSD-3-Clause |

These are dependency metadata declarations, not a license audit of redistributed wheels or of all their bundled components. A redistributor who chooses to vendor dependencies or the reference implementation must review those payloads and their notices separately. The export contains no such payloads.
