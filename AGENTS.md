# AGENTS.md — Lenguas Indígenas MX (conversor texto/video → audio)

## Qué es este proyecto

Conversor de contenido (texto o video de YouTube) a audio en lenguas indígenas mexicanas. Pipeline: yt-dlp → Whisper → Gemini Flash (traducción) → Meta MMS-TTS → .wav. 8 lenguas validadas (náhuatl, maya, mixteco, zapoteco, otomí, tzotzil, tzeltal, mam); extensible a las 1,100+ de MMS-TTS.

**Objetivo:** publicarlo open-source + aplicar a grants de datasets/accesibilidad (Lacuna Fund, Mozilla OMSF, AmericasNLP).

## Stack

- Python 3.12 — un solo archivo `conversor.py`
- Deps: `transformers scipy torch yt-dlp playwright` + `openai-whisper` (brew)
- Keys: `GOOGLE_API_KEY`, `HF_TOKEN` — SOLO por env vars (ya limpiadas del código)

## Comandos de verificación

```bash
python3 conversor.py --list-langs
python3 conversor.py "Texto de prueba" --lang nah   # genera .wav en output_audio/
```

## Reglas del proyecto

1. **Nunca commitear keys** — el script ya fue escrubado; mantenerlo así (usar `~/.hermes/.env` o `.env` local gitignored).
2. **Prueba con 1 lengua antes de batch.**
3. **Honestidad técnica en docs:** es orquestación de modelos existentes (Whisper+Gemini+MMS), no modelos propios — escribirlo así en README/grants es más creíble.
4. **Impacto comunitario primero:** el ángulo fundable es accesibilidad + datasets abiertos, no el pipeline en sí.

## Pendientes (roadmap)

- [ ] `requirements.txt` / `pyproject.toml`
- [ ] Manejo de error cuando falta key (mensaje claro, no crash)
- [ ] README en inglés + demo (video/gif corto)
- [ ] Licencia (sugerida MIT o Apache-2.0 — compatible con MMS)
- [ ] `.gitignore`: output_audio/, .env, __pycache__, .venv*
- [ ] Evaluar fallback de traducción a Llama local (desbloquea Meta Llama Impact Grants)
- [ ] Extender a variantes INALI (68 agrupaciones / 364 variantes — vía mapeo a modelos MMS más cercanos)
- [ ] Modo "corpus": grabación de hablantes nativos para dataset abierto (requisito Lacuna)

## No hacer

- No prometer "traducción perfecta" en docs — las traducciones Gemini→lenguas de bajos recursos tienen errores; documentarlo honestamente es requisito para grants serios.
- No distribuir audio generado como "voz de la comunidad" sin consentimiento — temas de soberanía de datos indígenas (ver UNESCO IDIL).
