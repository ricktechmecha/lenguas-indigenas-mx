#!/usr/bin/env python3
"""
build_coverage_matrix.py — genera docs/LENGUAS_COBERTURA_MUNDIAL.md

Clasifica cada lengua del registro (language_profiles.csv + mms_checkpoints +
GT_BY_MMS) en tiers de cobertura real:

  A ✅ Voz MMS + traducción dedicada (Google NMT)
  B 🔶 Voz MMS, traducción solo LLM (calidad baja en bajos recursos)
  C 📝 Solo texto (sin checkpoint MMS — p.ej. hch/tzo/tzh, o fuera de WALS/MMS)
  D ❌ Sin datos en el registro — el resto del mundo (~7,900 lenguas ISO 639-3)

Uso: python3 tools/build_coverage_matrix.py
"""
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from gtranslate import gt_code

OUT = ROOT / "docs" / "LENGUAS_COBERTURA_MUNDIAL.md"

ES_MACRO = {
    "Africa": "África", "Eurasia": "Eurasia", "Papunesia": "Papúa y Oceanía",
    "Américas": "Américas", "North America": "Américas", "South America": "Américas",
    "": "—",
}

def region_of(r):
    g, m = (r.get("genus") or ""), (r.get("macroarea") or "")
    if "Mexican" in g or "South American" in g: return "América Latina"
    if m in ES_MACRO: return ES_MACRO[m]
    if "Indo-European" in g or "Dravidian" in g or "Austroasiatic" in g or "Sino-Tibetan" in g or "Tai-Kadai" in g: return "Asia"
    if "Afroasiatic" in g or "Niger-Congo" in g or "Nilo-Saharan" in g or "Khoe" in g: return "África"
    if "Pama-Nyungan" in g or "Papuan" in g or "Austronesian" in g or "Trans-New Guinea" in g: return "Oceanía"
    return m or "—"

def esc(s): return (s or "—").replace("|", "\\|")

def main():
    rows = list(csv.DictReader(open(ROOT / "data" / "language_profiles.csv")))
    mms_cat = json.load(open(ROOT / "data" / "mms_checkpoints.json"))

    # MMS publica checkpoints por dialecto: 'mam-dialect_central', 'hus-…'.
    # Una lengua "tiene voz" si existe su ISO exacto o cualquier variante suya.
    def has_checkpoint(iso: str) -> bool:
        return iso in mms_cat or any(k.startswith(iso + "-") for k in mms_cat)

    import conversor as cv
    def curated_info(key: str):
        """Alias curado (nah→azz, hus→hus-dialect_…): nombre real y checkpoint."""
        e = cv.LANGUAGES.get(key)
        if not e:
            return None
        mms = (e.get("mms") or "").rsplit("-tts-", 1)
        base = mms[-1].split("-")[0] if len(mms) == 2 else ""
        return {"name": e.get("name"), "base": base,
                "voice": bool(e.get("mms")) or has_checkpoint(base)}

    tierA, tierB, tierC = [], [], []
    tier_of = {}
    for r in rows:
        iso = r["iso639_3"]
        name = r.get("name") or "—"
        reg = region_of(r)
        # Fila-alias sin metadatos WALS (nah, mix, zap-…): resolver por LANGUAGES
        if name == "—" or (not r.get("family") and not r.get("mms")):
            ci = curated_info(iso)
            if ci:
                name = ci["name"] or name
                has_voice = ci["voice"]
                ck_iso = ci["base"] or iso
            else:
                has_voice, ck_iso = has_checkpoint(iso), iso
        else:
            has_voice = has_checkpoint(iso) or bool(r.get("mms"))
            ck_iso = iso
        gt = gt_code(ck_iso) if has_voice else None
        line = {"iso": iso, "name": name, "region": reg,
                "family": r.get("family") or "—",
                "order": r.get("word_order") or "—", "google": gt or "—"}
        tier_of[iso] = ("A" if has_voice and gt else "B" if has_voice else "C")
        (tierA if has_voice and gt else tierB if has_voice else tierC).append(line)

    # stats
    n_total_iso = 7900  # ISO 639-3 vivas aprox (ethnologue/sil)
    out = []
    out.append("# Cobertura mundial de lenguas — matriz honesta\n")
    out.append("> Generado por `tools/build_coverage_matrix.py` — no editar a mano.\n")
    out.append("## Resumen\n")
    out.append("| Tier | Significado | Conteo |")
    out.append("|---|---|---|")
    out.append(f"| 🟢 **A** | Voz MMS + traducción NMT dedicada (Google) | **{len(tierA)}** |")
    out.append(f"| 🟡 **B** | Voz MMS, traducción solo LLM (baja calidad en bajos recursos) | **{len(tierB)}** |")
    out.append(f"| 🔵 **C** | Solo texto (sin checkpoint MMS) | **{len(tierC)}** |")
    out.append(f"| 🔴 **D** | Sin datos en el registro (resto de ISO 639-3) | **~{n_total_iso - len(rows)}** |")
    out.append("")
    out.append("> ⚠️ **Honestidad:** 'voz MMS' ≠ traducción buena. En tier B el LLM suele "
               "fallar o inventar (medido: zapoteco ≈ 0.01 en back-translation). "
               "Ninguna traducción está validada por hablante nativo.\n")

    def table(tier, title, note):
        out.append(f"\n## {title} — {len(tier)} lenguas\n")
        out.append(note + "\n")
        out.append("| ISO | Lengua | Región | Familia | Orden | Google |")
        out.append("|---|---|---|---|---|---|")
        for l in sorted(tier, key=lambda x: (x["region"], x["name"])):
            out.append(f"| `{l['iso']}` | {esc(l['name'])} | {esc(l['region'])} | {esc(l['family'])} | {l['order']} | {l['google']} |")
        out.append("")

    table(tierA, "🟢 Tier A — cobertura completa (voz + traducción)",
          "Traducción por NMT dedicado de Google Translate. Las de la tabla MX son las de mayor calidad relativa.")
    table(tierB, "🟡 Tier B — voz disponible, traducción débil",
          "MMS-TTS existe pero NO hay par Google verificado: la traducción depende del LLM (Groq/local). Revisar caso por caso; algunas (var. regionales) pueden usar el par de la lengua vecina con precaución.")
    table(tierC, "🔵 Tier C — solo texto",
          "Sin checkpoint MMS: el sistema entrega traducción (si el LLM puede) pero NO genera audio. Candidatas a fine-tune propio con corpus consentido.")

    out.append("\n## 🔴 Tier D — sin cobertura en el registro\n")
    out.append(f"Existen ~{n_total_iso:,} lenguas vivas en ISO 639-3; este registro cubre "
               f"{len(rows)} (las 999 con checkpoint MMS + {len(tierC)} adicionales de WALS). "
               "El resto (~6,800) no tiene ni voz MMS ni datos tipológicos cargados — son el "
               "universo de trabajo para la fase de datasets comunitarios. Ver "
               "`docs/CUALQUIER_IDIOMA.md` para agregar cualquier ISO vía `languages_extra.json`.\n")

    # México destacado
    # JSON para el frontend
    import json as _json
    (ROOT / "data" / "cobertura.json").write_text(_json.dumps(
        {"generated": "tools/build_coverage_matrix.py",
         "tiers": {"A": tierA, "B": tierB, "C": tierC}},
        ensure_ascii=False))
    mx_fams = ("Oto-Manguean","Mayan","Uto-Aztecan","Totonacan","Tequistlatecan","Huarpe","Corachol","Jicaque")
    mx = [l for l in tierA + tierB + tierC if l["family"] in mx_fams]
    out.append("\n## México — detalle por lengua\n")
    out.append("| ISO | Lengua | Tier | Google | Orden |")
    out.append("|---|---|---|---|---|")
    for l in sorted(mx, key=lambda x: x["name"]):
        out.append(f"| `{l['iso']}` | {esc(l['name'])} | {tier_of.get(l['iso'],'?')} | {l['google']} | {l['order']} |")
    out.append("")

    OUT.write_text("\n".join(out))
    print(f"OK → {OUT}  A={len(tierA)} B={len(tierB)} C={len(tierC)}")

if __name__ == "__main__":
    main()
