# Training & Fine-tuning Roadmap — Lenguas Indígenas MX

> Status: **deferred by design.** This project currently orchestrates existing
> open models (Whisper, MMS-TTS, hosted LLMs). Training our own models is a
> documented next stage, blocked on one prerequisite: **community-consistent
> data**, not compute or code.

This file consolidates what we evaluated, what we deferred and why, and the
concrete path to community-validated models. It exists so grant reviewers and
contributors can see the full picture — the deeper how-to lives in local agent
skills (see bottom).

## Why not train yet

1. **No consented corpus.** Fine-tuning TTS or translation on scraped audio
   would violate the data-sovereignty principles this project exists for
   (see README → Ethics). Corpus mode (guided recording with native speakers,
   informed consent, open license) comes first.
2. **Orchestration covers the accessibility gap today.** The bottleneck for
   communities is not model quality — it's that *no audio content exists at
   all* in their language.
3. **Training on an Intel Mac is not viable.** Compute will come from
   cloud GPU grants/credits (Modal, Lambda, or grant-funded), planned below.

## Path A — Fine-tune MMS-TTS on community voices

Goal: voices that communities recognize as their own, replacing the generic
MMS checkpoints.

- **Input**: 1–5 h of clean, consented recordings per speaker + transcripts
  (corpus mode tooling to be built — see ROADMAP).
- **Method**: fine-tune `facebook/mms-tts-<lang>` (VITS) on the new data;
  HF `transformers` supports VITS fine-tuning; speaker-conditioned models
  (XTTS-style) are an alternative for multi-speaker output.
- **Gate**: explicit community approval of synthetic-voice samples before
  any distribution. Never ship a "community voice" without it.

## Path B — Improve translation with open parallel corpora

Goal: better Spanish → indigenous translation than zero-shot LLM prompts.

- **Data**: FLORES-200 dev/devtest (includes `nah`, `yua`, `zap`, `ote`,
  `tzo`, `mam` variants), AmericasNLP shared-task corpora, INALI/CEPIADET
  public texts, Bible-adjacent public-domain parallel text (license-checked).
- **Curation**: dedup, quality-filter, license-audit (NeMo Curator-style
  pipeline; local skill `nemo-curator` has the how-to).
- **Method**: parameter-efficient fine-tuning (LoRA/QLoRA via `peft` +
  `accelerate`) on an open multilingual base (e.g. NLLB-200-distilled or an
  open Llama-class model if pursuing Meta Llama Grants). Preference tuning
  (SimPO/DPO) once human corrections of LLM translations accumulate via the
  review workflow.
- **Eval**: chrF/BLEU on FLORES dev + a community-review score; publish
  evals honestly — low-resource numbers will be modest and that's expected.

## Path C — Human-review loop (precondition for A and B)

Every translation this tool emits should be reviewable by a native speaker
and corrections stored as preference data. This loop is what turns
"orchestration" into a defensible dataset contribution for Lacuna /
AmericasNLP-style grants — and it is also the consent mechanism for Path A.

## Compute options evaluated

| Option | Status | Notes |
|--------|--------|-------|
| Local Intel Mac | Not viable | inference-only (MMS-TTS runs fine) |
| Modal | Documented (`modal` skill) | serverless GPU, credits needed |
| Lambda Labs | Documented (`lambda-labs` skill) | cheapest dedicated GPUs |
| Colab/Kaggle free tier | Viable for small LoRA runs | session limits |
| Grant-funded cluster | Target | Lacuna/Mozilla budgets can include compute |

## Local reference material (not committed)

This repo's `.devin/skills/` (gitignored, machine-local) already contains
deep how-to skills gathered during evaluation — `peft`, `accelerate`,
`torchtitan`, `pytorch-fsdp`, `flash-attention`, `huggingface-tokenizers`,
`nemo-curator`, `simpo`, `slime`, `saelens`, `modal`, `lambda-labs`,
`tensorrt-llm`. They document the *how*; this file records the *what/why/when*.

## Decision log

- **2026-11**: chose multi-backend translation (Groq/Gemini/Ollama/local
  Llama) over committing to one hosted LLM; training deferred until the
  consented corpus exists. See `fondeo/ROADMAP_FONDEO.md` for funding path.
