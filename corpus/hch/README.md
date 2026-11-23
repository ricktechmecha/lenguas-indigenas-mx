# Corpus — hch

## Qué va aquí

| Archivo | Para qué | Formato |
|---|---|---|
| `CONSENT.json` | Soberanía de datos — SIN ESTO NO SE ENTRENA | ver plantilla |
| `wavs/*.wav` | Voz del/de los hablante(s) → TTS + ASR | 1 frase por archivo, 5-15s |
| `metadata.csv` | `archivo\|transcripción` de cada wav | separador `\|` |
| `parallel_es.csv` | `español\|hch` pares de traducción | separador `\|` |

## Mínimos orientativos

- **TTS (voz propia):** ~1h de audio limpio, 1 hablante (más = mejor)
- **ASR (entender la lengua):** ~10h transcritas (con 2-3h ya se puede evaluar)
- **MT (traducir):** ~5,000 pares de frases para fine-tune decente

Después: `python3 tools/corpus_tool.py validate hch` y `pack-*`.
