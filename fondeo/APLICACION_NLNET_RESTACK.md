# Aplicación — NLnet Restack
**Deadline: 3-ene-2027 12:00 CET** | Rango: €5,000–50,000 | Acepta individuos, exige FLOSS (MIT ✅)
Portal: nlnet.nl/propose → fondo "Restack"
Formulario corto — se envía por email/formulario sencillo.

> ⚠️ Restack financia "bloques de construcción del internet abierto". El pitch correcto: **toolkit open-source de accesibilidad lingüística = building block para un internet no-anglocéntrico**, NO "app de traducción".

---

## Project name
**lenguas-indigenas-mx** — open speech toolkit for underrepresented languages

## Can you explain the whole project in one sentence?
An open-source toolkit and replicable protocol that turns any text or video into spoken audio in low-resource languages — starting with 17 indigenous languages of Mexico — so the open internet becomes usable for the ~7 million people it currently excludes.

## Requested amount
**€15,000** (rango conservador; pide lo que necesites justificar — desglose abajo)

## What are you going to do? (work plan)

1. **Harden the prototype into a distributable toolkit** (Python package + CLI + minimal web demo). Current state: working single-file pipeline (yt-dlp → Whisper → LLM translation → Meta MMS-TTS) already public under MIT. Deliverables: `pip install` package, docs EN/ES, test coverage, offline mode via local Llama (no API keys, no cloud dependency).
2. **Language-variant mapping layer**: map INALI's 68 groupings / 364 Mexican variants to the nearest MMS-TTS checkpoints, exposing a `--variant` flag — making the toolkit useful beyond the 17 languages already wired.
3. **Corpus toolkit + governance templates**: consent forms (ES + indigenous language), recording protocol, validation workflow, and license templates so communities can produce and own their own open speech data. This is the reusable "block" for the open internet.
4. **Pilot with maya yucateco community** (Yucatán): record + validate initial open corpus, proving the protocol end-to-end.

## Why is this relevant to an open internet stack?

> Today's internet speech layer is a walled garden: commercial TTS covers ~50 profitable languages, and ~7,000 others are invisible — no voice interfaces, no audio accessibility, no machine translation speech. Our contribution is a composable, permissively-licensed building block (orchestration layer + variant mapping + community data protocol) that any open application can reuse to voice-enable content in underrepresented languages. Everything produced — code, protocol, corpus, docs — is published under MIT / open data licenses. Without this layer, "open internet" silently means "internet for speakers of rich languages only".

## Compare with existing efforts

- **Meta MMS** (research): the TTS checkpoints we orchestrate — we add the usable toolkit + data layer on top.
- **Common Voice (Mozilla)**: covers few indigenous Mexican variants and is not community-governed; our protocol fixes the governance gap and our pipeline complements their data.
- **Google Translate / commercial TTS**: closed, paid, no indigenous Mexican languages for speech output.
- Novelty: end-to-end open pipeline + variant mapping + community-consent corpus protocol — no existing open equivalent for these languages.

## Costs breakdown (€15,000)

| Item | € |
|---|---|
| Development time (toolkit, variants, tests, docs) — ~6 months part-time | 9,000 |
| Native speaker compensation for pilot corpus (mayan) | 3,000 |
| Equipment + community travel (Yucatán pilot) | 2,000 |
| Hosting/domain/misc infra | 1,000 |

## Timeline

~6 months. Milestones: M1 package+docs, M2 variant mapping, M3 corpus toolkit, M4 pilot corpus + report.

## Sustainability

MIT-licensed repo with public roadmap; corpus governance charter hands ownership to the community; maintainer actively applying to complementary funders (Mozilla Fellowship, Lacuna Fund, FLOSS/fund) — NLnet's grant de-risks and accelerates, it is not sole dependency.
