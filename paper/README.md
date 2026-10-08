# The Proof-of-Control Research Paper

> ## 📄 [Read the paper (PDF)](main.pdf)
>
> Click the link above, then use the **Download** button at the top right of the viewer.
> Or [download it directly](https://github.com/LFDT-ProofOfControl/ov-poc-standard/raw/master/paper/main.pdf) in one click.

*Proof-of-Control: An Open Standard for Runtime Verifiability and Cryptographic Oversight in
Autonomous AI Execution* — Jim Schwoebel, Tricia Wang, Ken Huang.

**Status: working draft, open for review.** Not yet submitted.

## What this paper is

AI agents act faster than any person can watch, and the only account of what they did usually
comes from the system being asked. The [Proof-of-Control Standard](../README.md) answers that
with tamper-evident evidence anyone can openly verify, without trusting the operator: open
verification, where the root of trust is a mechanism anyone can verify, not a party anyone
must believe. The standard grades that
evidence on four [Verifiability Tiers](../0.1/en/0x10-C08-Verifiability-Tiers.md), and
Proof-of-Control is evidence at Verifiability Tiers 3 and 4 only. This paper is the
research behind the standard: we built the evidence pipeline the standard describes, attacked
it, and measured what it costs, on real confidential-computing hardware. It is written to
bridge AI-safety research into enterprise cybersecurity, in plain language, with every claim
tied to a measurement or a theorem.

**How it relates to the standard.** The two complement each other. The specification in this
repository ([`0.1/en/`](../0.1/en), also readable as a
[Google Doc working draft](https://docs.google.com/document/d/1EiiGDwLXvMxoSHp3Ru56AhR2u9gNd-6Fjs_CKZ4kU-w/edit))
is the normative text: the requirements an implementation must meet. The paper is the evidence
for it: why those requirements exist, what happens when they are missing, and what meeting them
costs. The repository remains the source of truth for the standard's text.

## The experiments we ran

Every experiment answers the same question about the
[Verifiability Tiers](../0.1/en/0x10-C08-Verifiability-Tiers.md): can evidence at
Verifiability Tier 3 (Trust-minimized) and Verifiability Tier 4 (Self-enforcing) — the only
two Tiers that count as Proof-of-Control, and the demonstration that open verification works —
be produced at machine speed, at a cost a deployment can carry? Everything in Section 9
("Does It Actually Work?") comes from the open reference implementation in
[`../impl/`](../impl/README.md), and every number can be regenerated from it.

* **We built the whole pipeline and timed it.** Interception, signing, hash-chaining,
  path-aware policy evaluation, capability tickets, anchoring, gossip, and fail-closed
  behavior: about 201 µs per intercepted step on a laptop, 160 µs inside a real Intel TDX
  trust domain — roughly 1% of a 15 ms per-action budget. The fail-closed gate is the
  Verifiability Tier 4 property: verification gates operation, and an action without evidence
  does not run.
* **We attacked it.** Eleven attacks, from log rewriting to privilege escalation through
  composed calls, each run with and without the requirement derived from it. All eleven
  succeed without the requirements and are refused or detected with them.
* **We measured real confidential hardware.** Running inside the trust domain costs 5.1%
  against an identical control instance, but one hardware attestation quote costs 39.5 ms,
  so per-action attestation is impossible and every deployment must amortize — which became
  requirements C7.2.3 and C7.2.4 of the standard. This is Verifiability Tier 3 evidence:
  produced by the mechanism itself, verifiable with published tools, with the parties it rests
  on disclosed rather than removed.
* **We checked it stays cheap.** Policy evaluation stays flat from 10 to 50,000 steps, where
  naive re-evaluation grows linearly.
* **We measured what an auditor pays.** Merkle inclusion proofs turn a 123 MB chain download
  into a 544-byte proof for verifying a single action.
* **We ran 2,000 randomized workflows** (70% ordinary work, 30% probing the boundaries) to
  measure how much legitimate work verification refuses — and found the result we did not
  expect: a monitor that watches the whole path refuses 42% of legitimate work unless the
  policy gives it an explicit declassification point.
* **We compared post-quantum signatures**, chose the anchoring interval by measurement, and
  measured the batching that removes most of the signing cost.

The paper also states what is *not* shown — Section 10, "What We Still Do Not Know," lists the
open problems in the authors' own words.

## How to contribute

We want this to work for people who use GitHub and people who do not. Pick whichever path
suits you:

1. **Join a research meeting.** We hold two research meetings during October to work on the
   paper together; times are posted in the Slack channel below.
2. **Discuss it in Slack.** New to our Slack?
   [Join here](https://join.slack.com/t/advancedaisoc-kxy6033/shared_invite/zt-4bl8klaav-E1CMLj0N3kG_fF3jwEnHuQ),
   then open the `#proof-of-control-paper`
   [channel](https://advancedaisoc-kxy6033.slack.com/archives/C0C7MKS5E3U) — it exists for
   exactly this conversation.
3. **Send a pull request.** The preferred route: send edits as a pull request against
   `paper/main.tex`, or open an
   [issue](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues) with your comments.
   Jim Schwoebel maintains the paper: pull requests come to him, and he rebuilds the committed
   PDF from the merged source. We discuss every comment at the research meetings.
4. **Email the maintainer.** Send comments to Jim Schwoebel, the paper's technical
   maintainer, at [jim@advancedaisociety.org](mailto:jim@advancedaisociety.org), and we will
   fold them into the review.

**On authorship.** We welcome as many reviewers as the paper can earn. The minimum for
co-authorship is that you reviewed the manuscript. Authorship can look like a review or
comments or rewrite suggestions. We will work through comments together in the October
meetings, in Slack, or by email.

## Build

```bash
./tools/build_paper_figures.sh      # from the repo root; requires rsvg-convert
cd paper
tectonic -Z shell-escape main.tex   # shell-escape needed for minted (pygments)
```

Output: `main.pdf` (a compiled copy is committed so readers can download the paper without
building it). Contributors send source changes, not rebuilt PDFs: the maintainer rebuilds
`main.pdf` after merging.

**Prose style.** The paper is written in the plain, concrete, direct manner associated with
Richard Feynman's expository writing: examples before abstractions, ordinary words for technical
things, and explicit statements of what is *not* known or claimed. All technical content —
theorems, proofs, tables, measurements, citations — is unchanged; only the prose style
differs. Section titles are plain declaratives ("The Problem", "Does It Actually Work?",
"What We Still Do Not Know").

## Before Submission — Required Steps

1. **Co-author consent.** The author list is limited to those who have reviewed the manuscript
   and consented to authorship: currently Jim Schwoebel, Tricia Wang, and Ken Huang. We will
   add all co-authors after reviewing the draft and consenting.
2. **Citation verification.** Entries in `references.bib` marked `[verify]` (Bandara et al.
   AI Trust OS, Chen et al. TraceSafe-Bench, Xie et al. SCR-Bench, Web 7.0 Verifiable Trust
   Circles, Catena-X AI Service KIT, MindXO KRI, and the arXiv:2603.16586 author list) carry
   metadata reported in secondary sources — confirm against the primary literature and fill
   in full author lists, venues, and identifiers.
3. **Numbers refresh.** The requirement count (111), threat count (32), and coverage table
   are generated from the specification repository. Re-run
   `python3 mappings/compute_coverage.py` and `python3 tools/generate_checklist.py` and update
   Section 7 / the abstract if the working group changes the requirement set.
4. **arXiv metadata.** Suggested categories: cs.CR (primary), cs.AI, cs.SE. License: CC BY 4.0
   to match the specification.

## Files

| File | Purpose |
| --- | --- |
| [`main.pdf`](main.pdf) | **The paper — download this to read it** |
| `main.tex` | The paper's LaTeX source (compiles with tectonic, XeTeX engine) |
| `references.bib` | Complete bibliography: RFCs, NIST/ISO/EU documents, frameworks, and the 2026 research corpus |
| `figures/aai-logo.png` | Advanced AI Society logo asset (reference; the cover uses the brand-kit lockup) |
| `figures/*.pdf` | Paper figures, built from the repo's SVGs. They are gitignored build output — regenerate all of them with `./tools/build_paper_figures.sh` from the repository root, which also re-runs the diagram and chart generators so a stale figure cannot outlive a data change. |
