#!/usr/bin/env python3
"""
train_mt.py — Fine-tune de traducción español↔lengua (scaffold GPU).

Entrada : dataset/<iso>-mt/  (train.jsonl + val.jsonl con
          {"source_lang","target_lang","source","target"})
Salida  : ./models/mt-<iso>/  (checkpoint seq2seq)

Base recomendada: facebook/nllb-200-distilled-600M — 200 lenguas,
corre hasta en Colab gratis. Para lenguas fuera de NLLB, se re-etiquetan
con el code más cercano o se añade un special token (ver docs/NLLB).

    python3 train_mt.py --dataset dataset/hch-mt --iso hch \
        --base facebook/nllb-200-distilled-600M --output ./models/mt-hch

Después (integración sin código):
    languages_extra.json:  "custom_mt": "./models/mt-hch"
    → conversor.py lo usa como motor preferente para esa lengua
      (implementado en translate_ex: chequea 'custom_mt' del perfil).
"""
import argparse, json, sys
from pathlib import Path


def load_jsonl(d: Path, split: str):
    f = d / f"{split}.jsonl"
    return [json.loads(l) for l in f.read_text("utf-8").splitlines()
            if l.strip()] if f.exists() else []


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", required=True)
    p.add_argument("--iso", default=None)
    p.add_argument("--base", default="facebook/nllb-200-distilled-600M")
    p.add_argument("--output", default=None)
    p.add_argument("--epochs", type=float, default=10)
    a = p.parse_args()

    d = Path(a.dataset)
    train, val = load_jsonl(d, "train"), load_jsonl(d, "val")
    print(f"dataset {d}: {len(train)} pares train / {len(val)} val")
    if len(train) < 500:
        sys.exit("❌ <500 pares — MT útil empieza ~5,000; igual puedes probar la mecánica.")

    try:
        import torch
        from datasets import Dataset
        from transformers import (AutoModelForSeq2SeqLM, AutoTokenizer,
                                  DataCollatorForSeq2Seq, Seq2SeqTrainer,
                                  Seq2SeqTrainingArguments)
    except ImportError:
        sys.exit("pip install transformers datasets accelerate sacremoses torch")

    iso = a.iso or d.name.split("-")[0]
    out = a.output or f"./models/mt-{iso}"
    tok = AutoTokenizer.from_pretrained(a.base)
    model = AutoModelForSeq2SeqLM.from_pretrained(a.base)

    def prep(b):
        m = tok(b["source"], truncation=True, max_length=128)
        with tok.as_target_tokenizer():
            m["labels"] = tok(b["target"], truncation=True, max_length=128)["input_ids"]
        return m

    ds_train = Dataset.from_list(train).map(prep)
    ds_val = Dataset.from_list(val).map(prep) if val else None
    coll = DataCollatorForSeq2Seq(tok, model=model)
    args = Seq2SeqTrainingArguments(
        output_dir=out, per_device_train_batch_size=16,
        learning_rate=5e-5, num_train_epochs=a.epochs,
        fp16=torch.cuda.is_available(), eval_strategy="epoch" if ds_val else "no",
        save_strategy="epoch", logging_steps=25, report_to=[])
    Seq2SeqTrainer(model=model, args=args, train_dataset=ds_train,
                   eval_dataset=ds_val, data_collator=coll).train()
    model.save_pretrained(out); tok.save_pretrained(out)
    print(f"✅ checkpoint en {out}")
    print(f"   Integra: languages_extra.json → \"custom_mt\": \"{out}\"")
    print(f"   Evalúa: python3 tools/score_translation.py --lang {iso}")


if __name__ == "__main__":
    main()
