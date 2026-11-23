# ACTIVIDAD_AGENTES.md — lenguas-indigenas

> Registro append-only, lo más reciente arriba. Cada agente anota: origen, qué se pidió, qué se hizo, archivos, pendientes.

---

## 2026-11-23 ~04:30 — Devin (mac-lap) — E2E Playwright + bug de preámbulo LLM cazado

**Se pidió:** seguir probando entrada/salida y corregir ("sigue haciendo todo, haz pruebas").

**Hecho:**
- `tests/e2e/test_web.py` — 9 tests con Playwright/Chromium real contra app.py en puerto efímero: APIs, tabla cobertura (filtros/paginación), validación del form, idioma inválido con sugerencias, a11y básico (h1/skip/labels/aria-live), landing, y conversión REAL a hch (text-only).
- **BUG REAL cazado por E2E:** Llama devolvía preámbulo ("I'm happy to happy to help with the translation… I'll be using Wixárika… (Note: …)") que pasaba el guard anti-disculpas y se habría mostrado/sintetizado como traducción. Ampliado `_REFUSALS` en conversor.py con patrones de preámbulo/meta-comentario ("i'm happy to help", "i'll be using", "here is the translation", "(note:", "note: i've"…). Ahora se descarta y cae al siguiente motor o falla limpio.
- Bug menor: `language_profiles.csv` abría archivo sin cerrar (ResourceWarning) → context manager.
- Fix de test: `page.content()` siempre contiene "<audio" en el JS inline → assert cambiado a locator real `#res audio` count==0; lectura de `#res` (incluye badges) en vez de `#result`.
- Landing: tiers de cobertura ahora se llenan por JS desde /api/coverage (antes estáticos); CSP actualizado con `script-src 'unsafe-inline'`.
- Resultado: **31 unitarios OK + 9/9 E2E OK.**

**Pendiente:** validación por hablantes nativos; alineación temporal para doblaje; corpus consentido tier C/D.

---

## 2026-11-23 ~03:30 — Devin (mac-lap) — skills ECC aplicadas: a11y + review + tests

**Se pidió:** revisar frontend/backend con las skills del proyecto ECC (code review, tests, diseño).

**Auditoría a11y (awesome-accessibility-audit) — fixes en app.py:**
- Labels ahora asociados (for/id), skip-link, nav landmark, h2 reales (antes divs), th scope=col, aria-live en progreso/resultado/contador, aria-labels en filtros, type="url" + name + spellcheck=false, :focus-visible, color-scheme dark, theme-color, touch-action, hover en botones, prefers-reduced-motion.

**Code review backend (awesome-code-review):**
- BUG: LANGUAGES['spa'].mms=None aunque el catálogo sí tiene mms-tts-spa → spa (demo) fallaba en TTS. Corregido + engine='none' en catálogo.
- BUG: synthesize() indexaba LANGUAGES[lang_code] → KeyError para aliases con guion/underscore → ahora resolve_language().
- /audio/ solo servía .wav → ahora wav/webm/m4a/mp3/ogg/opus/txt con mime correcto (audio_fuente de YouTube descargable).
- Security: Content-Length cap 2MB, jobs pruning >1h, headers nosniff/Referrer-Policy/CSP, traceback sanitizado a 1 línea.
- JS: alert()→error inline, polling con timeout 8min + retry en fallos de red, escape de regiones, paginación 100/pág en tabla de ~1,020 lenguas, catch en fetches, default yua.

**Tests (awesome-test-writing):** tests/test_core.py — 30 tests unittest stdlib, 0.02s, sin red/GPU. Mutación probada: gt_code→None falla 4 tests, _looks_refusal→False falla 1 → restaurado verde.

**Web guidelines (vercel):** color-scheme, tap-highlight, text-wrap balance, tabular-nums, overflow-wrap, empty states.

---

## 2026-11-23 ~02:00 — Devin (mac-lap) — documentación de fondeo completa

**Se pidió:** justificar por qué ayuda a la humanidad, por qué merecemos premios/fondos, e investigar cada premio para redactar su propia solicitud.

**Hecho:**
- Verificadas convocatorias reales (web): Mozilla Fellowship 2027 LOI cierra 17-dic-2026 ($125k, tracks Embedded/Independent); NLnet Restack €5-50k cada ~2 meses (GenAI fuera de scope → se vende como open-data commons); Lacuna ACTS cerró 13-nov (plantilla lista pa' próxima); UNESCO PP hasta $26k vía Comisión Nacional (requiere OSC aliada); ISOC research $200-500k.
- `fondeo/JUSTIFICACION_HUMANIDAD.md` — justificación maestra con evidencia medida.
- `APLICACION_MOZILLA_FELLOWSHIP.md` — reescrito como LOI listo-para-enviar (~500 palabras/sección) con scores y cobertura.
- `APLICACION_NLNET_RESTACK.md` — propuesta completa EN: abstract, fit Restack, plan 12m, budget ~€50k.
- `APLICACION_LACUNA.md` — posicionamiento + spec de dataset + checklist para próxima convocatoria.
- `APLICACION_UNESCO_PP.md` — borrador ES + ruta por comisión nacional.
- `ROADMAP_FONDEO.md` — actualizado con deadlines verificados y evidencia nueva.

---

## 2026-11-23 ~01:10 — Devin (mac-lap) — pruebas E2E + fixes reales

**Pruebas entrada/salida por la app:**
- yua: OK (google→MMS, back-translation perfecta)
- hch: OK text_only, Groq sí produce wixárika plausible
- nah (azz): OK — Groq produce náhuatl plausible, voz MMS 100%
- nhe: OK — Google round-trip EXACTO ("Buenos días, ¿cómo estás hoy?")
- Errores API: input vacío/lang inválido/JSON roto/traversal → todos 400/404 correctos

**Bugs encontrados y corregidos:**
1. `download_youtube` usaba CLI yt-dlp inexistente → reescrito con lib yt_dlp; cookies Chrome rompían extracción → fallback sin cookies; archivos webm/m4a sin ffmpeg (mime correcto por extensión); conservar extensión real (no renombrar a .mp3).
2. `convert` devolvía {} para lengua inválida → ahora devuelve error+suggestions (UI los muestra).
3. score_translation hardcodeaba 'groq' → agregado --translator; back-translate ahora prefiere Google cuando hay par.

**YouTube E2E VERIFICADO:** video ES 5.5min → webm → Groq Whisper → Google Maya → MMS 35.5s audio real (1.1MB wav).

**MAPA DEL HUECO (docs/MAPA_DEL_HUECO.md):** auto(google) vs groq — yua .75/.22, nah-hua .58/.27, mam .59/.13, kek .58/.04, zai .75/.00, quz .65/.32, ayr .65/.31, grn .70/.49. LLM se niega/inventa; NMT produce lengua real. Advertencia: round-trip mismo motor = fluidez, no exactitud.

---

## 2026-11-23 ~00:20 — Devin (mac-lap)

**Se pidió:** "haz todo lo que consideres" — cierre final.

**Hecho:**
- Back-translation de verificación en la UI: tras convertir, si Google soporta la lengua, re-traduce a español y lo muestra ("Significa en español"). Verificado: maya→es da "El niño come pan en casa de su abuela" — round-trip casi perfecto.
- `tts_mac_say` fallback arreglado sin ffmpeg: usa `afconvert` nativo → .m4a (probado, genera audio real). Retorna Path real para el result.
- app.py: server levantado con preview en :8000 (/, /cobertura, /convertir).
- README actualizado con las 3 rutas.

**Estado final:** sitio presentable completo + conversor verificado + docs de cierre (REVISION_FIRST_PRINCIPLES, PLAN_RECURSOS_POR_IDIOMA, LENGUAS_COBERTURA_MUNDIAL).

---

## 2026-11-22 ~23:45 — Devin (mac-lap)

**Se pidió:** cerrar investigación, decir si el pipeline está completo, qué falta, y generar frontend con página de explicación + tabla de cobertura + visión de doblaje de series/películas.

**Hecho:**
- `app.py` ahora es sitio de 3 páginas (stdlib puro): `/` landing explicativa (qué hace, tiers, visión doblaje, tabla de recursos por tier, disclaimer), `/cobertura` tabla mundial interactiva (buscador + filtros tier/región, ~1,020 lenguas desde data/cobertura.json), `/convertir` la herramienta (sin cambios funcionales).
- `tools/build_coverage_matrix.py` ahora emite también `data/cobertura.json`.
- `docs/PLAN_RECURSOS_POR_IDIOMA.md`: veredicto del pipeline por etapa + piezas que faltan para doblaje (alineación temporal = la pieza clave, aeneas/stable-ts/atempo; mezcla ffmpeg; MMS ASR para sentido inverso) + qué pedir por cada tier (A: validación; B: corpus paralelo/fine-tune; C: grabaciones consentidas + GPU; D: stack completo).
- Verificado: py_compile + las 3 rutas 200 + /api/coverage con tiers correctos.

**Veredicto:** pipeline texto→audio COMPLETO para tier A/B. Doblaje de contenido = ingeniería de pipeline (alineación+mezcla), no modelo nuevo. Cuello real: traducción tier B.

---

## 2026-11-22 ~23:15 — Devin (mac-lap)

**Se pidió:** lista mundial de cobertura por idioma (cuáles cubre y cuáles no) en .md tabla.

**Hecho:**
- `tools/build_coverage_matrix.py` → `docs/LENGUAS_COBERTURA_MUNDIAL.md` (regenerable).
- Clasificación real: 🟢A=116 (voz MMS + Google NMT), 🟡B=901 (voz MMS, traducción solo LLM), 🔵C=3 (solo texto: hch wixárika, tzo tzotzil, tzh tzeltal), 🔴D=~6,880 (resto ISO 639-3 sin datos).
- Fixes del generador: checkpoints MMS por dialecto (mam-dialect_central, hus-…) cuentan como voz; aliases curados (nah→azz, zap→zai, mix→xta) resuelven nombre+voz vía LANGUAGES; regiones Américas unificadas.
- México: tabla dedicada — A: kek/mam/yua/zai; C: hch/tzo/tzh.

---

## 2026-11-22 ~22:30 — Devin (mac-lap)

**Se pidió:** ejecutar la revisión first-principles + generar frontend, con mejor herramienta si existe.

**Hecho:**
- **Descubrimiento clave:** Google Translate NMT ya cubre ~110 pares MMS↔lengua verificados: nhe (náhuatl Huasteca), yua (maya), zap/zai (zapoteco), mam, kek, quz, ayr, grn + decenas de lenguas grandes. LLMs dan ~0.01 ahí; Google da traducciones reales (verificado E2E con yua → wav 4.6s, cobertura alfabeto 100%).
- `gtranslate.py` nuevo backend (auto-primero cuando hay par; endpoint público sin key, oficial con GOOGLE_TRANSLATE_API_KEY). Mapa `GT_BY_MMS` 110 pares, solo variantes coincidentes (nhe NO se usa para azz).
- `conversor.py`: `translate_ex` devuelve motor usado; `_looks_refusal` descarta disculpas del LLM (bug grave: se sintetizaban como "traducción"); `synthesize()` con caché de modelo, troceo por oraciones, `normalize_for_tts` (cobertura de grafemas); `text_only` para lenguas sin checkpoint (hch/tzo/tzh); `fallback_say` opt-out.
- **Fix:** epitran había subido numpy a 2.x rompiendo torch 2.2.2 → pineado numpy<2.
- `app.py` frontend: python3 app.py → :8000, catálogo con badges (voz/motor/alfabeto), jobs async, reproductor + descarga, aviso honesto. Verificado real con yua.
- `docs/REVISION_FIRST_PRINCIPLES.md` con el análisis completo + 3 experimentos.
- `docs/PROMPT_REVISION_Y_FRONTEND.md` (el prompt usado).

**Pendientes:** mapa del hueco (score sweep), diccionario few-shot, Whisper en lengua indígena; validación nativa sigue pendiente.

---

## 2026-11-22 ~20:00 — Devin (mac-lap)

**Se pidió:** priorizar APIs externas, avanzar todo, evaluar si es material de concursos.

**Hecho:**
- `tools/score_translation.py` — scorer objetivo vía back-translation ES→lengua→ES con Groq.
- **Hallazgo clave para grants:** gpt-oss-120b saca **0.01** en zapoteco del Istmo (se niega o loopea aun con prompt tipológico) y 0.00 en `zai` crudo → los LLMs frontera NO resuelven lenguas de bajos recursos. Eso justifica el proyecto: la voz ya existe (MMS), el hueco es traducción/datos.
- Veredicto concursos: SÍ como infraestructura+evaluación honesta+datasets; NO como "traductor que funciona".

---

## 2026-11-22 ~19:00 — Devin (mac-lap)

**Se pidió:** "haz todos los pendientes" — downloader de diccionarios/fonemas, Grambank, harness de evaluación.

**Hecho:**
- `tools/fetch_language_data.py` — descarga PHOIBLE (inventarios fonémicos IPA reales por lengua, CC BY-SA) + WALS/Grambank fusionado → genera `data/languages/<iso>.json` (pack: fonemas consonantes/vocales/tonos, orden de palabras, fuentes de diccionario, licencias, snippet para languages_extra.json). Corrido `--all-curated`: 30 packs generados; PHOIBLE cubre hus/huv/mam/maz/ncl/tsz/yua/zab/zai (huecos en el resto = documentación fonológica escasa, honesto).
- `tools/eval_translation.py` — benchmark: misma frase por Groq + modelos Ollama locales → `output_audio/eval_<lang>.md` (tiempo + detector degenerado). Filtra embeddings/vision/OCR y por default solo modelos ≤4B (CPU Intel). `--all` corre los ~28.
- epitran instalado pero NO cubre lenguas MX (solo fonemas PHOIBLE ahí; epitran sirve para lenguas grandes tipo ara/jpn).
- PanLex API caída → documentado; diccionarios apuntan a wiktextract/Glosbe.
- Cachés `data/_phoible`, `data/_grambank` gitignored; los packs `data/languages/*.json` sí se commitean.

**Pendientes:** Grambank completo (51MB) como fuente extra de rasgos; benchmark completo --all (lento en CPU); validación nativa.

---

## 2026-11-22 ~17:30 — Devin (mac-lap)

**Se pidió:** inyectar estructura gramatical por lengua al prompt de traducción ("excel" mínimo-completo de rasgos), re-revisar proyectos similares en GitHub, empezar con nuestras lenguas pero extensible (India, etc.).

**Hecho:**
- `tools/build_language_profiles.py` — descarga WALS CLDF (CC BY 4.0) y genera `data/language_profiles.csv`: **1,020 filas, 562 con datos WALS** (familia, género, orden de palabras 81A/82A/83A, adposición, genitivo, adjetivo-sustantivo, síntesis verbal, morfología).
- `_grammar_notes()` en conversor.py inyecta los rasgos WALS al prompt del traductor → el LLM reestructura al orden real de la lengua.
- **Bug corregido gracias a WALS:** varios códigos estaban mal etiquetados — `tri` era Tiriyo no Triqui (real: `trc`), `maz` era Mazahua no Mazateco (reales: `maj`,`mzi`), `cab` era Garífuna no Popoloca (real: `pls`), `hui` era Huli no Wixárika (`hch` no tiene checkpoint). Añadidos trs/maj/mzi/pls; hch/tzo/tzh quedan como stubs sin voz (candidatos a entrenar).
- **Verificado en vivo:** zapoteco ahora traduce limpio ("Bidxi' chii, gucui' ri' xquidxi'.") — el prompt VSO arregló el loop degenerado. Garífuna traduce real. Triqui/Popoloca: Groq se niega honestamente (mejor que alucinar).
- Panorama GitHub documentado en docs/CUALQUIER_IDIOMA.md (indic-speech-translate, ghana S2S, ttsmms, finetune-hf-vits) — nicho: nadie más hace tipología-en-prompt ni el combo video→audio con rotación gratis.
- `data/_wals/` gitignored (caché regenerable).

**Pendientes:** descargadores de diccionario/fonemas; Grambank como complemento de rasgos; validación nativa sigue pendiente para TODO.

---

## 2026-11-22 ~16:30 — Devin (mac-lap)

**Se pidió:** localizar la "super investigación" de entrenar modelos con audio / extender a todos los dialectos del mundo, revisar keys de video_creator (Gemini etc.) y **homologar el pipeline para cualquier idioma**.

**Hecho:**
- Investigación original encontrada en piezas: `video_creator/docs/LENGUAS_INDIGENAS_Y_VOZ.md` (+ FIRMA_VOZ, EMOCIONES_VOZ, TOOLKIT_IA_INVESTIGACION), `lyricforge/REPORTE_FINAL.md`, `ricpersonal/PLAN_ENTRENAR_LLMS.md`. No existe UN doc — consolidado en `docs/CUALQUIER_IDIOMA.md`.
- Keys de video_creator revisadas: la Gemini de su `.env`/`CREDENCIALES.md` es la misma muerta (400/403); ElevenLabs viva; Groq ya migrada.
- **Pipeline homologado a cualquier idioma:**
  - `data/mms_checkpoints.json` — 999 checkpoints MMS verificados (códigos ISO 639-3).
  - `resolve_language()`: `--lang` resuelve curados → `languages_extra.json` → catálogo MMS → alias de macrolenguas (que→quz, swa→swh) → sugerencias.
  - `--list-mms` nuevo; `--list-langs` muestra packs extra + conteo del catálogo.
  - `languages_extra.json.example` con esquema completo (iso639_3, glottocode, script, fuentes, licencia, validado_por_hablante).
  - `docs/CUALQUIER_IDIOMA.md`: receta de homologación — diccionarios (PanLex, wiktextract, Glosbe), fonemas (PHOIBLE, eSpeak NG, epitran), corpora (Common Voice/FLEURS/OpenSLR), ruta de fine-tune (VITS monohablante, XLSR ASR, LoRA NLLB), reglas de licencia/consentimiento.
- **Smoke test real:** `--lang quz` end-to-end → traducción Groq ("Allin p'unchay, comunidadman hamuqkuna") + `smoke_quz_quz.wav` 74KB. Funciona con lenguas no mexicanas.
- AGENTS.md/README actualizados (ya no "8 lenguas" ni solo MX).

**Pendientes:** descargadores reales de diccionario/fonemas (fuentes documentadas, sin implementar); benchmark de modelos Ollama locales; ninguna traducción validada por hablante nativo; `haw` (hawaiano) y otros sin checkpoint MMS publicado.

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
