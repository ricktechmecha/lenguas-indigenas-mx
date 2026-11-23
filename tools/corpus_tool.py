#!/usr/bin/env python3
"""
corpus_tool.py — Pipeline de corpus consentido → datasets de entrenamiento.

Misión: que "entrenar una lengua nueva" sea un proceso de ALIMENTAR DATOS,
no de escribir código. Estructura por lengua:

    corpus/<iso639_3>/
    ├── CONSENT.json      # consentimiento comunitario (OBLIGATORIO)
    ├── wavs/             # grabaciones de hablante(s) — para TTS y ASR
    ├── metadata.csv      # archivo|transcripción            — para TTS y ASR
    └── parallel_es.csv   # español|lengua                   — para traducción (MT)

Uso:
    python3 tools/corpus_tool.py init hch          # crea esqueleto + consentimiento
    python3 tools/corpus_tool.py validate hch      # ¿los datos están bien?
    python3 tools/corpus_tool.py status            # tabla de todas las lenguas
    python3 tools/corpus_tool.py pack-tts hch      # → dataset/hch-tts (VITS/MMS)
    python3 tools/corpus_tool.py pack-asr hch      # → dataset/hch-asr (Whisper)
    python3 tools/corpus_tool.py pack-mt  hch      # → dataset/hch-mt  (NLLB)

Solo stdlib. La normalización de audio usa `afconvert` (nativo macOS) o
`ffmpeg` si existe; si ninguno está, los wavs se copian tal cual con aviso.
"""
import csv, json, random, shutil, subprocess, sys, wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus"
DATASET = ROOT / "dataset"

# Extensiones de audio aceptadas en corpus/<iso>/wavs/
WAV_EXTS = {".wav", ".aiff", ".aif", ".m4a", ".mp3", ".flac", ".ogg"}

CONSENT_TEMPLATE = {
    "iso639_3": "",
    "comunidad": "",
    "hablantes": [{"nombre": "", "edad": None, "consentimiento": "pendiente"}],
    "licencia_datos": "CC-BY-4.0",
    "uso_permitido": ["entrenar modelos TTS/ASR/MT open-source"],
    "uso_prohibido": ["venta de datos", "voces comerciales sin permiso"],
    "contacto_comunidad": "",
    "fecha": "",
    "notas": "Documentar aquí cómo se obtuvo el consentimiento (asamblea, carta, audio)."
}

CONSENT_REQUIRED = ("iso639_3", "comunidad", "licencia_datos", "contacto_comunidad", "fecha")


def lang_dir(iso: str) -> Path:
    return CORPUS / iso.strip().lower()


# ─── init ────────────────────────────────────────────────────────────────────
def cmd_init(iso: str):
    d = lang_dir(iso)
    (d / "wavs").mkdir(parents=True, exist_ok=True)
    c = dict(CONSENT_TEMPLATE); c["iso639_3"] = iso
    (d / "CONSENT.json").write_text(json.dumps(c, ensure_ascii=False, indent=2), "utf-8")
    (d / "metadata.csv").write_text("archivo|transcripcion\n", "utf-8")
    (d / "parallel_es.csv").write_text("español|lengua\n", "utf-8")
    (d / "README.md").write_text(f"""# Corpus — {iso}

## Qué va aquí

| Archivo | Para qué | Formato |
|---|---|---|
| `CONSENT.json` | Soberanía de datos — SIN ESTO NO SE ENTRENA | ver plantilla |
| `wavs/*.wav` | Voz del/de los hablante(s) → TTS + ASR | 1 frase por archivo, 5-15s |
| `metadata.csv` | `archivo\\|transcripción` de cada wav | separador `\\|` |
| `parallel_es.csv` | `español\\|{iso}` pares de traducción | separador `\\|` |

## Mínimos orientativos

- **TTS (voz propia):** ~1h de audio limpio, 1 hablante (más = mejor)
- **ASR (entender la lengua):** ~10h transcritas (con 2-3h ya se puede evaluar)
- **MT (traducir):** ~5,000 pares de frases para fine-tune decente

Después: `python3 tools/corpus_tool.py validate {iso}` y `pack-*`.
""", "utf-8")
    print(f"✅ corpus/{iso}/ creado — llena CONSENT.json ANTES de grabar nada")


# ─── validate ────────────────────────────────────────────────────────────────
def _wav_seconds(p: Path) -> float:
    try:
        with wave.open(str(p)) as w:
            return w.getnframes() / w.getframerate()
    except Exception:
        return -1.0  # no es wav pcm legible (m4a/mp3…)


def cmd_validate(iso: str) -> bool:
    d = lang_dir(iso)
    errs, warns = [], []
    if not d.is_dir():
        print(f"❌ no existe corpus/{iso}/ — corre `init {iso}`"); return False

    # 1) Consentimiento — bloqueante
    consent = d / "CONSENT.json"
    if not consent.exists():
        errs.append("falta CONSENT.json")
    else:
        try:
            c = json.loads(consent.read_text("utf-8"))
            for k in CONSENT_REQUIRED:
                if not c.get(k): errs.append(f"CONSENT.json: campo vacío '{k}'")
            spk = c.get("hablantes") or []
            if not spk or all(s.get("consentimiento") != "otorgado" for s in spk):
                warns.append("CONSENT.json: ningún hablante con consentimiento='otorgado'")
        except Exception as e:
            errs.append(f"CONSENT.json inválido: {e}")

    # 2) Audio + metadata
    wavs = sorted(p for p in (d / "wavs").glob("*") if p.suffix.lower() in WAV_EXTS) if (d / "wavs").exists() else []
    meta = {}
    if (d / "metadata.csv").exists():
        for row in csv.reader((d / "metadata.csv").read_text("utf-8").splitlines(), delimiter="|"):
            if len(row) >= 2 and row[0] != "archivo":
                meta[row[0].strip()] = row[1].strip()
    total_s, sin_texto, sin_wav = 0.0, [], []
    for p in wavs:
        s = _wav_seconds(p)
        if s > 0: total_s += s
        if p.name not in meta: sin_texto.append(p.name)
    for name in meta:
        if name != "archivo" and not (d / "wavs" / name).exists(): sin_wav.append(name)
    if wavs and sin_texto: warns.append(f"{len(sin_texto)} wavs sin fila en metadata.csv: {sin_texto[:3]}…")
    if meta and sin_wav: warns.append(f"{len(sin_wav)} filas de metadata sin wav: {sin_wav[:3]}…")
    if wavs and total_s and total_s < 600: warns.append(f"solo {total_s/60:.1f} min de audio — TTS necesita ~1h")

    # 3) Pares de traducción
    pairs = 0
    if (d / "parallel_es.csv").exists():
        for row in csv.reader((d / "parallel_es.csv").read_text("utf-8").splitlines(), delimiter="|"):
            if len(row) >= 2 and row[0] != "español" and row[0].strip() and row[1].strip():
                pairs += 1
    if pairs and pairs < 1000: warns.append(f"solo {pairs} pares de traducción — MT necesita ~5,000")

    # Reporte
    print(f"\n📋 corpus/{iso}")
    print(f"   consentimiento : {'✅' if not any('CONSENT' in e for e in errs) else '❌'}")
    print(f"   wavs           : {len(wavs)} archivos ({total_s/60:.1f} min legibles)")
    print(f"   metadata       : {len(meta)} filas")
    print(f"   pares MT       : {pairs}")
    for w in warns: print(f"   ⚠️  {w}")
    for e in errs:  print(f"   ❌ {e}")
    ok = not errs
    print(f"\n{'✅ listo para pack-*' if ok else '❌ corrige los errores antes de entrenar'}")
    return ok


# ─── packing ─────────────────────────────────────────────────────────────────
def _to_wav_22k(src: Path, dst: Path) -> bool:
    """Normaliza a WAV mono 22050Hz (formato VITS/MMS)."""
    if src.suffix.lower() == ".wav":
        try:
            with wave.open(str(src)) as w:
                if w.getframerate() == 22050 and w.getnchannels() == 1 and w.getsampwidth() == 2:
                    shutil.copyfile(src, dst); return True
        except Exception:
            pass
    conv = shutil.which("afconvert")
    if conv:
        tmp = dst.with_suffix(".aiff")
        if subprocess.run([conv, "-f", "WAVE", "-d", "LEI16@22050", "-c", "1",
                           str(src), str(dst)], capture_output=True).returncode == 0:
            tmp.unlink(missing_ok=True); return True
    ff = shutil.which("ffmpeg")
    if ff:
        return subprocess.run([ff, "-y", "-i", str(src), "-ar", "22050", "-ac", "1",
                               str(dst)], capture_output=True).returncode == 0
    return False


def _split(rows: list, val_frac: float = 0.05):
    random.Random(42).shuffle(rows)
    n = max(1, int(len(rows) * val_frac)) if len(rows) > 20 else 0
    return rows[n:], rows[:n]


def _load_pairs(d: Path, fname: str):
    p = d / fname
    if not p.exists(): return []
    return [r for r in csv.reader(p.read_text("utf-8").splitlines(), delimiter="|")
            if len(r) >= 2 and r[0].strip() and r[1].strip() and r[0] not in ("archivo", "español")]


def cmd_pack_tts(iso: str) -> bool:
    """wavs+metadata → dataset/<iso>-tts/ (formato LJSpeech/VITS: metadata.csv + wavs/22050)."""
    d = lang_dir(iso)
    if not cmd_validate(iso): return False
    meta = {r[0].strip(): r[1].strip() for r in _load_pairs(d, "metadata.csv")}
    out = DATASET / f"{iso}-tts"; wd = out / "wavs"
    if wd.exists(): shutil.rmtree(wd)
    wd.mkdir(parents=True)
    rows, skipped = [], []
    for name, text in meta.items():
        src = d / "wavs" / name
        dst = wd / (Path(name).stem + ".wav")
        if src.exists() and text and _to_wav_22k(src, dst):
            rows.append(f"{dst.stem}|{text}|{text}")
        else:
            skipped.append(name)
    train, val = _split(rows)
    (out / "metadata_train.csv").write_text("\n".join(train) + "\n", "utf-8")
    (out / "metadata_val.csv").write_text("\n".join(val) + "\n", "utf-8")
    print(f"\n📦 dataset/{iso}-tts/ — {len(train)} train + {len(val)} val, "
          f"{len(skipped)} omitidos (formato/texto)")
    print(f"   → entrena: ver train/README.md (fine-tune sobre facebook/mms-tts-{iso} o VITS base)")
    return True


def cmd_pack_asr(iso: str) -> bool:
    """wavs+metadata → dataset/<iso>-asr/ (JSONL {'audio','sentence'} para Whisper/ASR)."""
    d = lang_dir(iso)
    if not cmd_validate(iso): return False
    meta = {r[0].strip(): r[1].strip() for r in _load_pairs(d, "metadata.csv")}
    out = DATASET / f"{iso}-asr"; wd = out / "wavs"
    if wd.exists(): shutil.rmtree(wd)
    wd.mkdir(parents=True)
    rows, skipped = [], []
    for name, text in meta.items():
        src = d / "wavs" / name
        dst = wd / (Path(name).stem + ".wav")
        if src.exists() and text and _to_wav_22k(src, dst):
            rows.append({"audio": f"wavs/{dst.name}", "sentence": text})
        else:
            skipped.append(name)
    train, val = _split(rows)
    def jl(rs): return "\n".join(json.dumps(r, ensure_ascii=False) for r in rs) + "\n"
    (out / "train.jsonl").write_text(jl(train), "utf-8")
    (out / "val.jsonl").write_text(jl(val), "utf-8")
    print(f"\n📦 dataset/{iso}-asr/ — {len(train)} train + {len(val)} val, {len(skipped)} omitidos")
    print("   → entrena: train/train_whisper.py --dataset dataset/" + f"{iso}-asr")
    return True


def cmd_pack_mt(iso: str) -> bool:
    """parallel_es.csv → dataset/<iso>-mt/ (JSONL {'source':'spa','target':iso} para NLLB/seq2seq)."""
    d = lang_dir(iso)
    if not cmd_validate(iso): return False
    pairs = [(r[0].strip(), r[1].strip()) for r in _load_pairs(d, "parallel_es.csv")]
    if not pairs:
        print("❌ parallel_es.csv vacío — MT necesita pares español|lengua"); return False
    out = DATASET / f"{iso}-mt"; out.mkdir(parents=True, exist_ok=True)
    rows = [{"source_lang": "spa", "target_lang": iso, "source": es, "target": tg}
            for es, tg in pairs]
    train, val = _split(rows)
    def jl(rs): return "\n".join(json.dumps(r, ensure_ascii=False) for r in rs) + "\n"
    (out / "train.jsonl").write_text(jl(train), "utf-8")
    (out / "val.jsonl").write_text(jl(val), "utf-8")
    print(f"\n📦 dataset/{iso}-mt/ — {len(train)} train + {len(val)} val")
    print("   → entrena: train/train_mt.py --dataset dataset/" + f"{iso}-mt")
    return True


def cmd_status():
    print(f"\n{'lengua':<10} {'consent.':<9} {'wavs':<6} {'min':<7} {'meta':<6} {'pares-MT':<9}")
    print("-" * 52)
    for d in sorted(CORPUS.glob("*/")) if CORPUS.exists() else []:
        iso = d.name
        ok_c = "—"
        if (d / "CONSENT.json").exists():
            try:
                c = json.loads((d / "CONSENT.json").read_text("utf-8"))
                ok_c = "✅" if all(c.get(k) for k in CONSENT_REQUIRED) else "⚠️"
            except Exception:
                ok_c = "❌"
        wavs = [p for p in (d / "wavs").glob("*") if p.suffix.lower() in WAV_EXTS] if (d / "wavs").exists() else []
        mins = sum(s for p in wavs if (s := _wav_seconds(p)) > 0) / 60
        meta = len(_load_pairs(d, "metadata.csv"))
        pairs = len(_load_pairs(d, "parallel_es.csv"))
        print(f"{iso:<10} {ok_c:<9} {len(wavs):<6} {mins:<7.1f} {meta:<6} {pairs:<9}")
    print()


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__); return
    cmd, rest = args[0], args[1:]
    if cmd == "status":
        cmd_status(); return
    if not rest:
        print(f"uso: corpus_tool.py {cmd} <iso639_3>"); sys.exit(2)
    iso = rest[0].strip().lower()
    fn = {"init": cmd_init, "validate": cmd_validate,
          "pack-tts": cmd_pack_tts, "pack-asr": cmd_pack_asr, "pack-mt": cmd_pack_mt}.get(cmd)
    if not fn:
        print(f"comando desconocido: {cmd}"); sys.exit(2)
    sys.exit(0 if fn(iso) is not False else 1)


if __name__ == "__main__":
    main()
