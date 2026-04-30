---
title: Swarm Intelligence
type: concept
tags: [AI, collective-behavior, emergence, simulation]
sources: 1
created: 2026-04-12
updated: 2026-04-13
---

The idea that **complex intelligence can emerge from the interactions of many simple agents** — without any central controller.

Natural examples: schools of fish (the origin of the name "MiroFish"), bird murmurations, ant colonies.

## In the AI Context

In modern AI, swarm intelligence typically means using many agents working concurrently and interacting with each other to solve problems or generate emergent behavior that a single agent cannot.

[[MiroFish]] applies this to social prediction: instead of asking a single LLM "what will happen?", it builds a simulated society of thousands of agents and observes the outcomes that emerge.

## Comparison with Traditional Prediction

| Approach | Method | Limitation |
| --- | --- | --- |
| Statistical model | Fit a curve from historical data | Misses nonlinear social dynamics |
| Single LLM | Ask the model directly | No emergent behavior; training bias |
| Swarm simulation | Release thousands of agents to interact | High compute cost; results depend on persona design |

## See Also

- [[Multi-Agent Simulation]] — implementation mechanics
- [[MiroFish]] — application of this concept
