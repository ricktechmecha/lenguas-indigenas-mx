# Plan de recursos por tier — qué falta para cada idioma

> Cierre de investigación 2026-11-22. Complementa `LENGUAS_COBERTURA_MUNDIAL.md`.
> Esto es la lista que sustenta las solicitudes de fondeo: cada tier dice
> exactamente qué recurso falta y para qué.

## Estado del pipeline (veredicto honesto)

| Etapa | Estado | Detalle |
|---|---|---|
| Entrada: texto | ✅ | textarea o URL YouTube → yt-dlp |
| STT del idioma FUENTE | ✅ (mayores) | Whisper vía Groq/local — ES/EN/etc. bien |
| STT de lengua indígena (sentido inverso) | 🟡 | MMS tiene checkpoints ASR (~1,000 lenguas: `mms-1b-all`, `mms-lid-256`) — **investigar integración, no probado aún** |
| Traducción tier A (116) | ✅ | Google NMT dedicado |
| Traducción tier B (901) | 🔴 | Solo LLM — medido ≈0.01 en zapoteco. **El hueco real del proyecto** |
| Traducción tier C/D | 🔴 | Sin datos |
| Voz TTS | ✅/🟡 | MMS-TTS real para 999 checkpoints (incl. variantes por dialecto); tier C/D sin voz |
| Verificación | ✅ | cobertura de alfabeto + back-translation scorer |
| Entrega web | ✅ | `python3 app.py` → landing + cobertura + conversor |

## Doblaje de series/películas — qué falta (investigación pendiente)

Pipeline objetivo: audio ES/EN → Whisper → traducción → TTS por línea →
alineación temporal → mezcla → .wav/.mp4 doblado.

| Pieza | Estado | Qué falta |
|---|---|---|
| STT fuente | ✅ | Whisper (Groq) ya integrado |
| Traducción por segmentos | 🟡 | Funciona pero hay que trocear por línea/subtítulo y mantener contexto |
| TTS por línea | ✅ | `synthesize()` ya trocea por oraciones; falta API por segmento con timestamps |
| **Alineación temporal** | ❌ | La pieza que falta: que cada línea quepa en su escena. Opciones a evaluar: `aeneas` (forzado), `stable-ts`/`whisperx` (word timestamps), o TTS con duración estimada + time-stretch (ffmpeg `atempo`) |
| Mezcla/mux | ❌ | ffmpeg: loudnorm, ducking de música, mux de audio en mp4. Ingeniería, no investigación |
| Subtítulos | ❌ | Opcional: generar .srt en lengua destino (barato una vez hay traducción por línea) |
| STT indígena (doblaje inverso: audio indígena → texto) | 🟡 | MMS ASR existe para ~1,000 lenguas — probar `facebook/mms-1b-all` o checkpoints por lengua |

**Veredicto doblaje:** NO es "un modelo nuevo" — es pipeline de ingeniería sobre
piezas existentes. El cuello real sigue siendo traducción (tier B) y alineación.

## Qué pedir por tier (la solicitud de recursos)

### 🟢 Tier A — 116 lenguas (voz + traducción dedicada)
- **Falta:** validación humana (hablantes nativos revisan samples), más dominios
  (salud, educación, trámites — no solo frases sueltas), cobertura de variantes.
- **Pedido:** horas de revisión comunitaria + grabaciones de control para eval.

### 🟡 Tier B — 901 lenguas (voz sí, traducción no)
- **Falta:** LA traducción. Opciones reales:
  1. Corpus paralelo ES↔lengua (la más honesta y barata de conseguir:
     materiales existentes — libros, folletos, subtítulos, textos escolares).
  2. Diccionarios estructurados (Wiktionary/wiktextract por lengua — parcial).
  3. Fine-tune de NLLB-200 o LLM con LoRA usando el corpus anterior.
- **Pedido:** acceso a corpus textuales existentes + lexicógrafos/comunidad +
  GPU modesta (Colab/ Kaggle alcanzan para LoRA de 600M-3B).

### 🔵 Tier C — 3 lenguas MX (wixárika, tzotzil, tzeltal)
- **Falta:** TODO menos la idea. Voz: fine-tune VITS/MMS desde checkpoint de
  lengua vecina + corpus grabado con consentimiento. Traducción: igual que B.
- **Pedido:** **grabaciones consentidas** (el requisito #1 de Lacuna Fund) +
  GPU. Son las candidatas perfectas para el "primer fine-tune propio" del proyecto.

### 🔴 Tier D — ~6,880 lenguas
- **Falta:** stack completo. Ruta estándar por lengua:
  1. ¿Existe corpus? (Common Voice, FLEURS, OpenSLR, archivos comunitarios)
  2. Ortografía/alfabeto normalizado (fuentes: ISO 15924, alfabetos INALI/sil.org)
  3. Comunidad socia (consentimiento, gobernanza de datos — UNESCO IDIL)
  4. Voz: fine-tune VITS monohablante (~30-60 min de audio limpio) o adaptar MMS
  5. Oído: XLS-R-300M fine-tune o Whisper LoRA
  6. Traducción: NLLB si la lengua está en sus 200; si no, LoRA sobre LLM con
     diccionario + corpus paralelo
- **Pedido:** fondeo de datasets (Lacuna), cómputo (NLnet/Cloud credits),
  y la red de comunidades/socios locales.

## Lo que ya se puede presentar HOY

1. **Demo en vivo:** `python3 app.py` → texto/YouTube → audio real en maya,
   náhuatl Huasteca, zapoteco, k'ekchí, mam, quechua… (tier A, ~116 lenguas).
2. **La tabla mundial** de cobertura honesta (116/901/3/~6,880).
3. **La medición del hueco:** zapoteco 0.01 con LLM frontera → justifica el proyecto.
4. **La infraestructura:** registry universal, tipología WALS en prompts,
   fonemas PHOIBLE, scorer de back-translation, evaluación reproducible.
5. **La ruta técnica completa** para cada tier — no hay misterio, hay recursos.
