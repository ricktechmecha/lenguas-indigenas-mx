#!/usr/bin/env python3
"""
score_translation.py — score objetivo de traducción vía back-translation.

Traduce frases ES → lengua destino (Groq) y luego lengua → ES (Groq). Compara
la frase original contra el round-trip: si el significado sobrevive el viaje,
la traducción "conserva semántica". NO es validación nativa — es una métrica
aproximada y reproducible, útil para rankings internos y evidencia en grants.

Score por frase = similitud difflib (0-1) entre original y back-translation.
Además reporta: degenerada (guard existente), longitud, tiempo.

Uso:
  python3 tools/score_translation.py --lang zai
  python3 tools/score_translation.py --lang quz --out output_audio/score_quz.md
"""
import difflib, json, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from conversor import (translate, resolve_language, LANGUAGES, _looks_degenerate,
                       _translation_prompt, GROQ_KEYS, GROQ_MODEL, HTTP_UA)

SENTENCES = [
    "Buenos días, bienvenidos a la comunidad.",
    "El niño pequeño come pan en la casa de su abuela.",
    "Mañana iremos al mercado a comprar maíz y frijoles.",
    "La maestra enseña a leer a los estudiantes.",
    "El agua del río es importante para nuestra vida.",
]

def _groq(prompt: str) -> str:
    body = json.dumps({"model": GROQ_MODEL, "reasoning_effort": "low",
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions", data=body,
        headers={"Authorization": f"Bearer {GROQ_KEYS[0]}", "User-Agent": HTTP_UA,
                 "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"].strip()

def back_translate(text: str, lang_code: str) -> str:
    name = LANGUAGES.get(lang_code, {}).get("name", lang_code)
    # Preferir Google NMT para el regreso si hay par (misma razón que forward):
    # los LLM no conocen la mayoría de lenguas de bajos recursos.
    try:
        from gtranslate import google_translate, gt_code
        info = resolve_language(lang_code) or {}
        mms = info.get("mms") or ""
        slug = mms.rsplit("-tts-", 1)[-1] if "-tts-" in mms else (mms or lang_code)
        gt = gt_code(slug)
        if gt:
            bt = google_translate(text, "es", source=gt)
            if bt:
                return bt
    except Exception:
        pass
    prompt = (f"Translate the following text from {name} to Spanish. "
              f"Output ONLY the Spanish translation.\n\n{text}")
    try:
        return _groq(prompt)
    except Exception as e:
        return f"ERROR: {e}"

def sim(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a.lower().split(), b.lower().split()).ratio()

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--translator", default="auto",
                    help="auto (default, como producción) | groq | google | …")
    args = ap.parse_args()

    if not resolve_language(args.lang):
        print(f"❌ '{args.lang}' no resuelve"); sys.exit(1)
    name = LANGUAGES[args.lang]["name"]
    rows, scores = [], []
    for s in SENTENCES:
        t0 = time.time()
        fwd = translate(s, args.lang, args.translator) or ""
        back = back_translate(fwd, args.lang) if fwd else ""
        sc = sim(s, back)
        deg = _looks_degenerate(s, fwd)
        rows.append((s, fwd, back, sc, deg, time.time() - t0))
        scores.append(sc)
        print(f"  · score {sc:.2f}{'  ⚠️DEGEN' if deg else ''}: {fwd[:60]!r} → {back[:50]!r}")

    avg = sum(scores) / len(scores)
    out = Path(args.out or f"output_audio/score_{args.lang}.md")
    out.parent.mkdir(exist_ok=True)
    L = [f"# Score back-translation → {name} ({args.lang})",
         f"_{time.strftime('%Y-%m-%d %H:%M')} · motor {args.translator} · {len(SENTENCES)} frases_",
         f"\n## Promedio: **{avg:.2f}** / 1.00",
         "> Round-trip ES→lengua→ES. ~0.5+ conserva semántica aprox.; NO sustituye validación nativa.\n",
         "| # | Original | Traducción | Back-translation | score | deg | s |",
         "|---|---|---|---|---|---|---|"]
    for i, (s, f, b, sc, d, dt) in enumerate(rows, 1):
        esc = lambda x: x.replace("|", "\\|").replace("\n", " ")[:90]
        L.append(f"| {i} | {esc(s)} | {esc(f)} | {esc(b)} | {sc:.2f} | {'⚠️' if d else '—'} | {dt:.1f} |")
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"\n✅ {out} — promedio {avg:.2f}")

if __name__ == "__main__":
    main()
