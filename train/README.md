# Entrenamiento — corpus consentido → modelos propios

Este directorio contiene los scaffolds para entrenar las 3 piezas del pipeline
con los datasets que produce `tools/corpus_tool.py`. **Requieren GPU** (Colab,
Lambda, RunPod, o el GPU que financie el grant) — la Mac Intel solo sirve para
preparar y validar datos.

## Flujo completo por lengua

```bash
# 0) En la Mac (o donde recolecten):
python3 tools/corpus_tool.py init hch          # esqueleto + CONSENT.json
#    → grabar wavs/, llenar metadata.csv y parallel_es.csv, firmar CONSENT.json
python3 tools/corpus_tool.py validate hch      # datos + consentimiento OK
python3 tools/corpus_tool.py pack-tts hch      # → dataset/hch-tts/
python3 tools/corpus_tool.py pack-asr hch      # → dataset/hch-asr/
python3 tools/corpus_tool.py pack-mt  hch      # → dataset/hch-mt/

# 1) En GPU (Colab/RunPod — cada script trae su header con instrucciones):
python3 train_tts.py     --dataset dataset/hch-tts --base facebook/mms-tts-spa
python3 train_whisper.py --dataset dataset/hch-asr
python3 train_mt.py      --dataset dataset/hch-mt  --base facebook/nllb-200-distilled-600M

# 2) Integrar el checkpoint propio (¡sin tocar código!):
#    languages_extra.json:
#    { "hch": { "name": "Wixárika (voz comunitaria)",
#               "mms": "./models/tts-hch",          # dir local o repo HF
#               "gt": null, "custom_mt": "./models/mt-hch" } }
python3 conversor.py "Buenos días" --lang hch   # ya usa tu modelo
```

## Qué entrena cada pieza

| Script | Modelo base | Dataset | Resultado |
|---|---|---|---|
| `train_tts.py` | `facebook/mms-tts-*` o VITS base | `dataset/<iso>-tts` (~1h mín) | Voz propia de la lengua |
| `train_whisper.py` | `openai/whisper-small` | `dataset/<iso>-asr` (~10h ideal) | ASR que entiende la lengua |
| `train_mt.py` | `facebook/nllb-200-distilled-600M` | `dataset/<iso>-mt` (~5k pares) | Traductor español↔lengua |

## Evaluación antes de publicar

- **ASR:** WER en val set (`train_whisper.py --eval-only` lo imprime)
- **MT:** `tools/score_translation.py --lang <iso> --translator auto` + revisión humana
- **TTS:** que 2-3 hablantes nativos escuchen y califiquen (MOS informal)
- **Todo:** publicar checkpoint SOLO si `CONSENT.json` lo permite explícitamente

## Soberanía de datos (no negociable)

Los wavs y textos NO se suben a HuggingFace público ni a ningún servicio
sin que la comunidad lo autorice por escrito en `CONSENT.json`.
Los checkpoints entrenados sí pueden publicarse (no contienen audio crudo
reconstruible de forma trivial), pero solo con consentimiento documentado.
