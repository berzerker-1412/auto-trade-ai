---
title: AI Research Skills Library
type: source
tags: [ai-research, skills, agents, ml, orchestra-research]
sources: 1
created: 2026-04-14
updated: 2026-04-14
---

Open-source library of 87 skills by [[orchestra-research|Orchestra Research]] that enables AI agents to autonomously conduct end-to-end ML research — from ideation and literature survey through experiment execution to paper writing.

## Key Claims / Findings

- **87 skills across 22 categories** covering the full AI research lifecycle: model architecture, fine-tuning, post-training, distributed training, inference, RAG, agents, multimodal, prompt engineering, MLOps, observability, safety, emerging techniques, ideation, and paper writing.
- **Autoresearch skill** is the central orchestration layer — uses a two-loop architecture (inner optimization loop + outer synthesis loop) that manages the full research lifecycle and routes to domain-specific skills as needed. Supports Claude Code `/loop` and OpenClaw heartbeat for continuous operation.
- **Progressive disclosure skill format** — same pattern as [[playwright-skill]]: each skill has a `SKILL.md` (50–150 lines quick reference) + `references/` folder (300KB+ deep documentation from official sources, real GitHub issues, tutorials, API refs).
- **Install in one command**: `npx @orchestra-research/ai-research-skills` — auto-detects Claude Code, Gemini CLI, Cursor, OpenCode, Hermes Agent and installs to `~/.orchestra/skills/` with symlinks per agent.
- **Claude Code marketplace alternative**: `/plugin marketplace add orchestra-research/AI-research-SKILLs` then install by category.
- Skills installed to `~/.orchestra/skills/` with symlinks into each agent's skill directory.
- Quality bar: 300KB+ documentation per skill, real GitHub issues & solutions, code examples with language detection, version history & breaking changes.

## Notable Demos

Two papers produced end-to-end by AI agents using the autoresearch skill:

> **Norm Heterogeneity → LoRA Brittleness**: Agent discovered norm heterogeneity predicts fine-tuning difficulty (r=−0.99) by autonomously *refuting its own hypothesis* and pivoting to a stronger finding. The agent started with ETF overlaps, got null results, and discovered the stronger signal independently.

> **RL Algorithm Brain Scan**: Agent found DPO is a rank-1 perturbation (95.6% recovery from one SVD direction) while online RL is distributed and structure-preserving. Used GRPO, TRL, SAELens, TransformerLens, and ML Paper Writing skills together.

These are notable because the agent didn't just execute — it demonstrated genuine research behavior: hypothesis generation, refutation, pivoting, synthesis.

## Skill Categories

| Category | Count | Highlights |
| --- | --- | --- |
| Autoresearch | 1 | Two-loop orchestration, routes to all other skills |
| Post-Training | 8 | TRL, GRPO, OpenRLHF, SimPO, verl, slime, miles, torchforge |
| Multimodal | 7 | CLIP, Whisper, LLaVA, Stable Diffusion, SAM, BLIP-2, AudioCraft |
| Emerging Techniques | 6 | MoE, Model Merging, Long Context, Speculative Decoding, Distillation, Pruning |
| Optimization | 6 | Flash Attention, bitsandbytes, GPTQ, AWQ, HQQ, GGUF |
| Distributed Training | 6 | Megatron-Core, DeepSpeed, FSDP2, Accelerate, Lightning, Ray Train |
| RAG | 5 | Chroma, FAISS, Sentence Transformers, Pinecone, Qdrant |
| Model Architecture | 5 | LitGPT, Mamba, RWKV, NanoGPT, TorchTitan |
| Fine-Tuning | 4 | Axolotl, LLaMA-Factory, PEFT, Unsloth |
| Mech Interp | 4 | TransformerLens, SAELens, pyvene, nnsight |
| Agents | 4 | LangChain, LlamaIndex, CrewAI, AutoGPT |
| Safety & Alignment | 4 | Constitutional AI, LlamaGuard, NeMo Guardrails, Prompt Guard |
| Inference | 4 | vLLM, TensorRT-LLM, llama.cpp, SGLang |
| Prompt Engineering | 4 | DSPy, Instructor, Guidance, Outlines |
| Evaluation | 3 | lm-eval-harness, BigCode, NeMo Evaluator |
| MLOps | 3 | W&B, MLflow, TensorBoard |
| Infrastructure | 3 | Modal, SkyPilot, Lambda Labs |
| ML Paper Writing | 2 | LaTeX templates, Academic Plotting |
| Ideation | 2 | Research Brainstorming, Creative Thinking |
| Data Processing | 2 | NeMo Curator, Ray Data |
| Tokenization | 2 | HuggingFace Tokenizers, SentencePiece |
| Observability | 2 | LangSmith, Phoenix |

## Pattern Connection

This library is a large-scale instance of the [[soul-md|plain-text context injection]] pattern — SKILL.md files injected into agent context on demand. The autoresearch skill extends the pattern by adding *routing logic*: instead of a single static context file, the agent dynamically selects which domain skills to load based on the current research stage.

## Entities Touched

- [[orchestra-research|Orchestra Research]] — maintainer
- [[openclaw|OpenClaw]] — autoresearch skill supports OpenClaw heartbeat for continuous operation
