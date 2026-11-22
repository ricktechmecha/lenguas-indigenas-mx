# Aplicación — Mozilla Foundation Fellowship
**Deadline: 17-dic-2026 23:59 PT** | Premio: $125,000 USD / 12 meses
Portal: mozillafoundation.org → Fellowships → Apply

> ⚠️ Copia/adapta cada sección al formulario real. Personaliza lo que está en [corchetes].

---

## Sobre ti / About you

**Nombre:** Ricardo Rodríguez [apellidos completos]
**Ubicación:** Ciudad de México, México
**Rol:** Independent open-source developer
**Links:**
- Repo: https://github.com/ricktechmecha/lenguas-indigenas-mx
- LinkedIn: [tu perfil]
- Demo: [link al video demo — grabarlo antes de enviar]

**Bio (EN, ~100 palabras):**

> Independent developer from Mexico City building open-source infrastructure for linguistic equity. I built Lenguas Indígenas MX, a working pipeline that converts any text or YouTube video into spoken audio in 8 Mexican indigenous languages — náhuatl, maya yucateco, mixteco, zapoteco, otomí, tzotzil, tzeltal and mam — by orchestrating Whisper ASR, LLM translation (Gemini and local Llama) and Meta's MMS-TTS. My work sits at the intersection of AI, accessibility, and indigenous data sovereignty: the next phase is a community-governed open speech corpus recorded and validated by native speakers themselves.

---

## ¿Cuál es el problema? / The problem

> Mexico has 68 linguistic groupings and 364 variants (INALI), spoken by ~7 million people — yet almost none of them work on the internet. Government health information, emergency alerts, educational content, and every AI assistant ship in Spanish first, and in indigenous languages never. The communities most excluded from digital infrastructure are precisely those who most need accessible information in their own voice — literally.
>
> The bottleneck is not goodwill; it is data. There are no open, community-governed speech corpora for most Mexican indigenous languages, so no one can build voice interfaces for them. Commercial labs will not fund this: 7 million speakers fragmented across 68 languages is not a market. It is a public good — and public goods need public-interest technologists.

## ¿Qué vas a construir? / The project

> During the fellowship I will build three things:
>
> **1. A production-ready open-source toolkit** (already prototyped): the existing pipeline becomes a documented library + CLI + minimal web demo, with a local-Llama translation path so it runs fully offline — no API keys, no cost, usable inside communities without connectivity.
>
> **2. An open speech corpus, community-governed.** With partner communities in Yucatán (maya yucateco first), I will design a consent-first recording protocol: speakers are paid, retain control over how their voice data is used, and the corpus is published under an open license with a community governance charter following CARE Principles for Indigenous Data Governance. This is the dataset layer every future voice application in these languages needs.
>
> **3. A replicable playbook.** Documented protocol (consent, recording, validation, licensing, publishing) that any community in Latin America or Africa can reuse for their own language — turning one project into infrastructure.

## ¿Por qué ahora? / Why now

> Three curves just crossed: (a) open TTS models (Meta MMS) now cover 1,100+ languages including the main Mexican variants — the raw capability exists for the first time; (b) the Decade of Indigenous Languages (UNESCO IDIL 2022-2032) put institutional pressure on this gap; (c) LLM translation makes the "last mile" — turning written Spanish into natural indigenous speech — cheap enough to run on a laptop. The only missing piece is the open data layer and a person dedicated full-time to building it.

## ¿Por qué tú? / Why you

> I built the working prototype alone, on consumer hardware, in one file: it already turns a YouTube video into a maya yucateco audio file end-to-end. I am embedded in the context I build for — Mexican, working-class, self-taught, with direct relationships in Yucatán where the pilot corpus would be recorded. I am not a researcher describing the problem; I am the person who ships the code, records the speakers, and writes the consent protocol. The fellowship is not seed money for a team — it is 12 months of full-time focus for the one person already doing the work.

## ¿Qué cambia en el mundo si funciona? / Impact

> Success = (1) a public corpus of validated indigenous-language speech (first of its kind for maya yucateco under community governance), (2) a toolkit any developer can `pip install` to voice-enable their content in an indigenous language, (3) a documented playbook adopted by at least 2 other communities/regions. In the long run: every government announcement, health campaign, and classroom video can exist in náhuatl or maya within hours, not never.

## Plan de 12 meses / Milestones (resumen)

| Trimestre | Entregable |
|---|---|
| Q1 | Toolkit v1.0 (library + CLI + web demo), protocolo de consentimiento co-diseñado con comunidad piloto |
| Q2 | Grabación corpus piloto maya yucateco (meta: 50+ hrs, 20+ hablantes, todos remunerados) |
| Q3 | Corpus publicado (open license + governance charter), toolkit v1.1 con evaluación por hablantes |
| Q4 | Playbook + documentación replicable; extensión a 2ª lengua según comunidad; reporte de impacto |

## Presupuesto orientativo (si lo piden)

| Concepto | Estimado |
|---|---|
| Honorarios fellow (12 meses, tiempo completo) | $60,000 |
| Remuneración a hablantes nativos (grabación + validación) | $25,000 |
| Equipo de grabación + viajes a comunidades | $15,000 |
| Cómputo/infraestructura + dominio + hosting | $10,000 |
| Documentación, traducción de materiales, comunidad | $15,000 |
| **Total** | **$125,000** |

## Riesgos y honestidad (sección "challenges")

> Translation quality for low-resource languages is imperfect — I am honest about it in the repo. Mitigation: human validation by native speakers is built into the corpus workflow, not an afterthought. Second risk: doing community work *for* rather than *with* — mitigated by paid speaker governance seats and the CARE-principles charter. Third: solo-maintainer bus factor — mitigated by open playbook and public roadmap.

---

## Antes de enviar

- [ ] Grabar video demo (guion en `CAMPAÑA_GOFUNDME.md` §Video) y subirlo — Mozilla juzga ejecución
- [ ] Personalizar bio y links
- [ ] Verificar que el repo esté al día: push de Llama fallback + funding.json
- [ ] Releer en inglés; que alguien lo revise si hay tiempo
