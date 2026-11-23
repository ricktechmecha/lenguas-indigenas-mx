#!/usr/bin/env python3
"""
train_whisper.py — Fine-tune de Whisper para ASR en una lengua nueva (scaffold GPU).

Entrada : dataset/<iso>-asr/  (train.jsonl + val.jsonl con {"audio","sentence"})
Salida  : ./models/asr-<iso>/  (checkpoint Whisper)

Requiere GPU + `pip install transformers datasets librosa soundfile accelerate evaluate jiwer`.
En Colab el dataset se sube como carpeta o se monta Drive.

    python3 train_whisper.py --dataset dataset/hch-asr --iso hch \
        --base openai/whisper-small --output ./models/asr-hch --epochs 6

    python3 train_whisper.py --dataset dataset/hch-asr --eval-only \
        --model ./models/asr-hch     # imprime WER del checkpoint

Después: el checkpoint se usa para transcribir audio EN la lengua
(sentido inverso del conversor — subtitulado/doblaje inverso/corpus bootstrapping).
"""
import argparse, json, sys
from pathlib import Path


def load_jsonl(d: Path, split: str):
    f = d / f"{split}.jsonl"
    if not f.exists():
        return []
    return [json.loads(l) for l in f.read_text("utf-8").splitlines() if l.strip()]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", required=True)
    p.add_argument("--iso", default=None)
    p.add_argument("--base", default="openai/whisper-small")
    p.add_argument("--output", default=None)
    p.add_argument("--model", default=None, help="checkpoint a evaluar (--eval-only)")
    p.add_argument("--epochs", type=float, default=6)
    p.add_argument("--eval-only", action="store_true")
    a = p.parse_args()

    d = Path(a.dataset)
    train, val = load_jsonl(d, "train"), load_jsonl(d, "val")
    print(f"dataset {d}: {len(train)} train / {len(val)} val")
    if len(train) < 50:
        sys.exit("❌ <50 muestras — ASR necesita horas de audio; recolecta más.")

    if a.eval_only:
        try:
            import evaluate, librosa, torch  # noqa
            from transformers import WhisperForConditionalGeneration, WhisperProcessor, pipeline
        except ImportError:
            sys.exit("pip install transformers datasets librosa soundfile evaluate jiwer torch")
        model_id = a.model or a.base
        print(f"WER de {model_id} en {len(val)} muestras de val:")
        pipe = pipeline("automatic-speech-recognition", model=model_id)
        import evaluate as ev
        wer = ev.load("wer")
        refs, preds = [], []
        for r in val[:50]:  # muestra acotada para eval rápida
            pred = pipe(str(d / r["audio"]))["text"]
            refs.append(r["sentence"]); preds.append(pred)
        print(f"  WER ≈ {wer.compute(predictions=preds, references=refs):.2%}")
        return

    # ── Fine-tune real (GPU) — receta estándar HF para Whisper ──
    try:
        import torch
        from datasets import Audio, Dataset
        from transformers import (Seq2SeqTrainer, Seq2SeqTrainingArguments,
                                  WhisperForConditionalGeneration,
                                  WhisperProcessor)
    except ImportError:
        sys.exit("pip install transformers datasets librosa soundfile accelerate evaluate jiwer torch")

    iso = a.iso or d.name.split("-")[0]
    out = a.output or f"./models/asr-{iso}"
    processor = WhisperProcessor.from_pretrained(a.base)
    model = WhisperForConditionalGeneration.from_pretrained(a.base)
    model.config.forced_decoder_ids = None  # lengua nueva: no forzar tokens de idioma conocido

    def to_ds(rows):
        ds = Dataset.from_list([{"audio": str(d / r["audio"]), "sentence": r["sentence"]}
                                for r in rows])
        return ds.cast_column("audio", Audio(sampling_rate=16000))

    def prep(b):
        af = b["audio"]["array"]
        b["input_features"] = processor.feature_extractor(
            af, sampling_rate=16000).input_features[0]
        b["labels"] = processor.tokenizer(b["sentence"]).input_ids
        return b

    ds_train = to_ds(train).map(prep, remove_columns=["audio", "sentence"])
    ds_val = to_ds(val).map(prep, remove_columns=["audio", "sentence"]) if val else None

    def collate(feats):
        import torch
        inp = [{"input_features": f["input_features"]} for f in feats]
        batch = processor.feature_extractor.pad(inp, return_tensors="pt")
        lab = [{"input_ids": f["labels"]} for f in feats]
        lb = processor.tokenizer.pad(lab, return_tensors="pt")["input_ids"]
        lb[lb == processor.tokenizer.pad_token_id] = -100
        batch["labels"] = lb
        return batch

    args = Seq2SeqTrainingArguments(
        output_dir=out, per_device_train_batch_size=8, gradient_accumulation_steps=2,
        learning_rate=1e-5, num_train_epochs=a.epochs, fp16=torch.cuda.is_available(),
        eval_strategy="epoch" if ds_val else "no", save_strategy="epoch",
        logging_steps=25, report_to=[])
    Seq2SeqTrainer(model=model, args=args, train_dataset=ds_train,
                   eval_dataset=ds_val, data_collator=collate).train()
    model.save_pretrained(out); processor.save_pretrained(out)
    print(f"✅ checkpoint en {out} — evalúa con --eval-only antes de usarlo")


if __name__ == "__main__":
    main()
