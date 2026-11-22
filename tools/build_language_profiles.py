#!/usr/bin/env python3
"""
Genera data/language_profiles.csv — la "tabla maestra" por lengua.

Fuentes (todas abiertas, CC BY 4.0):
  - WALS CLDF (cldf-datasets/wals): familia, género, orden de palabras,
    morfología. https://github.com/cldf-datasets/wals
  - data/mms_checkpoints.json: checkpoints MMS-TTS verificados.
  - conversor.LANGUAGES: nombres/hints curados MX.

Salida (CSV mínimo-pero-completo, abrible en Excel):
  iso639_3, mms, code, name, family, genus, macroarea,
  word_order, subj_verb, obj_verb, adposition, genitive, adj_noun,
  verb_synthesis, affix_position, hint

Uso:
  python3 tools/build_language_profiles.py           # descarga WALS a data/_wals/
  python3 tools/build_language_profiles.py --offline # usa data/_wals/ existente
"""
import csv, json, sys, urllib.request
from pathlib import Path

ROOT   = Path(__file__).resolve().parent.parent
WALS_D = ROOT / "data" / "_wals"
OUT    = ROOT / "data" / "language_profiles.csv"
BASE   = "https://raw.githubusercontent.com/cldf-datasets/wals/master/cldf/"

# Rasgos WALS que alimentan el prompt/estructura (ver docs/CUALQUIER_IDIOMA.md)
FEATURES = {
    "22A": "verb_synthesis",
    "26A": "affix_position",
    "81A": "word_order",
    "82A": "subj_verb",
    "83A": "obj_verb",
    "85A": "adposition",
    "86A": "genitive",
    "87A": "adj_noun",
}

def fetch(name: str) -> Path:
    p = WALS_D / name
    if not p.exists():
        WALS_D.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(BASE + name, p)
    return p

def main():
    offline = "--offline" in sys.argv
    files = {n: (WALS_D / n if offline and (WALS_D / n).exists() else fetch(n))
             for n in ("languages.csv", "values.csv", "codes.csv")}

    sys.path.insert(0, str(ROOT))
    from conversor import LANGUAGES  # nombres/hints curados

    mms_cat = json.loads((ROOT / "data" / "mms_checkpoints.json").read_text())

    langs = {}   # wals_code -> row base
    with open(files["languages.csv"], encoding="utf-8") as f:
        for r in csv.DictReader(f):
            langs[r["ID"]] = {
                "name": r["Name"], "family": r["Family"], "genus": r["Genus"],
                "macroarea": r["Macroarea"], "iso639_3": r["ISO639P3code"],
                "glottocode": r["Glottocode"],
            }

    code_name = {}  # code_id -> nombre legible (ej. 81A-2 -> "SOV")
    with open(files["codes.csv"], encoding="utf-8") as f:
        for r in csv.DictReader(f):
            code_name[r["ID"]] = r["Name"]

    feats = {}  # wals_code -> {col: value}
    wanted = set(FEATURES)
    with open(files["values.csv"], encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["Parameter_ID"] in wanted:
                feats.setdefault(r["Language_ID"], {})[FEATURES[r["Parameter_ID"]]] = \
                    code_name.get(r["Code_ID"], r["Value"])

    # Una fila por código con checkpoint MMS; WALS enriquece cuando hay match ISO.
    wals_by_iso = {v["iso639_3"]: k for k, v in langs.items() if v["iso639_3"]}
    rows = []
    for iso in sorted(set(mms_cat) | {LANGUAGES[c].get("iso", c) for c in LANGUAGES}):
        wals_id = wals_by_iso.get(iso)
        base = langs.get(wals_id, {}) if wals_id else {}
        feat = feats.get(wals_id, {}) if wals_id else {}
        row = {
            "iso639_3": iso,
            "mms": mms_cat.get(iso, ""),
            "wals_code": wals_id or "",
            "name": base.get("name", ""),
            "family": base.get("family", ""),
            "genus": base.get("genus", ""),
            "macroarea": base.get("macroarea", ""),
            "hint": "", "curated": "",
        }
        row.update({c: feat.get(c, "") for c in FEATURES.values()})
        rows.append(row)

    # Mezclar perfiles curados (nombre/hint/iso por alias como nah, zap-val)
    for code, info in LANGUAGES.items():
        mms = info.get("mms") or ""
        slug = mms.replace("facebook/mms-tts-", "") if "mms-tts-" in mms else code
        iso = slug.split("-")[0].split("_")[0]
        for row in rows:
            if row["iso639_3"] == iso:
                row["curated"] = code
                if info.get("hint") and not row["hint"]:
                    row["hint"] = info["hint"]
                if not row["name"]:
                    row["name"] = info.get("name", "")

    cols = ["iso639_3", "mms", "wals_code", "name", "family", "genus",
            "macroarea", "word_order", "subj_verb", "obj_verb", "adposition",
            "genitive", "adj_noun", "verb_synthesis", "affix_position",
            "curated", "hint"]
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    n_wals = sum(1 for r in rows if r["wals_code"])
    print(f"✅ {OUT.name}: {len(rows)} filas ({n_wals} con datos WALS)")
    for r in rows:
        if r["curated"]:
            print(f"   {r['curated']:<8} {r['iso639_3']:<5} {r['word_order']:<3} "
                  f"{r['family'][:28]:<28} {r['name'][:30]}")

if __name__ == "__main__":
    main()
