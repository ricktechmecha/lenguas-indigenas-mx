#!/usr/bin/env python3
"""
train_tts.py — Fine-tune de TTS para una lengua nueva (scaffold GPU).

Entrada : dataset/<iso>-tts/  (de `corpus_tool.py pack-tts`)
Salida  : ./models/tts-<iso>/  (checkpoint VITS compatible con conversor.py)

El fine-tuning de VITS/MMS no es un Trainer estándar de HF; la receta
probada por la comunidad es ylacombe/finetune-hf-vits, que adapta un
checkpoint MMS (o VITS base) a un dataset formato LJSpeech — que es
exactamente lo que produce `pack-tts`.

Setup en GPU (Colab A100/L4 o RunPod):

    git clone https://github.com/ylacombe/finetune-hf-vits
    cd finetune-hf-vits && pip install -r requirements.txt
    # sube tu dataset/<iso>-tts/ a esta carpeta

    python train_vits.py \
        --dataset_dir ../dataset/hch-tts \
        --base_checkpoint facebook/mms-tts-spa   # o el MMS de la familia más cercana
        --output_dir ../models/tts-hch \
        --language hch \
        --learning_rate 2e-4 --num_epochs 500 --batch_size 16

Tips reales (de la receta MMS):
  - Partir de un checkpoint MMS CERCANO en familia/ortografía mejora mucho
    (para lenguas MX, mms-tts-spa o el de la lengua hermana suelen servir).
  - 1h de audio limpio > 5h ruidoso. Silencios recortados, 1 frase por clip.
  - Si la lengua usa grafemas fuera del vocab del tokenizer, añade los
    caracteres (el repo permite extender el vocab — ver su README).

Después del entrenamiento:
    # El dir ./models/tts-hch queda en formato VitsModel+tokenizer.
    # En languages_extra.json:  "mms": "./models/tts-hch"
    # conversor.py lo carga con VitsModel.from_pretrained() sin cambios.

Validación honesta: genera 5 frases y que hablantes nativos las califiquen
inteligibilidad + naturalidad ANTES de publicar el checkpoint.
"""
import argparse, sys


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dataset", required=True, help="dataset/<iso>-tts/")
    p.add_argument("--base", default="facebook/mms-tts-spa")
    p.add_argument("--output", default=None)
    p.add_argument("--check", action="store_true",
                   help="solo verifica que el dataset tenga el formato correcto")
    a = p.parse_args()

    from pathlib import Path
    d = Path(a.dataset)
    ok = (d / "wavs").is_dir() and (d / "metadata_train.csv").exists()
    n = len(list((d / "wavs").glob("*.wav"))) if (d / "wavs").is_dir() else 0
    print(f"dataset: {d} — {n} wavs, metadata_train={'sí' if (d/'metadata_train.csv').exists() else 'NO'}")
    if not ok or n < 30:
        print("❌ dataset insuficiente (mín ~30 clips; ~1h recomendado).")
        sys.exit(1)
    print("✅ formato correcto — este scaffold delega en ylacombe/finetune-hf-vits.")
    print("   Lee el docstring de este archivo para los comandos exactos.")
    if a.check:
        return
    print("\n⚠️  Sin GPU local: ejecuta la receta en Colab/RunPod (ver docstring).")


if __name__ == "__main__":
    main()
