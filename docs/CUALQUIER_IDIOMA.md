# Cualquier idioma del mundo — cómo homologar el pipeline

> El proyecto ya no está limitado a lenguas mexicanas. `--lang` acepta:
> 1. un código curado (`nah`, `yua`, `zap-val`…),
> 2. **cualquier ISO 639-3 con checkpoint MMS** (`que`, `arb`, `haw`… — ~999 verificados en `data/mms_checkpoints.json`), o
> 3. un perfil tuyo en `languages_extra.json`.

## Cómo resolver un idioma nuevo (receta de 5 pasos)

### 1. ¿Existe checkpoint MMS-TTS?
```bash
python3 conversor.py --list-mms          # catálogo local completo
python3 conversor.py "Hola" --lang que   # resolución automática
```
Si existe, el pipeline ya funciona de punta a punta — la calidad de la
traducción dependerá del backend (Groq/Gemini/Ollama) y de los recursos de
esa lengua. **La voz será real (MMS-TTS); la traducción puede tener errores.**

### 2. Dale un perfil decente (`languages_extra.json`)
Un código ISO genérico produce un prompt de traducción débil ("the language
with ISO 639-3 code que"). El `hint` es lo que más mejora la traducción —
escribe la variante exacta:

```json
"quz": {
  "name": "Quechua sureño",
  "mms": "facebook/mms-tts-quz",
  "hint": "quechua sureño, variante Cusco",
  "iso639_3": "quz",
  "glottocode": "cusc1236",
  "script": "latn",
  "fuentes": {"diccionario": "...", "fonemas": "..."},
  "licencia_datos": "...",
  "validado_por_hablante": false
}
```

### 3. Consigue el diccionario / léxico
| Fuente | Qué tiene | Licencia |
|---|---|---|
| **PanLex** (panlex.org) | Léxico pan-lingüístico, ~5,700 variedades | CC0/datos abiertos |
| **Wiktionary + wiktextract** | Diccionarios por lengua, con IPA y audio | CC BY-SA 3.0 |
| **Glosbe** | Diccionarios comunitarios + memoria de traducción | variada — verificar |
| **StarLing / Tower of Babel** | Léxicos históricos | académica |

### 4. Consigue el inventario de fonemas
| Fuente | Qué tiene |
|---|---|
| **PHOIBLE** (phoible.org) | Inventarios fonémicos de ~2,000 lenguas (IPA) |
| **eSpeak NG** | Tablas G2P de ~100 lenguas — útil como normalizador |
| **epitran** (`pip install epitran`) | Grafema→IPA para ~500 lenguas — corre local en la Mac |
| **WALS** (wals.info) | Rasgos tipológicos para el hint |

### 5. Si NO hay checkpoint MMS → camino de entrenamiento
Ver `docs/ENTRENAMIENTO_MODELOS.md` para la ruta completa. Resumen honesto:

- **TTS (VITS/MMS)**: fine-tune del checkpoint de una lengua hermana con
  ~30min–2h de audio + transcripción de UN hablante consentido. VITS es
  monohablante por checkpoint — se entrena uno por voz.
- **ASR (wav2vec2/XLSR)**: fine-tune con ~10h transcritas; corpus base en
  Common Voice / FLEURS / OpenSLR si existen para esa lengua.
- **Traducción (NLLB/LLM)**: LoRA/QLoRA con bitextos (FLORES-200,
  AmericasNLP, diccionario descargado → pares ejemplo).
- **Fonemas como puente**: si no hay texto suficiente, el inventario de
  PHOIBLE + reglas G2P de eSpeak/epitran homologan la entrada al formato
  que MMS espera.

## Reglas duras (ver AGENTS.md)
- **Validación humana**: `validado_por_hablante: true` solo cuando un
  hablante real haya evaluado la salida. Un LLM que "produce texto" no
  equivale a que el audio sea correcto.
- **Licencias**: anota la fuente y licencia de cada diccionario/corpus en
  el perfil antes de usarlo en datos de entrenamiento.
- **Soberanía de datos**: nunca presentar audio sintético como voz de la
  comunidad; las grabaciones para entrenar requieren consentimiento
  explícito y compensación.
- **Prueba 1 antes de batch** (regla de este repo).

## Estado vs. promesa (para grants)
- ✅ Funciona hoy: ~1,000 lenguas con TTS real vía MMS + traducción
  multi-backend + perfiles extensibles sin tocar código.
- 🔄 En desarrollo: descargadores de diccionario/fonemas, evaluación
  automática de traducción, corpus consentido.
- ⏳ Futuro (requiere datos+fondeo): fine-tunes por lengua, ASR propio,
  modelos entrenados directamente para cada comunidad.
