# ACTIVIDAD_AGENTES.md — lenguas-indigenas

> Registro append-only, lo más reciente arriba. Cada agente anota: origen, qué se pidió, qué se hizo, archivos, pendientes.

---

## 2026-11-22 ~14:25 — Devin (mac-lap)

**Se pidió:** recuperar API keys de otros proyectos (ricpersonal, video_creator), revisar/mejorar el conversor, verificar doc de entrenamiento de LLMs.

**Hecho:**
- Verificación EN VIVO de todas las keys del ecosistema. Resultado actualizado en `ricpersonal/API_KEYS_ESTADO.md`.
  - VIVAS: Groq ×3 (traducción gpt-oss-120b + Whisper STT), ElevenLabs, Ollama local (llama3.2:3b)
  - AUTH-OK-SIN-CRÉDITO: Ollama Cloud ×5 (402), Cerebras ×4 (402)
  - MUERTAS: Google ×8, OpenRouter ×4, HF ×2, Groq ×2, Cerebras ×1
- `conversor.py` reescrito: rotación de keys (`X_API_KEY`..`_5`), auto-carga de `.env`, 5 backends de traducción (`auto` → groq→gemini→ollama-cloud→cerebras→llama), `--stt groq` (Whisper API gratis), detector de salida degenerada, auto-detección de modelo Ollama local.
- **Corregido el mapa de lenguas:** los IDs `nah/mix/zap/oto/tzo/tzh/mam` NO existían en HF (401). Tabla nueva verificada en vivo: 17 lenguas + 9 variantes. Tzotzil/Tzeltal no tienen checkpoint MMS.
- `.env` del proyecto creado con las 3 keys Groq vivas (gitignored).
- `.venv` Python 3.12 creado; pins Intel-Mac en `requirements.txt` (torch ≤2.2.2, transformers 4.46.3).
- **3 audios demo generados:** output_audio/demo_nahuatl_nah.wav, demo_maya_yua.wav, demo_mam_mam.wav.
- README, AGENTS.md, fondeo/*, PLAN_REGISTRO_Y_ONG.md actualizados (8→17 lenguas, keys, backends).
- `docs/ENTRENAMIENTO_MODELOS.md` creado — roadmap de fine-tuning (lo que pidió Rick: "doc de cómo entrenar LLMs" = las ~24 skills ML en `.devin/skills/`, locales; el doc las referencia y fija la ruta).

**⚠️ Concurrencia:** otro agente commiteó `7f6a36a` durante esta sesión (añadió `FONDEO_GOOGLE_GOBIERNO_MX.md`) y barrió parte de mis cambios en su commit. Sin pérdida, pero coordinar via este archivo.

**Pendientes:**
- Video 60s del GoFundMe (audios listos — falta grabar).
- zapoteco/otomí/huasteco: gpt-oss-120b alucina/balbucea; mejorar con prompts por lengua u otro backend.
- Enviar Mozilla Fellowship antes del 17-dic, NLnet antes del 3-ene.
- Activar GitHub Sponsors + subir funding.json a floss.fund.

---
