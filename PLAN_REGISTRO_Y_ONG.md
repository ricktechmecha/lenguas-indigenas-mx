# PLAN — Registro/publicación app Lenguas Indígenas + idea ONG (11-oct-2026)

## A. Plan de registro del proyecto (open-source + grants)

### 1. Identidad y presencia (esta semana)
- [ ] Nombre/dominio del proyecto — candidatos: `lenguasindigenas.mx`, `vocesindigenas.mx` (verificar disponibilidad en Namecheap/Cloudflare ~$200 MXN/año)
- [ ] Correo del proyecto: `contacto@<dominio>` o `lenguasindigenasmx@gmail.com` gratis mientras
- [ ] Repo GitHub público en `ricktechmecha` (o crear org `voces-indigenas-mx` — gratis, se ve más serio para grants)
- [ ] README EN+ES honesto: "orquestación de Whisper + Gemini + MMS-TTS" (ver AGENTS.md regla 3)

### 2. Publicación técnica (requisitos del repo)
- [ ] `requirements.txt`/`pyproject.toml` ✅ (requirements ya existe — verificar)
- [ ] `.gitignore`: `output_audio/`, `.env`, `__pycache__`, `.venv*`
- [ ] Licencia MIT o Apache-2.0 (compatible con MMS)
- [ ] Demo: video/gif de 30s generando audio en náhuatl
- [ ] Test con 1 lengua antes de batch (regla AGENTS.md)

### 3. Grants a los que aplicar (el dinero)
| Grant | Qué pide | Fit |
|---|---|---|
| **Lacuna Fund** (datasets lenguas) | Dataset abierto + comunidad | 🔥 El modo "corpus" con hablantes nativos |
| **Mozilla OMSF** (Open Source) | Proyecto open-source con impacto | 🔥 Repo público + README impacto |
| **AmericasNLP** | Papers/workshops NLP lenguas americanas | Publicar paper del pipeline |
| **Meta Llama Impact Grants** | Usar Llama | Requiere fallback de traducción a Llama local (pendiente roadmap) |
| **Google.org / AI for Good** | Impacto social medible | Fase posterior |
| **INALI / gobierno MX** | Convenios de difusión | Vía ONG (sección B) |

### 4. Correos/convocatorias — template de pitch (borrador)
```
Subject: Open-source pipeline — text/video to audio in 17 Mexican indigenous languages

We built an open-source pipeline converting any text/YouTube video into spoken
audio in náhuatl, maya, mixteco, zapoteco, otomí, mam, huasteco, mazateco, triqui, chatino, wixárika, huave, purépecha, totonaco, tepehua, mayo and popoloca
(Whisper ASR → translation → Meta MMS-TTS, extensible to 1,100+ languages).
We seek funding to build a community-validated open corpus with native speakers.
Repo: github.com/ricktechmecha/lenguas-indigenas
```

## B. Idea ONG — inclusión de lenguas indígenas en México

**Por qué sí tiene sentido:** la ONG es el vehículo legal para recibir grants internacionales (Lacuna/Mozilla NO fondean personas físicas — fondean organizaciones). También desbloquea convenios con INALI, CDI (ahora INPI), SEP, universidades.

### Figura legal en México
- **A.C. (Asociación Civil)** — la correcta para esto. Sin fines de lucro, puede recibir donativos y grants.
- Requisitos: acta constitutiva ante notario (~$15-30k MXN), mínimo 2 socios, estatutos, registro en Registro Público.
- **CLUNI** (registro federal) — gratis, te habilita para fondeos gubernamentales. Trámite: cluni.gob.mx
- **Donataria autorizada SAT** — para emitir recibos deducibles (clave para donaciones grandes). Tarda meses.
- Alternativa barata/rápida: **fiscal sponsorship** — operar bajo una ONG ya constituida (ej. aliarse con una que ya trabaje con comunidades indígenas) mientras se constituye la propia.

### Ruta realista
1. Fase 0 (gratis, ahora): repo público + nombre + correo + documentar misión
2. Fase 1 (0-3 meses): aplicar grants internacionales como individuo/repo donde se pueda (Mozilla OMSF sí acepta individuos en algunas convocatorias)
3. Fase 2 (cuando haya grant serio): constituir A.C. con notario + CLUNI
4. Fase 3: donataria autorizada + convenios INALI/INPI

### ⚠️ Advertencia honesta (soberanía de datos)
Los grants serios y comunidades indígenas exigen: consentimiento informado de hablantes, gobernanza comunitaria del corpus, no extraer datos sin retorno a la comunidad. Esto NO es burocracia — es lo que hace el proyecto fundable. Ver UNESCO IDIL + CARE Principles for Indigenous Data Governance.

## C. Prioridad vs todo lo demás
Esto es un asset de portafolio+impacto, NO genera dinero esta semana. Secuencia:
**empleo freelance (Outlier/DataAnnotation $) → candidatura IPN (30 oct) → este proyecto en ratos libres.**
