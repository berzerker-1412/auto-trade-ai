---
title: "MiroFish: A Simple and Universal Swarm Intelligence Engine"
type: source
tags: [multi-agent, simulation, prediction, swarm-intelligence, AI]
sources: 1
created: 2026-04-12
updated: 2026-04-13
---

**Source:** GitHub repo `666ghj/MiroFish`
**Date clipped:** 2026-04-12

---

## Key Claims

- MiroFish accepts "seed information" (news, policy, financial signals) and automatically builds a high-fidelity parallel digital world.
- Agents in the simulated world have independent personality, long-term memory, and behavioral logic — not just rule-based bots.
- Users get a "God's-eye view" and can inject additional variables to observe different trajectories.
- Designed for both serious use (policy, PR, finance) and entertainment (extending novels).
- Powered by the [[OASIS]] framework from [[CAMEL-AI]].
- Sponsored by [[Shanda Group]] (盛大集团).

## Internal Workflow

1. **Graph Building** — pull seed, inject individual/collective memory, build GraphRAG
2. **Environment Setup** — extract entity relationships, generate personas, inject agent configs
3. **Simulation** — dual-platform parallel simulation, parse prediction requirements, update temporal memory
4. **Report Generation** — ReportAgent with toolset to interact with the post-simulation environment
5. **Deep Interaction** — chat with any agent in the simulated world or interact with ReportAgent

## Technical Stack

| Component | Technology |
| --- | --- |
| Frontend | Node.js 18+, port 3000 |
| Backend | Python 3.11–3.12, port 5001 |
| Memory | [[Zep Cloud]] (free tier sufficient for general use) |
| LLM | OpenAI-compatible API (Alibaba Qwen-plus recommended) |
| Deployment | npm dev or Docker Compose |

## Example Use Cases

- Simulating public opinion around a Wuhan University event
- Predicting the lost ending of Dream of the Red Chamber (based on the full ~100K-character text)
- Financial prediction, political news prediction (coming soon)

## Notable Quotes

> "Rehearse the future in a digital sandbox, and win decisions after countless simulations."
>
> "You only need to: Upload seed materials and describe your prediction requirements in natural language — MiroFish will return: A detailed prediction report and a deeply interactive high-fidelity digital world."

## Links to Wiki Pages

- [[MiroFish]] — entity page
- [[Swarm Intelligence]] — core concept
- [[Multi-Agent Simulation]] — simulation mechanics
- [[OASIS]] — underlying framework
- [[CAMEL-AI]] — OASIS development team
- [[Zep Cloud]] — memory backend
- [[GraphRAG]] — knowledge graph technique
