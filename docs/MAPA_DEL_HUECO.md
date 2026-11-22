# Mapa del hueco — scores reales de traducción

> Medido 2026-11-22 con `tools/score_translation.py` (5 frases, round-trip
> ES→lengua→ES, similitud de palabras). Reportes: `output_audio/score_*.md`.

## Resultado principal

| Lengua | LLM (Groq gpt-oss-120b) | Pipeline auto (Google NMT) |
|---|---|---|
| `yua` maya yucateco | 0.22 | **0.75** |
| `nah-hua` náhuatl Huasteca | 0.27 | **0.58** |
| `mam` mam | 0.13 | **0.59** |
| `kek` k'ekchí | 0.04 | **0.58** |
| `zai` zapoteco Istmo | **0.00** (se niega) | **0.75** |
| `quz` quechua | 0.32 | **0.65** |
| `ayr` aymara | 0.31 | **0.65** |
| `grn` guaraní | 0.49 | **0.70** |

**Conclusión medida:** los LLM frontera producen 0.00–0.49 (a menudo se
niegan o inventan); el NMT dedicado de Google produce round-trips
0.58–0.75 con texto real en la lengua (ortografía correcta: glotalizaciones,
apóstrofos, palabras como *waaj*, *lidxi*, *aru*).

## Advertencias honestas

1. **Circularidad:** auto usa Google ida y vuelta — el score mide fluidez y
   consistencia del NMT, NO exactitud frente al idioma real. La validación
   final sigue requiriendo hablante nativo.
2. El score de `kek` (0.58) puede estar inflado: Google 'kek' tiene cobertura
   parcial del k'ekchí.
3. `zai`→Google usa el código `zap` sin variante declarada — la salida usa
   léxico del Istmo (verificado por vocabulario) pero puede mezclar variantes.

## Qué significa para el proyecto

- **Tier A ya es usable HOY** para contenido donde "aproximadamente correcto"
  basta (difusión, avisos, material básico) — con disclaimer.
- El hueco real se concentra en **tier B sin par Google** (~885 lenguas):
  ahí el LLM sigue siendo el único motor y falla. Ese es el objetivo del
  fine-tune con corpus comunitario.
- Los scores Groq documentados arriba son la evidencia de "por qué se
  necesita el proyecto" para grants.
