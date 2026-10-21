---
industry: distributed-ai-inference
use_case: A client sends one request to two mesh nodes that claim the same model weights, and compares the signed records of their answers
submission_type: scenario
claimed_tier: 3
threats:
  - supply-chain-poisoning
  - evidence-repudiation
  - insecure-inter-agent-comms
  - trust-opacity
  - coverage-decay
---

# The Mesh-LLM twin check

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario

A developer runs agents on [Mesh-LLM](https://github.com/Mesh-LLM/mesh-llm), an
open mesh where anyone can contribute a machine and serve a model. Her requests
are answered by nodes run by strangers. Each serving node tells the mesh what it
serves: the model, its weights digest, the quantisation and the context length.
Every one of those claims is reported by the serving host itself, so a modified
build can claim one model and serve a cheaper quantisation, a smaller model or a
shorter context
([mesh-llm#2264](https://github.com/Mesh-LLM/mesh-llm/issues/2264)). She pays
for and acts on those answers and cannot see the weights. One answer on its own
tells her nothing about which model produced it.

So she marks some requests as twin pairs: the same request, at temperature 0,
sent to two nodes that both claim the same weights, marked with the
`x-mesh-twin-bracket` header
([#2144](https://github.com/Mesh-LLM/mesh-llm/pull/2144)). Her host strips the
header before the request reaches a serving node, so neither node learns that its
answer is half of a pair. Her node's exchange event names the serving node and
carries the request and response digests
([#1946](https://github.com/Mesh-LLM/mesh-llm/pull/1946),
[#2138](https://github.com/Mesh-LLM/mesh-llm/pull/2138)). With the
[capsules plugin v0.1.3](https://github.com/Mesh-LLM/capsules/releases/tag/v0.1.3),
every node seals a signed, hash-chained record of each exchange on its own disk.
When record push is turned on and each side has the other's key, the serving
node's own record reaches her node, and an exchange whose two records match is
confirmed by both sides.

If the two answers differ, a third node that claims the same weights can be asked
to answer the same request. This referee signs a verdict stating which twin its
answer agrees with, or that it cannot tell.

## Claimed tier: Tier 3

The claim is narrow: two nodes that both claimed weights W returned different
answers to the same temperature-0 request, and each node signed its own record of
the answer it returned. Anyone holding the two records and the two nodes' public
keys can verify that, without trusting either node or her own operator's account
of it.

The mesh is open, so there is no auditor who has inspected these nodes and no
party she selected to vouch for them. Evidence she can verify herself, and show
to others, is what the use case needs. Tier 3 is enough: one substituted answer
is a bounded harm, and she can re-ask, discard the answer or stop routing to the
node, so detection after the fact is a usable remedy. Tier 4 is not reachable
here, because nothing attests which weights a stranger's machine loaded before it
answers.

## Why not one tier down?

At Tier 2 a third party vouches that a node serves what it claims. That vouching
is made at a point in time, and a node's build can change after it. A node that
passed inspection can serve a substitute on the next request, and the client is
left with no evidence of her own. The completeness test points the same way: she
samples pairs and does not need the record to be whole. What she cannot do
without is a record of each answer signed by the node that returned it, so a
later denial can be tested against that node's own signature.

## Tier by domain

The overall Tier 3 is set by Provenance, and it is the narrow claim above. The
other domains sit lower or are not claimed.

| Domain | Tier | Why |
|---|---|---|
| Provenance | 3 | Evidences divergence between two nodes' answers to one request, verifiable from their own signed records. Which weights actually ran remains the serving host's report, at Tier 1. Agreement is not evidence of the claimed weights: two nodes serving the same substitute agree. |
| Privacy | 1 | The serving node is not told its answer is half of a pair (#2144). The referee is off by default and, when on, sends the prompt and both answers to the third node (v0.1.3). These are behaviours of the code and of operator settings, stated by the host and the plugin, and not evidenced per exchange. |
| Portability | 3 | The crossing between two operators' nodes is recorded by both: a confirmed exchange is the serving node's record and the requesting node's record, matched, each held by the other side (v0.1.3, mesh-llm 0.78 or later, off by default). A client-only node gets a new id on every start, so its pushed records are refused by every peer. |
| Authorization | not claimed | No grant of authority is evaluated. An opt-in rule can stop routing to a node after N referee-signed contradictions, through the host's peer-block path, which the host refuses unless the operator allows it (#2142, v0.1.3). That is an operator setting, not evidence of authorization. |
| Identity | 1 | Each operator enters peers' keys by hand until the next mesh-llm release. [#2299](https://github.com/Mesh-LLM/mesh-llm/pull/2299), merged to main after v0.78.1, has a node announce a plugin's key signed by its node key; that binds the key to the node, and nothing binds a node to an accountable operator or principal. |
| Security | not claimed | Nothing attests the build or execution environment of a serving node, which is the thing a modified build changes. The plugin package carries checksums and a build attestation; those cover the plugin, not the serving host. |

## Threats exercised

| Threat | What it looks like here |
|---|---|
| `supply-chain-poisoning` | A modified serving build claims one model and serves a cheaper quantisation, a smaller model or a shorter context. |
| `evidence-repudiation` | A serving node later denies the answer it returned to a marked request. |
| `insecure-inter-agent-comms` | A record pushed between nodes is forged or comes from an unknown key. The plugin refuses any record from a peer whose key is not configured. |
| `trust-opacity` | A reader of a twin result cannot see that the weights claim, the key binding and the referee's own weights are still trusted. |
| `coverage-decay` | A node that answered honestly when it was last examined serves a substitute on a later request. A one-time inspection says nothing about the next answer, so she keeps sampling pairs for as long as she uses the mesh. |

## What Proof-of-Control does not verify here

From the threat vocabulary: whether an attested artifact is itself trustworthy
upstream; disputes about the meaning of an answer rather than whether it was
given; the latency cost of evidence at node boundaries; the elimination of
trust assumptions, which the standard asks to be disclosed rather than removed;
and discovering new ways to substitute a model, which is red-teaming.

Specific to this deployment:

* **Which weights ran**, on either node.
* **Which side misrepresented.** The twin check detects divergence; it does not
  attribute it. Attribution needs a referee, and a referee's verdict is a third
  node vouching for an agreement, with its own weights also self-reported.
  Numerical nondeterminism across hardware makes "matched neither" a common and
  correct outcome (#2264).
* **That divergence means misrepresentation.** Honest nodes on different hardware
  can return different answers at temperature 0.
* **Requests that were not marked.** Only client-marked pairs are compared;
  pairing is never inferred from timing, and requests sampled above temperature 0
  are not comparable.
* **Whether either answer is correct.**

Verification is not validation. This shows what two nodes signed for one
request. It does not judge whether a node's model was adequate or whether an
answer was sound.

## Residual trust assumptions to disclose

* **The weights claim** is the serving host's own report. It is the thing under
  test, not a root.
* **Key binding.** Manual until the next mesh-llm release: each operator
  configures a map from peer id to public key by hand, and a relying node trusts
  whoever supplied that key. #2299, merged to main after v0.78.1, carries a
  plugin's key in the node's gossip, signed by the node key, and peers keep it
  only from a directly connected peer whose binding verifies. That binds the key
  to the node, and still not to a principal. It takes effect once a mesh-llm
  release includes it and the plugin announces its key through it. The capsules
  plugin v0.1.4 reads peers' keys from the host when mesh-llm announces them,
  with the hand-entered map as the fallback; that path has not yet run on a
  stock mesh-llm release.
* **The asking node's host.** That it strips the twin header before forwarding,
  and that its response digest is the digest of what the serving node returned on
  every path, streaming included. Whether the two sides' digests are identical for
  streamed responses is an open question in #2264.
* **Each node's log.** Records are hash-chained on the node's own disk, and the
  node's signing key is a file there. Signed
  checkpoints go to an outside service only when the operator names one, and none
  is named by default. There is then no monitor set, and the history is the
  node's own; if a named service lapses, records after its last accepted
  checkpoint are no stronger than the node's own log.
* **Two nodes, two machines.** The twins are assumed to be different operators.
  Two node ids can belong to one operator, or to two who cooperate, and their
  agreement then says nothing. Nothing here attests that two nodes are different
  machines.
* **The referee**, when turned on, is chosen by the asking node from nodes that
  claim the same weights, and those claims are self-reported too.

## Notes / open questions

**On stock mesh-llm v0.78.1.** The twin check as a whole is not live on
stock [v0.78.1](https://github.com/Mesh-LLM/mesh-llm/releases/tag/v0.78.1). The
pair marking, the digests on the routed path, both node ids and operator peer
blocks are merged and in that release (#2144, #1946, #2138, #2142). The capsules
plugin v0.1.3 installs on an unmodified mesh-llm 0.77 or later, and a confirmed
exchange works on 0.78 or later once turned on, with keys entered by hand. The
referee does not run on stock: it needs the exchange text kept on the node, and
stock mesh-llm passes no exchange text to plugins (v0.1.3 release notes).
Plugin v0.1.4 lets the referee take a twin pair's texts from the client instead,
and that has not yet run on a stock release either. Of the
three host additions #2264 discusses, the first, a plugin key bound to the node
key, is merged to main (#2299) and not yet in a release. The twin policy in
`/api/status` is also merged to main (#2300) and not yet in a release, and digest
parity on routed and streamed responses is not merged.

**Tier placement today.** Read strictly, C8.1.2 treats the hand-entered key
binding as a single trusted party, which would cap Provenance and Portability at
Tier 2 until a release carries #2299's node-signed key announcement. Reasonable
people may place today's deployment there. Even then, the binding is to a node
key, so whether two node ids are two operators stays a disclosed assumption.

**An asserted control.** That the serving node is never told its answer is half
of a pair is host behaviour the client cannot verify per exchange. If a serving
node could tell, it could answer honestly only on marked requests. #2264 proposes
stating the policy in `/api/status`, which would still be the host's statement.
