# Use cases (informative)

***This section answers:*** *What does it look like in practice? Worked use cases that
exercise the six domains, the Verifiability Tiers, and the System surface against real
deployments.*

This folder holds worked stories that show how a deployment maps onto the six
verification domains ([C1 to C6](../../0.1/en/0x10-C01-Provenance.md)) and the four
Verifiability Tiers ([C8](../../0.1/en/0x10-C08-Verifiability-Tiers.md)). They are
calibration material. They carry no normative force, and they are the fastest way to
see how a Proof-of-Control claim is made and how an evaluator reads one.

Each use case states not only what Proof-of-Control verifies but what it does not
verify in that deployment (for example, that a sanctions list was correctly compiled,
or that a consent record was validly obtained). That keeps the verification-not-validation
boundary concrete against real examples.

## Use cases in this folder

| File | Industry | Type | Tier |
|---|---|---|---|
| [`credit-decisioning.md`](credit-decisioning.md) | Consumer lending | Scenario | 4 |

A further worked use case, Proof-of-Control for the Universal Commerce Protocol,
adapts Ken Huang's UCP assurance framework and exercises the six domains, the System
surface ([C9](../../0.1/en/0x10-C09-System-Surface-MAESTRO.md)), and the Verifiability
Tiers against a live agentic-commerce protocol. It lives in the companion demo document,
"UCP PoC Demo", and is not yet ported to this folder. <!--aais-allow-->

## The six domains

Provenance, Privacy, Portability, Authorization, Identity, Security.

## The four Verifiability Tiers

| Tier | Name | What it means |
|---|---|---|
| 1 | Assertion | The operator's word. Model cards, self-reported benchmarks. |
| 2 | Attestation | A third party vouches. External evaluations, red-teaming. |
| 3 | Trust-minimized | Anyone can verify; the parties its soundness rests on are disclosed rather than removed. |
| 4 | Self-enforcing | The action cannot run without producing evidence. Verification is enforced at serving time, and unverified actions are refused. |

Tiers 1 and 2 both ask you to trust a party. Tiers 3 and 4 do not. That
boundary is the one a claim turns on.

Two properties separate Tier 3 from Tier 4. At Tier 3 you can verify that the
records you hold were not altered, and you are not guaranteed the record is
whole. At Tier 4 an action cannot execute without producing evidence, so the
absence of evidence means the action did not happen.

## How a tier is set

The overall tier is the highest bar the domains that carry the most risk for
that use case demand, rather than an average across all six. A low tier on a
domain that carries no risk in this deployment is a correct answer.

Tiers are ordinal and tied to their justification. The reasoning matters more
than the number.

## Two submission types

**Scenario.** A hypothetical deployment, written for calibration. This is the
default. Keep the disclaimer line and do not describe any real organization's
actual current state.

**Incident.** A documented event with primary sources, where the facts are
published by the parties involved or by an investigator granted access. An
incident submission argues about the tier the deployment was operating at and
the tier its risky domains demanded, rather than a tier being claimed for a
system.

An incident submission carries a higher bar. Every material fact needs a
citation to a primary source, and where the sources disagree or leave a gap,
say so rather than filling it.

## Threat tagging

Every submission tags the threats its deployment exercises, using the slugs in
[THREATS.md](THREATS.md). Tagging does two things: it lets us maintain a
coverage index showing which threats have a worked use case and which have
none, and it gives you the source material for the "What Proof-of-Control does
not verify here" section, which comes from the out-of-scope column of the
threat vocabulary.

## To contribute

Two ways, depending on how you work.

**In your browser, with no git.** Open
[`_TEMPLATE.md`](_TEMPLATE.md), click **Raw**, and copy everything. Come back to
this folder, click **Add file** and then **Create new file**. GitHub forks the
repository for you at that point. Name the file a descriptive slug ending in
`.md`, paste the template in, fill it out, and click **Propose new file** to open
a pull request.

**With git.** Fork the repository, clone your fork, create a branch, copy
`_TEMPLATE.md` to a descriptive slug, fill it out, push, and open a pull request
from your fork.

Either way:

1. Replace every value in the frontmatter, including `threats`.
2. Replace every italic prompt with your own text, and delete the prompts.
3. Delete the HTML comment at the top of the file.
4. Complete every section, including the argument for why one tier down would
   not do.
5. One scenario or one incident per file.

### Filling in an incident submission

An incident replaces three things in the template. The frontmatter carries
`submission_type: incident`, `observed_tier` and `required_tier` in place of
`claimed_tier`, and a required `sources:` list with primary sources first. The
disclaimer becomes *"Documented incident. Facts are drawn from the sources
listed in the frontmatter."* And the single "Claimed tier" heading becomes two:
**Tier observed** and **Tier the risky domains demanded**.

### The two tests in "Why not one tier down?"

**Reversibility.** Can the harm be undone once you detect it? Money that has
settled, data that has been disclosed and a border that has been crossed are all
final. Where detection after the fact is not a remedy, the argument for Tier 4 is
that enforcement has to refuse the action rather than report it.

**Completeness.** At Tier 3 you can verify that the records you hold were not
altered, and you are not guaranteed the record is whole: an agent can act
off-record, and the absence of a record tells you nothing. At Tier 4 the action
cannot execute without producing evidence, so absence of evidence means the
action did not happen.

## Coverage

<!-- coverage:start -->
**Coverage: 3 of 29 threats** across 2 use cases. `███░░░░░░░░░░░░░░░░░░░░░░░░░`  
Full index in [COVERAGE.md](COVERAGE.md).
<!-- coverage:end -->

`COVERAGE.md` is generated from the `threats:` frontmatter across this
folder and shows which threats have a worked use case. Threats with no
coverage are where a submission helps most.

After merging a submission, run `python3 tools/generate_use_case_coverage.py`
from the repository root. Continuous integration runs the same script with
`--check`, which fails if the index has drifted from the submissions. Do not edit
`COVERAGE.md` or the coverage block above by hand.

*To contribute a use case from your sector, join a working group at
[advancedaisociety.org](https://advancedaisociety.org/).*

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*
