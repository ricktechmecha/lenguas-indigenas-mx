#!/usr/bin/env python3
"""
fetch_language_data.py — descarga el "pack de lengua" para un código ISO 639-3.

Para cada lengua genera data/languages/<iso>.json con:
  - inventario fonémico real (PHOIBLE, CC BY-SA — phoible.org)
  - orden de palabras + posición del verbo (WALS 81A + Grambank GB131-133,
    vía codesandletters.com/grammar CC BY 4.0)
  - fuentes de diccionario sugeridas (kaikki/wiktextract, Glosbe)
  - snippet listo para pegar en languages_extra.json

Uso:
  python3 tools/fetch_language_data.py quz            # una lengua
  python3 tools/fetch_language_data.py --all-curated  # todas las curadas
  python3 tools/fetch_language_data.py --refresh      # re-descarga cachés
"""
import csv, json, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PH_D = ROOT / "data" / "_phoible"
GB_D = ROOT / "data" / "_grambank"
OUT_D = ROOT / "data" / "languages"

URLS = {
    PH_D / "inventories.csv": "https://raw.githubusercontent.com/cldf-datasets/phoible/master/cldf/inventories.csv",
    PH_D / "values.csv":      "https://raw.githubusercontent.com/cldf-datasets/phoible/master/cldf/values.csv",
    PH_D / "parameters.csv":  "https://raw.githubusercontent.com/cldf-datasets/phoible/master/cldf/parameters.csv",
    PH_D / "languages.csv":   "https://raw.githubusercontent.com/cldf-datasets/phoible/master/cldf/languages.csv",
    GB_D / "word-order.csv":  "https://codesandletters.com/grammar/word-order/word-order-languages.csv",
}

def ensure_caches(refresh=False):
    for p, url in URLS.items():
        if refresh or not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            print(f"  ⬇ {p.name}")
            urllib.request.urlretrieve(url, p)

def _rows(path):
    with open(path, encoding="utf-8") as f:
        yield from csv.DictReader(f)

def phonemes_for(iso: str) -> dict:
    """Inventario(s) fonémico(s) PHOIBLE para un ISO 639-3."""
    glottos = [r["ID"] for r in _rows(PH_D / "languages.csv")
               if r.get("ISO639P3code") == iso]
    if not glottos:
        return {}
    seg_class = {r["ID"]: r.get("SegmentClass", "") for r in _rows(PH_D / "parameters.csv")}
    inv_meta = {r["ID"]: r for r in _rows(PH_D / "inventories.csv")}
    invs = {}
    for r in _rows(PH_D / "values.csv"):
        if r["Language_ID"] in glottos:
            invs.setdefault(r["Inventory_ID"], []).append(r)
    out = {}
    for inv_id, vals in invs.items():
        meta = inv_meta.get(inv_id, {})
        ph = {"consonants": [], "vowels": [], "tones": [], "other": []}
        for v in vals:
            cls = seg_class.get(v["Parameter_ID"], "")
            key = {"consonant": "consonants", "vowel": "vowels",
                   "tone": "tones"}.get(cls, "other")
            ph[key].append(v["Value"])
        out[meta.get("Name", inv_id)] = {
            "source": meta.get("Inventory_source_ID", "PHOIBLE"),
            "counts": {"phonemes": meta.get("count_phonemes"),
                       "consonants": meta.get("count_consonants"),
                       "vowels": meta.get("count_vowels"),
                       "tones": meta.get("count_tones")},
            "phonemes": {k: sorted(set(v)) for k, v in ph.items() if v},
        }
    return out

def word_order_for(iso: str) -> dict:
    """WALS 81A + Grambank verb position (archivo fusionado, clave = glottocode)."""
    by_glotto = {r["glottocode"]: r for r in _rows(GB_D / "word-order.csv")
                 if r.get("glottocode")}
    # el archivo no trae ISO; buscamos por glottocode vía PHOIBLE languages
    glottos = [r["ID"] for r in _rows(PH_D / "languages.csv")
               if r.get("ISO639P3code") == iso]
    for g in glottos:
        if g in by_glotto:
            r = by_glotto[g]
            return {"wals_81a": r.get("wals_81a_value") or None,
                    "verb_initial": r.get("grambank_gb131_verb_initial") == "1",
                    "verb_medial": r.get("grambank_gb132_verb_medial") == "1",
                    "verb_final":   r.get("grambank_gb133_verb_final") == "1",
                    "family": r.get("family"), "genus": r.get("genus"),
                    "macroarea": r.get("macroarea")}
    return {}

def build_pack(iso: str) -> dict:
    iso = iso.strip().lower()
    pack = {
        "iso639_3": iso,
        "phoneme_inventories": phonemes_for(iso),
        "word_order": word_order_for(iso),
        "dictionary_sources": {
            "wiktextract": f"https://kaikki.org/dictionary/{iso}/ (JSONL por lengua, CC BY-SA)",
            "glosbe": f"https://glosbe.com/en/{iso} (diccionario comunitario)",
            "nota": "PanLex API caída (2026-11); usar wiktextract o dumps panlex",
        },
        "fuentes_licencias": {
            "phonemes": "PHOIBLE (phoible.org) — CC BY-SA 4.0",
            "word_order": "WALS v2020.6 + Grambank v1.0.3 — CC BY 4.0",
        },
        "validado_por_hablante": False,
    }
    pack["_languages_extra_snippet"] = {
        "name": f"(revisar nombre ISO — {iso})",
        "mms": f"facebook/mms-tts-{iso}",
        "hint": "(escribe la variante exacta para mejorar la traducción)",
        "iso639_3": iso,
        "fuentes": {"fonemas": "PHOIBLE", "orden": "WALS/Grambank"},
        "validado_por_hablante": False,
    }
    return pack

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ensure_caches(refresh="--refresh" in sys.argv)
    if "--all-curated" in sys.argv:
        sys.path.insert(0, str(ROOT))
        from conversor import LANGUAGES
        args = [i["mms"].replace("facebook/mms-tts-", "").split("-")[0].split("_")[0]
                for i in LANGUAGES.values() if i.get("mms")]
    if not args:
        print(__doc__); return
    OUT_D.mkdir(parents=True, exist_ok=True)
    for iso in sorted(set(args)):
        pack = build_pack(iso)
        out = OUT_D / f"{iso}.json"
        out.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
        n_inv = len(pack["phoneme_inventories"])
        wo = pack["word_order"].get("wals_81a") or "—"
        print(f"  ✅ {iso}: {n_inv} inventario(s) fonémicos, orden {wo} → {out.name}")

if __name__ == "__main__":
    main()
