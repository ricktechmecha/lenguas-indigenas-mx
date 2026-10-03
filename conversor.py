#!/usr/bin/env python3
"""
Conversor de Texto/Video a Audio en Lenguas Indígenas de México
================================================================
Pipeline: YouTube URL / texto → MP3 → transcripción → traducción → audio en lengua indígena

Lenguas soportadas (vía Meta MMS-TTS):
  nah  - Náhuatl
  yua  - Maya Yucateco
  mix  - Mixteco
  zap  - Zapoteco (variante)
  oto  - Otomí / Hñähñu
  tzo  - Tzotzil
  tzh  - Tzeltal
  mam  - Mam (Maya)

Dependencias:
  pip install transformers soundfile yt-dlp playwright
  pip install scipy numpy  (para audio)
"""

import os, sys, json, time, subprocess, tempfile, base64
import urllib.request
from pathlib import Path
from typing import Optional

# ─── CONFIG ────────────────────────────────────────────────────────────────
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY", "")
HF_TOKEN   = os.getenv("HF_TOKEN", "")
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "output_audio"))

LANGUAGES = {
    "nah": {"name": "Náhuatl",        "mms": "facebook/mms-tts-nah", "gemini_hint": "náhuatl clásico de México central"},
    "yua": {"name": "Maya Yucateco",  "mms": "facebook/mms-tts-yua", "gemini_hint": "maya yucateco (maya peninsular)"},
    "mix": {"name": "Mixteco",        "mms": "facebook/mms-tts-mix", "gemini_hint": "mixteco (Tu'un savi)"},
    "zap": {"name": "Zapoteco",       "mms": "facebook/mms-tts-zap", "gemini_hint": "zapoteco del Valle de Oaxaca"},
    "oto": {"name": "Otomí",          "mms": "facebook/mms-tts-oto", "gemini_hint": "hñähñu / otomí del Valle del Mezquital"},
    "tzo": {"name": "Tzotzil",        "mms": "facebook/mms-tts-tzo", "gemini_hint": "tzotzil de Chiapas"},
    "tzh": {"name": "Tzeltal",        "mms": "facebook/mms-tts-tzh", "gemini_hint": "tzeltal de Chiapas"},
    "mam": {"name": "Mam",            "mms": "facebook/mms-tts-mam", "gemini_hint": "mam (lengua maya de Chiapas/Guatemala)"},
    "spa": {"name": "Español (demo)", "mms": None,                   "gemini_hint": "español"},
}

# ─── STEP 1: DESCARGA DE VIDEO ──────────────────────────────────────────────
def download_youtube(url: str, out_dir: Path) -> Optional[Path]:
    """Descarga audio de YouTube a MP3 usando yt-dlp con cookies de Chrome."""
    out_dir.mkdir(parents=True, exist_ok=True)
    out_template = str(out_dir / "%(id)s.%(ext)s")
    cmd = [
        "yt-dlp",
        "--cookies-from-browser", "chrome",
        "-f", "bestaudio[ext=m4a]/bestaudio/best",
        "--extract-audio", "--audio-format", "mp3", "--audio-quality", "128K",
        "-o", out_template,
        "--no-playlist", "-q", url
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        # Find output file
        mp3_files = list(out_dir.glob("*.mp3"))
        if mp3_files:
            mp3 = sorted(mp3_files, key=lambda f: f.stat().st_mtime)[-1]
            print(f"  ✅ Audio descargado: {mp3.name} ({mp3.stat().st_size // 1024}KB)")
            return mp3
        print(f"  ❌ yt-dlp: {result.stderr[:200]}")
        return None
    except Exception as e:
        print(f"  ❌ Error descarga: {e}")
        return None

# ─── STEP 2: TRANSCRIPCIÓN LOCAL CON WHISPER ────────────────────────────────
def transcribe_with_whisper(audio_path: Path, model: str = "small", language: str = "es") -> Optional[str]:
    """Transcribe audio localmente usando el CLI de whisper (openai-whisper via brew)."""
    import shutil, tempfile
    whisper_bin = shutil.which("whisper")
    if not whisper_bin:
        print("  ⚠️  whisper no encontrado — instala con: brew install openai-whisper")
        return None
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [
            whisper_bin, str(audio_path),
            "--model", model,
            "--language", language,
            "--output_format", "txt",
            "--output_dir", tmp,
            "--fp16", "False",
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            stem = Path(audio_path).stem
            txt_file = Path(tmp) / f"{stem}.txt"
            if txt_file.exists():
                text = txt_file.read_text(encoding="utf-8").strip()
                print(f"  ✅ Transcripción local Whisper ({len(text)} chars)")
                return text
            print(f"  ❌ Whisper sin output. stderr: {result.stderr[:200]}")
            return None
        except subprocess.TimeoutExpired:
            print("  ❌ Whisper timeout (>10min)")
            return None
        except Exception as e:
            print(f"  ❌ Error Whisper: {e}")
            return None

# ─── STEP 3: TRADUCCIÓN A LENGUA INDÍGENA ──────────────────────────────────
def translate_with_gemini(text: str, lang_code: str, retries: int = 3) -> Optional[str]:
    """Traduce texto a lengua indígena usando Gemini."""
    lang_info  = LANGUAGES[lang_code]
    lang_name  = lang_info["name"]
    lang_hint  = lang_info["gemini_hint"]
    
    prompt = f"""Traduce el siguiente texto al {lang_name} ({lang_hint}).

IMPORTANTE:
- Proporciona ÚNICAMENTE la traducción, sin explicaciones ni notas.
- Usa vocabulario auténtico y gramática correcta de la lengua.
- Si alguna palabra no tiene equivalente directo, usa el préstamo más común en esa lengua.
- Si el texto es muy largo, mantén el sentido completo.

Texto a traducir (español):
{text}

Traducción al {lang_name}:"""

    for attempt in range(retries):
        try:
            payload = {"contents": [{"parts": [{"text": prompt}]}],
                       "generationConfig": {"temperature": 0.3, "maxOutputTokens": 2000}}
            req = urllib.request.Request(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_KEY}",
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"}, method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                resp = json.loads(r.read())
            translation = resp["candidates"][0]["content"]["parts"][0]["text"].strip()
            print(f"  ✅ Traducido a {lang_name}: {translation[:80]}...")
            return translation
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(15 * (attempt + 1))
            else:
                print(f"  ❌ HTTP {e.code}")
                return None
        except Exception as e:
            print(f"  ❌ Error traducción: {e}")
            return None
    return None

# ─── STEP 4: TTS EN LENGUA INDÍGENA ─────────────────────────────────────────
def tts_mms_local(text: str, lang_code: str, out_path: Path) -> bool:
    """Genera audio usando Meta MMS-TTS (requiere transformers instalado)."""
    try:
        from transformers import VitsModel, AutoTokenizer
        import torch, scipy.io.wavfile as wavfile
        import numpy as np
        
        model_id = LANGUAGES[lang_code]["mms"]
        if not model_id:
            return False
        
        print(f"  🔊 Cargando modelo MMS-TTS: {model_id}")
        tokenizer = AutoTokenizer.from_pretrained(model_id, token=HF_TOKEN)
        model     = VitsModel.from_pretrained(model_id, token=HF_TOKEN)
        
        inputs  = tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            output = model(**inputs).waveform
        
        waveform = output.squeeze().numpy()
        wavfile.write(str(out_path), rate=model.config.sampling_rate,
                      data=(waveform * 32767).astype(np.int16))
        print(f"  ✅ Audio generado: {out_path.name}")
        return True
    except ImportError:
        print("  ⚠️  transformers no instalado — usa: pip install transformers scipy")
        return False
    except Exception as e:
        print(f"  ❌ Error TTS: {e}")
        return False

def tts_mac_say(text: str, out_path: Path) -> bool:
    """Fallback: TTS en español con `say` de macOS."""
    aiff_path = out_path.with_suffix(".aiff")
    try:
        subprocess.run(["say", "-v", "Paulina", "-o", str(aiff_path), text],
                       check=True, capture_output=True, timeout=60)
        subprocess.run(["ffmpeg", "-i", str(aiff_path), "-q:a", "4",
                        str(out_path), "-y"], check=True, capture_output=True, timeout=30)
        aiff_path.unlink(missing_ok=True)
        print(f"  ✅ Audio (español fallback): {out_path.name}")
        return True
    except Exception as e:
        print(f"  ❌ say fallback: {e}")
        return False

# ─── PIPELINE PRINCIPAL ──────────────────────────────────────────────────────
def convert(input_source: str, lang_code: str = "nah", output_name: str = None) -> dict:
    """
    Convierte texto o video de YouTube a audio en lengua indígena.
    
    Args:
        input_source: URL de YouTube o texto directo
        lang_code: código de lengua (nah, yua, mix, zap, oto, tzo, tzh, mam)
        output_name: nombre base para el archivo de salida
    
    Returns:
        dict con paths de archivos generados
    """
    lang_info = LANGUAGES.get(lang_code)
    if not lang_info:
        print(f"❌ Lengua '{lang_code}' no soportada. Disponibles: {list(LANGUAGES.keys())}")
        return {}
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    base_name = output_name or f"audio_{lang_code}_{int(time.time())}"
    
    result = {"lang": lang_code, "lang_name": lang_info["name"], "files": {}}
    
    print(f"\n{'='*60}")
    print(f"🌿 CONVERSOR LENGUAS INDÍGENAS DE MÉXICO")
    print(f"   Lengua: {lang_info['name']} ({lang_code})")
    print(f"   Fuente: {input_source[:60]}...")
    print(f"{'='*60}")
    
    # ── PASO 1: Obtener texto en español ──
    spanish_text = None
    
    if input_source.startswith(("http://", "https://", "www.")):
        print("\n📥 PASO 1: Descargando video...")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path  = Path(tmp)
            mp3_file  = download_youtube(input_source, tmp_path)
            if not mp3_file:
                print("❌ No se pudo descargar el video")
                return result
            
            # Save MP3
            mp3_dest = OUTPUT_DIR / f"{base_name}.mp3"
            mp3_dest.write_bytes(mp3_file.read_bytes())
            result["files"]["mp3"] = str(mp3_dest)
            
            print("\n📝 PASO 2: Transcribiendo audio (Whisper local)...")
            spanish_text = transcribe_with_whisper(mp3_dest)
    else:
        print("\n📝 PASO 1: Texto recibido directamente")
        spanish_text = input_source
    
    if not spanish_text:
        print("❌ Sin texto para procesar")
        return result
    
    # Save transcription/text
    txt_path = OUTPUT_DIR / f"{base_name}_es.txt"
    txt_path.write_text(spanish_text, encoding="utf-8")
    result["files"]["texto_es"] = str(txt_path)
    print(f"\n📄 Texto: {spanish_text[:100]}...")
    
    # ── PASO 2/3: Traducir ──
    step = 3 if "mp3" in result["files"] else 2
    print(f"\n🔄 PASO {step}: Traduciendo a {lang_info['name']}...")
    
    if lang_code == "spa":
        translation = spanish_text
    else:
        translation = translate_with_gemini(spanish_text, lang_code)
    
    if not translation:
        print("❌ Sin traducción")
        return result
    
    trad_path = OUTPUT_DIR / f"{base_name}_{lang_code}.txt"
    trad_path.write_text(translation, encoding="utf-8")
    result["files"]["texto_indigena"] = str(trad_path)
    
    # ── PASO 3/4: TTS ──
    step += 1
    print(f"\n🔊 PASO {step}: Generando audio en {lang_info['name']}...")
    
    audio_out = OUTPUT_DIR / f"{base_name}_{lang_code}.wav"
    
    # Try MMS-TTS first, fallback to say
    success = tts_mms_local(translation, lang_code, audio_out)
    if not success:
        print(f"  ⚠️  MMS-TTS no disponible — instalando dependencias...")
        print(f"      Ejecuta: pip install transformers scipy torch")
        print(f"  🔄 Usando fallback macOS say (en español)...")
        audio_out = OUTPUT_DIR / f"{base_name}_es_fallback.mp3"
        success = tts_mac_say(translation, audio_out)
    
    if success:
        result["files"]["audio"] = str(audio_out)
    
    # ── RESUMEN ──
    print(f"\n{'='*60}")
    print(f"✅ COMPLETADO — {lang_info['name']}")
    for k, v in result["files"].items():
        size = Path(v).stat().st_size // 1024 if Path(v).exists() else 0
        print(f"   {k}: {Path(v).name} ({size}KB)")
    print(f"{'='*60}\n")
    
    return result


# ─── CLI ─────────────────────────────────────────────────────────────────────
def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Conversor de Texto/Video a Audio en Lenguas Indígenas de México",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # Video de YouTube a Náhuatl
  python conversor.py "https://youtube.com/watch?v=XXX" --lang nah

  # Texto directo a Maya Yucateco
  python conversor.py "Hola, bienvenido a la comunidad" --lang yua

  # Listar lenguas disponibles
  python conversor.py --list-langs
        """
    )
    parser.add_argument("input", nargs="?", help="URL de YouTube o texto en español")
    parser.add_argument("--lang", "-l", default="nah",
                        help="Código de lengua destino (default: nah=Náhuatl)")
    parser.add_argument("--output", "-o", default=None,
                        help="Nombre base para archivos de salida")
    parser.add_argument("--list-langs", action="store_true",
                        help="Listar lenguas disponibles")
    parser.add_argument("--outdir", default="output_audio",
                        help="Directorio de salida (default: output_audio)")
    
    args = parser.parse_args()
    
    global OUTPUT_DIR
    OUTPUT_DIR = Path(args.outdir)
    
    if args.list_langs:
        print("\n🌿 LENGUAS INDÍGENAS DE MÉXICO DISPONIBLES\n")
        print(f"{'Código':<6} {'Nombre':<20} {'Modelo TTS'}")
        print("-"*55)
        for code, info in LANGUAGES.items():
            mms = info["mms"] or "— (usa español)"
            print(f"  {code:<6} {info['name']:<20} {mms}")
        print()
        return
    
    if not args.input:
        parser.print_help()
        return
    
    result = convert(args.input, args.lang, args.output)
    sys.exit(0 if result.get("files") else 1)


if __name__ == "__main__":
    main()
