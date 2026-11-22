#!/usr/bin/env python3
"""
eval_translation.py — benchmark de traducción por backend/modelo.

Traduce las MISMAS frases con Groq + cada modelo Ollama instalado (o un
subconjunto), mide tiempo, detecta salida degenerada y escribe una tabla
Markdown reproducible en output_audio/eval_<lang>.md — base para decidir qué
modelo local vale la pena fine-tunear (Fase 1 de PLAN_ENTRENAR_LLMS.md) y para
la validación por hablante nativo.

Uso:
  python3 tools/eval_translation.py --lang zap
  python3 tools/eval_translation.py --lang quz --models llama3.2:3b,qwen3:8b
  python3 tools/eval_translation.py --lang nah --all      # los ~28 modelos
"""
import json, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from conversor import (_translation_prompt, _looks_degenerate, resolve_language,
                       LANGUAGES, OLLAMA_HOST, GROQ_KEYS, GROQ_MODEL, HTTP_UA)

SENTENCES = [
    "Buenos días, bienvenidos a la comunidad.",
    "El niño pequeño come pan en la casa de su abuela.",
    "Mañana iremos al mercado a comprar maíz y frijoles.",
]

def ollama_models():
    try:
        with urllib.request.urlopen(f"{OLLAMA_HOST}/api/tags", timeout=5) as r:
            names = [m["name"] for m in json.loads(r.read()).get("models", [])]
        # fuera embeddings/vision/OCR que no generan texto de chat
        return [m for m in names if not any(
            x in m.lower() for x in ("embed", "minicpm", "moondream", "ocr"))]
    except Exception:
        return []

def ask_groq(prompt: str):
    if not GROQ_KEYS:
        return None, 0
    t0 = time.time()
    body = json.dumps({"model": GROQ_MODEL, "reasoning_effort": "low",
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions", data=body,
        headers={"Authorization": f"Bearer {GROQ_KEYS[0]}", "User-Agent": HTTP_UA,
                 "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())["choices"][0]["message"]["content"].strip(), time.time() - t0
    except Exception as e:
        return f"ERROR: {e}", time.time() - t0

def ask_ollama(model: str, prompt: str):
    t0 = time.time()
    body = json.dumps({"model": model, "stream": False,
                       "messages": [{"role": "user", "content": prompt}],
                       "options": {"temperature": 0.3}}).encode()
    req = urllib.request.Request(f"{OLLAMA_HOST}/api/chat", data=body,
                                 headers={"Content-Type": "application/json"},
                                 method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read())["message"]["content"].strip(), time.time() - t0
    except Exception as e:
        return f"ERROR: {e}", time.time() - t0

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="zap")
    ap.add_argument("--models", default="")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    if not resolve_language(args.lang):
        print(f"❌ '{args.lang}' no resuelve"); sys.exit(1)
    models = ollama_models()
    if args.models:
        models = [m for m in args.models.split(",") if m in models or True]
    elif not args.all:
        # default: modelos chicos (tag ≤4B parámetros) — corre en CPU razonable
        import re
        def _small(m):
            tag = m.split(":")[-1]
            n = re.search(r"(\d+\.?\d*)b", tag)
            return ("mini" in m.lower() or (n and float(n.group(1)) <= 4))
        models = [m for m in models if _small(m)][:4]
    backends = [("groq:" + GROQ_MODEL, ask_groq)] + \
               [(f"ollama:{m}", lambda p, m=m: ask_ollama(m, p)) for m in models]

    out = Path("output_audio") / f"eval_{args.lang}.md"
    out.parent.mkdir(exist_ok=True)
    lines = [f"# Eval traducción → {LANGUAGES[args.lang]['name']} ({args.lang})",
             f"_generado por tools/eval_translation.py — {time.strftime('%Y-%m-%d %H:%M')}_\n",
             f"Frases: {len(SENTENCES)} | Backends: {len(backends)}\n"]
    total_degen = {}
    for si, sent in enumerate(SENTENCES, 1):
        prompt = _translation_prompt(sent, args.lang)
        lines.append(f"\n## {si}. «{sent}»\n")
        lines.append("| Backend | s | Degenerada | Salida |")
        lines.append("|---|---|---|---|")
        for name, fn in backends:
            txt, dt = fn(prompt)
            if txt is None:
                lines.append(f"| {name} | — | — | (sin key/backend) |"); continue
            deg = _looks_degenerate(sent, txt)
            total_degen[name] = total_degen.get(name, 0) + deg
            safe = txt.replace("|", "\\|").replace("\n", " ")[:120]
            lines.append(f"| {name} | {dt:.1f} | {'⚠️ SÍ' if deg else 'no'} | {safe} |")
        print(f"  frase {si}/{len(SENTENCES)} lista")
    lines.append("\n## Resumen\n")
    for name, d in total_degen.items():
        lines.append(f"- {name}: {d}/{len(SENTENCES)} degeneradas")
    lines.append("\n**Pendiente:** calidad real la valida un hablante nativo "
                 "(campo `validado_por_hablante` en el pack de lengua).\n")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ {out}")

if __name__ == "__main__":
    main()
