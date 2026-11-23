# Qué falta y cómo alimentarlo — checklist maestro

> El pipeline está listo de punta a punta. Lo que falta NO es código:
> es **datos consentidos**, **GPU**, y **validación humana**. Este doc dice
> exactamente qué falta por pieza y el comando que lo alimenta.

## Cómo alimentar el proyecto (resumen de 3 comandos)

```bash
python3 tools/corpus_tool.py init <iso>      # 1. crea el folder de la lengua
#    → meter wavs/ + metadata.csv + parallel_es.csv + firmar CONSENT.json
python3 tools/corpus_tool.py validate <iso>  # 2. ¿los datos sirven?
python3 tools/corpus_tool.py pack-<tts|asr|mt> <iso>   # 3. → dataset listo pa' GPU
```

El checkpoint resultante se integra **sin tocar código** en `languages_extra.json`:

```json
{ "<iso>": { "name": "...", "mms": "./models/tts-<iso>",
             "custom_mt": "./models/mt-<iso>" } }
```

`custom_mt` tiene **prioridad automática** sobre Groq/Google en el pipeline.

---

## ✅ Ya funciona (no falta nada para usarlo)

| Pieza | Estado |
|---|---|
| Texto → audio | 116 lenguas tier A (voz + NMT), 901 tier B (voz + LLM) |
| YouTube → audio | yt_dlp + Groq Whisper + translate + MMS, verificado E2E |
| Audio local → audio | `--audio` / pegar ruta en la web (demo incluida) |
| Evaluación objetiva | `tools/score_translation.py` (back-translation) |
| Sitio | `app.py` — landing + tabla mundial + conversor, a11y básico |
| Infra de corpus | `corpus_tool.py` — consentimiento, validación, packing |

## 🟡 Falta — ingeniería (código/pipeline, no datos)

| # | Qué falta | Dificultad | Para qué |
|---|---|---|---|
| 1 | **Alineación temporal para doblaje** — cada línea traducida debe caber en su escena. Herramientas: `aeneas`/`stable-ts` (timestamps por frase) + `ffmpeg atempo` | Media | Convertir series/películas sin que el audio se desfase |
| 2 | **Mezcla/mux de doblaje** — bajar el original bajo la voz nueva: `ffmpeg loudnorm` + sidechain básico | Baja | Audio final usable en video real |
| 3 | **Diarización de voces** — separar quién habla (pyannote) para dar voz distinta por personaje | Media | Doblaje con más de un personaje |
| 4 | **Whisper fine-tuneado como STT** — hoy transcribe bien español; para audio indígena → texto hace falta ASR propio | Datos+GPU | Sentido inverso: corpus/documentales indígenas → texto |
| 5 | **Detección de idioma de entrada** — hoy asume español | Baja (langdetect/fasttext lid) | Robustez cuando el video no está en español |
| 6 | **Diccionarios en contexto (RAG léxico)** — inyectar glosarios curados al prompt de traducción | Media | Subir calidad de traducción sin entrenar |

## 🔴 Falta — datos y recursos (lo que se pide en los grants)

| # | Qué falta | Mínimo | Ideal | Comando que lo valida |
|---|---|---|---|---|
| 1 | **Corpus de voz consentido** (tier C/D: hch, tzo, tzh y ~6,880 más) | ~1h limpia, 1 hablante | 5-20h, varios hablantes | `corpus_tool.py validate <iso>` |
| 2 | **Pares de traducción** español↔lengua | ~5,000 frases | 50k+ | `corpus_tool.py validate` (cuenta pares) |
| 3 | **GPU** para fine-tune | Colab Pro/RunPod | A100 dedicada | `train/*.py` |
| 4 | **Validación de hablantes nativos** — TTS/MT evaluados por la comunidad | 3 personas por lengua | panel por región | manual (no automatizable) |
| 5 | **CONSENT.json firmado por lengua** — soberanía de datos documentada | 1 por lengua | asamblea/carta comunitaria | `corpus_tool.py validate` (bloqueante) |
| 6 | **Socios comunitarios** — asociaciones de hablantes, UADY, INALI, radios comunitarias | 1 por lengua | red permanente | — |
| 7 | **MMS-ASR probado** (`mms-1b-all` cubre ~1,000 lenguas) — puede que ASR ya exista para tier A/B y NO lo hemos probado | 1 tarde de experimento | integrarlo como `transcribe` alterno | pendiente: spike técnico |

## Por idioma (los 3 sin NADA hoy)

| ISO | Lengua | Tier | Qué falta exactamente |
|---|---|---|---|
| `hch` | Wixárika | C | Todo: corpus voz, pares MT, TTS propio, ASR |
| `tzo` | Tzotzil | C | Todo (mismo stack; hay más recursos externos disponibles) |
| `tzh` | Tzeltal | C | Todo |

Para las ~6,880 tier D del mundo: el mismo stack — por eso el pipeline es genérico por ISO 639-3 y no por lista mexicana.

## Lo que NO falta (para no pedir de más en los grants)

- ❌ "Investigar cómo hacer TTS" — MMS + fine-tune VITS ya está resuelto y scaffold en `train/`
- ❌ "Desarrollar la app" — `app.py` + `conversor.py` funcionan y hay tests
- ❌ "Evaluar calidad" — `score_translation.py` mide objetivamente

**La narrativa correcta:** "la infraestructura y la evaluación existen; financiamos
datos consentidos, cómputo y validación comunitaria — no humo."
