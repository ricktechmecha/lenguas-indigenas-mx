# AGENTS.md — Lenguas Indígenas MX (conversor texto/video → audio)

## Qué es este proyecto

Conversor de contenido (texto o video de YouTube) a audio en lenguas indígenas. Pipeline: yt-dlp → Whisper (local o Groq API) → traducción multi-backend (Groq/Gemini/Ollama) → Meta MMS-TTS → .wav. 17 lenguas mexicanas curadas + variantes, más **cualquier ISO 639-3 con checkpoint MMS** (~999 en `data/mms_checkpoints.json`, `--list-mms`) y perfiles propios vía `languages_extra.json` (ver `docs/CUALQUIER_IDIOMA.md`). Tzotzil/tzeltal NO tienen checkpoint MMS.

**Objetivo:** publicarlo open-source + aplicar a grants de datasets/accesibilidad (Lacuna Fund, Mozilla OMSF, AmericasNLP).

## Stack

- Python 3.12 — un solo archivo `conversor.py` (venv en `.venv/`, no del sistema)
- Deps: `transformers scipy torch yt-dlp` + `openai-whisper`, `ffmpeg` (en /usr/local/bin)
- Keys: SOLO por env vars o `.env` en raíz (auto-cargado, gitignored). Rotación: `X_API_KEY`, `X_API_KEY_2`..`_5`.
- Traductores (`--translator`): `groq` (gratis, recomendado), `gemini`, `ollama-cloud`, `cerebras`, `llama` (Ollama local, offline). `auto` prueba todos.
- STT (`--stt`): `groq` (whisper-large-v3-turbo API, gratis) o `local` (whisper CLI).

### Keys verificadas 2026-11-22

- **VIVAS:** GROQ ×3 (traducción gpt-oss-120b + Whisper STT), ElevenLabs, Ollama Cloud ×5 (auth OK pero 402 sin créditos)
- **MUERTAS:** Google ×8 (todas, 400/403 leaked), OpenRouter ×4, HF ×2, Cerebras (402), Groq ×2
- Copia de las Groq vivas en `.env` del proyecto. Inventario maestro: `ricpersonal/API_KEYS_ESTADO.md`

## Comandos de verificación

```bash
.venv/bin/python conversor.py --list-langs
.venv/bin/python conversor.py "Texto de prueba" --lang nah   # genera .wav en output_audio/
```

## Reglas del proyecto

1. **Nunca commitear keys** — el script ya fue escrubado; mantenerlo así (usar `~/.hermes/.env` o `.env` local gitignored).
2. **Prueba con 1 lengua antes de batch.**
3. **Honestidad técnica en docs:** es orquestación de modelos existentes (Whisper+Gemini+MMS), no modelos propios — escribirlo así en README/grants es más creíble.
4. **Impacto comunitario primero:** el ángulo fundable es accesibilidad + datasets abiertos, no el pipeline en sí.

## Pendientes (roadmap)

- [x] `requirements.txt`
- [x] Manejo de error cuando falta key (mensaje claro + rotación automática)
- [ ] Demo (video/gif corto) — audios demo pendientes de generar
- [x] Licencia MIT
- [x] `.gitignore`: output_audio/, .env, __pycache__, .venv*
- [x] Fallback de traducción (multi-backend: Groq/Gemini/Ollama-Cloud/Cerebras/Llama local — `--translator llama` para Meta Llama Grants)
- [ ] Extender a variantes INALI (68 agrupaciones / 364 variantes — vía mapeo a modelos MMS más cercanos)
- [ ] Modo "corpus": grabación de hablantes nativos para dataset abierto (requisito Lacuna) — ver `docs/ENTRENAMIENTO_MODELOS.md`
- [ ] Entrenar/fine-tune modelos propios — plan en `docs/ENTRENAMIENTO_MODELOS.md` (bloqueado: falta corpus consentido, no compute)

## No hacer

- No prometer "traducción perfecta" en docs — las traducciones Gemini→lenguas de bajos recursos tienen errores; documentarlo honestamente es requisito para grants serios.
- No distribuir audio generado como "voz de la comunidad" sin consentimiento — temas de soberanía de datos indígenas (ver UNESCO IDIL).
