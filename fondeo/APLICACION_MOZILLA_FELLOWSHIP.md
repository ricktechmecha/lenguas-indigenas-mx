# Mozilla Foundation Fellowship 2027 — ✅ LOI ENVIADO 22-nov-2026

**Estado: LOI enviado y confirmado por el portal.** Respuestas/invitaciones a Full Application: ~mediados de feb-2027. Contacto oficial: fellowships@mozillafoundation.org.
Se envió como **Track II: Independent Fellow**, issue area **"Sovereign AI, public infrastructure and maintenance"**, con email nornos94@gmail.com. Este archivo queda como registro del contenido base.

**Deadline LOI: jueves 17-dic-2026, 11:59 PM PT** — ~3 semanas.
Premio: hasta **$125,000 USD / 12 meses**. Tracks: Embedded e Independent.
Portal: mozillafoundation.org → Fellowships → 2027 Call → Letter of Intent.

> El LOI de Mozilla es CORTO (~500-800 palabras por sección). Aquí va la
> versión lista; adapta nombres/rutas con [corchetes]. Basado en la
> convocatoria real verificada 2026-11-22.

---

## Track recomendado: **Independent**

El proyecto no necesita sede institucional — es open-source puro con socios
comunitarios. Embedded exigiría una org anfitriona que no tenemos todavía.

## LOI — Project Summary (~200 palabras)

> **Lenguas Indígenas** is open-source infrastructure for linguistic equity:
> it turns any text or YouTube video into spoken audio in the language of
> your choice — today covering 116 languages end-to-end and mapping all
> ~7,000 living languages by real capability.
>
> The problem is measured, not assumed: frontier LLMs score 0.00–0.49 on
> back-translation into languages like Isthmus Zapotec and Yucatec Maya,
> while dedicated NMT reaches 0.58–0.75 — and Meta's MMS-TTS already ships
> voice checkpoints for ~1,000 languages that nobody connects to translation.
> We built the missing orchestration layer: honest evaluation, typological
> grammar injection, phoneme-aware TTS normalization, and a public coverage
> matrix showing exactly which languages work, which have voice-only, and
> which of the ~6,880 remaining need community-built datasets.
>
> During the fellowship I will (1) build a consent-first speech corpus with
> Maya/Yucatec partner communities following CARE Principles, (2) fine-tune
> open models (VITS/MMS for voice, LoRA for translation) on that corpus,
> and (3) publish a replicable playbook so any community can do the same
> for their language. Repo + live demo: [link].

## LOI — Why you / why this (~150 palabras)

> I am an independent developer from Mexico City who already built and
> published the working prototype — pipeline, evaluation harness, coverage
> matrix, and web demo are live and verifiable today. I work at the
> intersection Mozilla cares about: open source, accessibility, and the
> communities technology forgot. My commitment is to keep every artifact
> open (MIT/CC-BY), every claim measured, and every dataset community-governed.

## LOI — What you'll build (~150 palabras)

> Three deliverables in 12 months:
> **1. Community speech corpus** — consent-first recording protocol with
> paid native speakers in Yucatán (maya yucatec first), governance charter
> per CARE Principles, open license.
> **2. First community-validated models** — fine-tune VITS/MMS-TTS and a
> translation adapter on the corpus; publish WER/BLEU-style scores and
> native-speaker evaluation, honest about what fails.
> **3. Replicable playbook + expanded coverage** — documented protocol any
> community can reuse; extend validated coverage to 3–5 more Mexican
> languages (náhuatl, zapoteco candidates) using the same method.

## LOI — Budget sketch (~100 palabras)

> ~$60k personnel (my time), ~$25k community speaker compensation + travel,
> ~$15k compute (cloud GPU for fine-tuning), ~$10k validation workshops +
> dissemination, ~$15k contingency. All open-source outputs; no proprietary
> lock-in.

## Notas para la full application (si avanza)

- **Evidencia adjunta:** captura de `python3 app.py` funcionando, tabla de
  `docs/MAPA_DEL_HUECO.md` (scores LLM vs NMT), `docs/LENGUAS_COBERTURA_MUNDIAL.md`.
- **Debilidad honesta a anticipar:** no somos lingüistas — el plan incluye
  partners académicos/comunitarios para validación (mencionar a alguien
  concreto si existe: [investigador INALI / universidad local]).
- **Cuidado con claims:** decir "orquestación de modelos abiertos + datasets
  comunitarios" — NO "traductor que funciona para todas las lenguas".
- Mozilla valora **open source + movimiento**: destacar que todo el código,
  datos de perfiles (WALS/PHOIBLE, CC-BY) y herramientas de evaluación son
  reutilizables por otros proyectos.
