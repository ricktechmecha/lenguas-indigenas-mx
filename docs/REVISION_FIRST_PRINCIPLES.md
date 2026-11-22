# Revisión first-principles del sistema

> Hecha 2026-11-22 contra el código real (`conversor.py` ~830 líneas,
> `gtranslate.py`, `tools/*`). Decomposición mínima: **obtener texto →
> traducir → sintetizar voz → verificar que sirve → entregar a humano.**

## 1. Qué sobraba / faltaba / estaba en orden equivocado

| Hallazgo | Estado | Acción |
|---|---|---|
| El paso "verificar que sirve" no existía | ❌ faltaba | `score_translation.py` (back-translation) + badge de cobertura de alfabeto en la UI |
| Fallback `say` leía texto indígena con voz ESPAÑOLA | ⚠️ orden equivocado | `convert(fallback_say=False)`; web nunca lo activa; solo CLI lo permite |
| TTS sobre texto con caracteres fuera del alfabeto del checkpoint | ⚠️ silencioso | `normalize_for_tts` mapea apóstrofos y reporta cobertura + grafemas perdidos |
| Lenguas sin checkpoint MMS intentaban TTS | ❌ | ahora devuelven `text_only` explícito |
| LLM "se disculpaba" y eso se sintetizaba como si fuera traducción | ❌ grave | `_looks_refusal` descarta negativos del LLM (no aplica a Google NMT) |
| Un solo archivo de 800 líneas con 6 backends | ⚠️ deuda | `gtranslate.py` ya es módulo aparte; el resto se modulariza cuando duela |

## 2. Qué mejora la calidad por unidad de esfuerzo (rankeado)

1. **Motor NMT dedicado donde existe** — `gtranslate.py` conecta ~110 pares
   MMS↔Google verificados (náhuatl Huasteca, maya, zapoteco, mam, q'eqchi',
   quechua, aymara, guaraní + decenas de lenguas grandes). Impacto ALTO,
   esfuerzo BAJO, ya implementado y probado end-to-end.
   - Riesgo honesto: el endpoint sin key (`client=gtx`) es no-oficial →
     para publicar/operar se usa `GOOGLE_TRANSLATE_API_KEY` (mismo código,
     rama oficial).
2. **Back-translation como sanity check** — re-traducir a español con el
   MISMO motor para que el usuario vea el significado. Barato, ya en el diseño.
3. **Diccionario léxico en contexto (pocos shots)** — inyectar 10-30 pares
   ES→lengua del diccionario descargado al prompt del LLM para las lenguas
   SIN motor dedicado. Impacto medio, esfuerzo medio.
4. **Voto entre backends** — bajo valor HOY: solo Groq produce algo (mal) en
   bajas lenguas; cuando haya 2 motores decentes, el voto sí paga.
5. **NLLB local (nllb-200-distilled-600M)** — corre en CPU pero NO cubre
   náhuatl/maya/zapoteco MX; solo quz/ayr/grn/swa… Útil para el subconjunto
   que sí cubre, no para el núcleo del proyecto.
6. **Post-edición con reglas por familia** — ortografía oficial (INALI) y
   glotalización como normalización pre-TTS. Esfuerzo medio, impacto medio
   (la voz mejora aunque el texto siga siendo dudoso).

## 3. Deuda técnica y modularización (sin romper la CLI)

- `conversor.py`: separar en `pipeline/` (stt, translate_backends,
  tts_engines, registry). NO hacerlo ahora: la CLI y `convert()` son la API
  pública que usa `app.py`; modularizar cuando haya un segundo consumidor.
- Estado global (`LANGUAGES`, `_TTS_CACHE`): aceptable en CLI single-file;
  si se vuelve servicio multiusuario, mover a config por request.
- `_key_chain` es correcto; solo documentar que los `.env` de otros proyectos
  NO se leen automáticamente (aislamiento intencional).

## 4. Tres experimentos baratos (corren hoy en esta Mac)

1. **Mapa del hueco**: `tools/score_translation.py --lang <X>` para
   yua/nhe/mam/zai/quz/ayr/grn → tabla de qué lenguas ya resuelve Google NMT
   vs cuáles siguen en ~0.0 con LLM. Es LA tabla para grants.
2. **Diccionario few-shot**: bajar un mini-diccionario ES→náhuatl (Wiktionary
   vía wiktextract, 30 entradas) → inyectar al prompt Groq → re-correr el
   scorer en `nah-hua`. Mide si el léxico en contexto sube el score.
3. **Whisper en lengua indígena**: pasar audio MMS generado (o YouTube con
   hablante) por Whisper `small` — ¿entiende náhuatl/maya o alucina? Define
   si el STT propio es factible o hay que esperar fine-tune.
