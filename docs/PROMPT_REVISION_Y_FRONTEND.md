# Prompt para revisión first-principles + frontend

Pégalo en Claude Opus / GPT-5 / Gemini estando dentro del repo `lenguas-indigenas`:

---

```
Eres un ingeniero senior de ML + lingüística computacional + producto accesible.
Trabajas sobre el repo ACTUAL en el que estás parado (lenguas-indigenas).
Antes de proponer NADA, lee por completo: conversor.py, README.md, AGENTS.md,
docs/CUALQUIER_IDIOMA.md, docs/ENTRENAMIENTO_MODELOS.md,
tools/build_language_profiles.py, tools/fetch_language_data.py,
tools/score_translation.py, tools/eval_translation.py,
data/language_profiles.csv (estructura), languages_extra.json.example.

## Contexto que debes respetar

- Misión: accesibilidad — convertir texto o video de YouTube a AUDIO en lenguas
  indígenas. Empezó con México; ahora acepta cualquier ISO 639-3 con checkpoint
  MMS (999 verificados en data/mms_checkpoints.json).
- Hardware: Mac Intel, sin GPU. Inferencia pesada NO es local.
- Backends: Groq API (gratis, primario), Gemini (keys rotas), Ollama local
  (lento, solo offline), Ollama Cloud/Cerebras (sin créditos).
- Realidad medida: gpt-oss-120b saca ~0.01 en back-translation a zapoteco —
  los LLMs frontera FALLAN en lenguas de bajos recursos. La voz MMS es real;
  el hueco es la traducción.
- Reglas duras (AGENTS.md): honestidad técnica (es orquestación + evaluación,
  no "traductor que funciona"), nunca keys en código, probar 1 lengua antes
  de batch, no presentar audio sintético como voz comunitaria sin consentimiento,
  licencias/consentimiento documentados por lengua.

## TAREA 1 — Revisión desde first principles

Descompón el sistema a sus funciones mínimas (obtener texto → convertirlo a
otra lengua → sintetizar voz → verificar que sirve) y dime:

1. Qué pasos del pipeline actual sobran, faltan o están en el orden equivocado
   (ej: ¿conviene post-procesar la traducción? ¿validar fonemas antes de TTS?
   ¿detección de idioma de entrada?).
2. Qué mejoraría MÁS la calidad por unidad de esfuerzo: ¿mejores prompts?
   ¿diccionarios en contexto (RAG léxico)? ¿voto entre backends? ¿otro modelo
   de traducción (NLLB local)? ¿post-edición con reglas por familia? Rankea.
3. Qué deuda técnica cortar ahora (un solo archivo de ~700 líneas, estado
   global, keys en _key_chain) y cómo modularizar SIN romper la CLI.
4. Qué 3 experimentos baratos (corre hoy en esta máquina) responderían la
   pregunta "¿cómo subo el score de traducción de 0.01 a algo usable?".

No reescribas todo. Lista priorizada con impacto/esfuerzo y razonamiento
first-principles, no "best practices" genéricas.

## TAREA 2 — Genera el frontend

Construye una UI web mínima-pero-completa que corra `python3 app.py` en esta
Mac Intel, sin dependencias nuevas pesadas (Flask o stdlib http.server +
HTML/JS vanilla; NO Gradio si añade peso innecesario):

- Selector de lengua: curadas primero + campo libre para cualquier ISO 639-3
  (usa --list-mms / mms_checkpoints.json como fuente).
- Input: textarea (texto español) O url de YouTube.
- Botón "Generar": llama al pipeline real (conversor.convert), muestra
  progreso por pasos, luego: traducción generada + reproductor de audio +
  descarga .wav.
- Aviso honesto visible: "traducción automática de bajos recursos —
  verifica con un hablante; la voz es síntesis, no una persona real".
- Marca lenguas SIN checkpoint MMS (hch, tzo, tzh) como "solo texto" —
  no intentes TTS.
- API JSON en el mismo proceso: POST /api/convert {input, lang} → {translation, audio_path}.
- Que se pueda abrir file:// o http://localhost:8000 sin build steps.

Entrega los archivos completos y el comando exacto para correrlo. Después de
escribir, verifica: python3 -m py_compile app.py + una corrida real con una
frase corta en 'yua' y reporta resultado, no solo "debería funcionar".
```

---

## Notas de uso

- Si el otro modelo NO tiene acceso al repo, adjunta `conversor.py` y
  `docs/CUALQUIER_IDIOMA.md` como contexto.
- Si propone NLLB local: `facebook/nllb-200-distilled-600M` corre en CPU
  (~1GB RAM) y tiene ~200 lenguas — es el candidato #1 para subir el score
  sin nube; que lo evalúe contra el scorer antes de integrarlo.
- Regla del repo: cualquier cambio significativo se anota en
  `ACTIVIDAD_AGENTES.md` y se verifica con 1 lengua real antes de batch.
