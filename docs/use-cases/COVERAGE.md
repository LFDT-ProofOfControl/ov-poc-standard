# Coverage index

**29 of 29 threats have a worked use case.** 17 submissions.

Generated from the `threats:` frontmatter across this folder. Do not
edit by hand: run `python3 tools/generate_use_case_coverage.py`.

## By family

| Family | Covered | |
|---|---|---|
| Instruction and goal manipulation | 3/3 | `████████████████████` |
| Memory, knowledge, and supply chain | 4/4 | `████████████████████` |
| Identity, authority, and inter-agent trust | 4/4 | `████████████████████` |
| Tools, actions, and effects | 4/4 | `████████████████████` |
| Data exposure | 1/1 | `████████████████████` |
| Autonomy, drift, and lifecycle | 3/3 | `████████████████████` |
| Record integrity and resilience | 5/5 | `████████████████████` |
| Human oversight and disclosure | 2/2 | `████████████████████` |
| Output quality and availability | 3/3 | `████████████████████` |

## Every threat

| Family | Threat | Use cases |
|---|---|---|
| Instruction and goal manipulation | `prompt-injection` | `ai-assisted-legal-filing`, `ai-assisted-public-emergency-alert` |
| Instruction and goal manipulation | `bent-goals` | `ai-assisted-public-emergency-alert` |
| Instruction and goal manipulation | `system-prompt-leakage` | `ai-assisted-public-emergency-alert` |
| Memory, knowledge, and supply chain | `memory-poisoning` | `ai-assisted-clinical-infusion-instruction` |
| Memory, knowledge, and supply chain | `rag-weakness` | `ai-assisted-clinical-infusion-instruction`, `ai-assisted-legal-filing` |
| Memory, knowledge, and supply chain | `model-poisoning` | `credit-decisioning` |
| Memory, knowledge, and supply chain | `supply-chain-poisoning` | `credit-decisioning`, `frontier-lab-agent-collective`, `privileged-software-change` |
| Identity, authority, and inter-agent trust | `identity-abuse` | `account-takeover-stolen-credentials`, `agentic-cross-border-payments`, `ai-assisted-clinical-infusion-instruction`, `credit-decisioning`, `deepfake-biometric`, `deepfake-interview-insider`, `frontier-lab-agent-collective`, `license-piracy-agent`, `pig-butchering`, `privileged-software-change` |
| Identity, authority, and inter-agent trust | `context-blind-authorization` | `agent-exceeds-principal-clearance`, `agentic-cross-border-payments`, `ai-assisted-clinical-infusion-instruction`, `ai-assisted-legal-filing`, `frontier-lab-agent-collective`, `privileged-software-change`, `provider-replacement-live-mandate`, `rogue-internal-agent-pii` |
| Identity, authority, and inter-agent trust | `excessive-agency` | `account-takeover-stolen-credentials`, `agent-exceeds-principal-clearance`, `agentic-cross-border-payments`, `deepfake-interview-insider`, `frontier-lab-agent-collective`, `privileged-software-change`, `provider-replacement-live-mandate`, `rogue-internal-agent-pii`, `shopping-agent` |
| Identity, authority, and inter-agent trust | `insecure-inter-agent-comms` | `agentic-cross-border-payments`, `frontier-lab-agent-collective` |
| Tools, actions, and effects | `tool-misuse` | `agentic-cross-border-payments`, `license-piracy-agent` |
| Tools, actions, and effects | `unexpected-code-execution` | `frontier-lab-agent-collective` |
| Tools, actions, and effects | `unsafe-actuation` | `ai-assisted-clinical-infusion-instruction` |
| Tools, actions, and effects | `improper-output-handling` | `ai-assisted-clinical-infusion-instruction`, `ai-assisted-legal-filing`, `ai-assisted-public-emergency-alert` |
| Data exposure | `data-exfiltration` | `account-takeover-stolen-credentials`, `agent-exceeds-principal-clearance`, `credit-decisioning`, `frontier-lab-agent-collective`, `rogue-internal-agent-pii` |
| Autonomy, drift, and lifecycle | `autonomy-creep` | `agentic-cross-border-payments`, `shopping-agent` |
| Autonomy, drift, and lifecycle | `behavioral-drift` | `credit-decisioning`, `frontier-lab-agent-collective` |
| Autonomy, drift, and lifecycle | `scope-creep-lifecycle` | `credit-decisioning`, `deepfake-interview-insider`, `privileged-software-change` |
| Record integrity and resilience | `audit-tampering` | `agentic-cross-border-payments`, `frontier-lab-agent-collective`, `privileged-software-change`, `rogue-internal-agent-pii` |
| Record integrity and resilience | `cascading-failure` | `privileged-software-change` |
| Record integrity and resilience | `coverage-decay` | `ai-assisted-public-emergency-alert` |
| Record integrity and resilience | `evidence-repudiation` | `agentic-cross-border-payments`, `ai-assisted-clinical-infusion-instruction`, `ai-assisted-legal-filing`, `ai-assisted-public-emergency-alert`, `credit-decisioning`, `deepfake-biometric`, `frontier-lab-agent-collective`, `privileged-software-change`, `provider-replacement-live-mandate`, `rogue-internal-agent-pii`, `shopping-agent` |
| Record integrity and resilience | `trust-opacity` | `account-takeover-stolen-credentials`, `deepfake-interview-insider`, `pig-butchering` |
| Human oversight and disclosure | `approval-fatigue` | `deepfake-biometric`, `pig-butchering` |
| Human oversight and disclosure | `undisclosed-ai` | `license-piracy-agent`, `pig-butchering` |
| Output quality and availability | `misinformation` | `ai-assisted-clinical-infusion-instruction`, `ai-assisted-legal-filing`, `ai-assisted-public-emergency-alert` |
| Output quality and availability | `hidden-bias` | `credit-decisioning` |
| Output quality and availability | `unbounded-consumption` | `shopping-agent` |

## Every use case

| Use case | Threats tagged |
|---|---|
| `account-takeover-stolen-credentials` | `identity-abuse`, `excessive-agency`, `data-exfiltration`, `trust-opacity` |
| `agent-exceeds-principal-clearance` | `excessive-agency`, `context-blind-authorization`, `data-exfiltration` |
| `agentic-cross-border-payments` | `context-blind-authorization`, `excessive-agency`, `identity-abuse`, `tool-misuse`, `insecure-inter-agent-comms`, `autonomy-creep`, `audit-tampering`, `evidence-repudiation` |
| `ai-assisted-clinical-infusion-instruction` | `memory-poisoning`, `rag-weakness`, `unsafe-actuation`, `improper-output-handling`, `misinformation`, `context-blind-authorization`, `identity-abuse`, `evidence-repudiation` |
| `ai-assisted-legal-filing` | `prompt-injection`, `rag-weakness`, `improper-output-handling`, `misinformation`, `context-blind-authorization`, `evidence-repudiation` |
| `ai-assisted-public-emergency-alert` | `prompt-injection`, `bent-goals`, `system-prompt-leakage`, `improper-output-handling`, `coverage-decay`, `misinformation`, `evidence-repudiation` |
| `credit-decisioning` | `model-poisoning`, `supply-chain-poisoning`, `scope-creep-lifecycle`, `behavioral-drift`, `identity-abuse`, `data-exfiltration`, `hidden-bias`, `evidence-repudiation` |
| `deepfake-biometric` | `identity-abuse`, `approval-fatigue`, `evidence-repudiation` |
| `deepfake-interview-insider` | `identity-abuse`, `excessive-agency`, `scope-creep-lifecycle`, `trust-opacity` |
| `frontier-lab-agent-collective` | `insecure-inter-agent-comms`, `audit-tampering`, `excessive-agency`, `context-blind-authorization`, `identity-abuse`, `unexpected-code-execution`, `data-exfiltration`, `supply-chain-poisoning`, `behavioral-drift`, `evidence-repudiation` |
| `license-piracy-agent` | `identity-abuse`, `tool-misuse`, `undisclosed-ai` |
| `pig-butchering` | `identity-abuse`, `approval-fatigue`, `undisclosed-ai`, `trust-opacity` |
| `privileged-software-change` | `supply-chain-poisoning`, `identity-abuse`, `context-blind-authorization`, `excessive-agency`, `scope-creep-lifecycle`, `audit-tampering`, `cascading-failure`, `evidence-repudiation` |
| `provider-replacement-live-mandate` | `context-blind-authorization`, `excessive-agency`, `evidence-repudiation` |
| `rogue-internal-agent-pii` | `excessive-agency`, `context-blind-authorization`, `data-exfiltration`, `audit-tampering`, `evidence-repudiation` |
| `shopping-agent` | `excessive-agency`, `autonomy-creep`, `unbounded-consumption`, `evidence-repudiation` |
| `sovereign-agents` | **none tagged** |
