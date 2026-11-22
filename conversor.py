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
import urllib.request, urllib.error
from pathlib import Path
from typing import Optional

# ─── CONFIG ────────────────────────────────────────────────────────────────
def _load_dotenv():
    """Carga .env del cwd si existe (KEY=VALUE, sin comillas obligatorias)."""
    env_file = Path(".env")
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip().strip("'\"")
        if k and k not in os.environ:
            os.environ[k] = v

_load_dotenv()

def _key_chain(base: str, n: int = 5) -> list:
    """Junta BASE, BASE_2..BASE_n del entorno. Permite rotar keys gratis."""
    keys = []
    for suffix in [""] + [f"_{i}" for i in range(2, n + 1)]:
        k = os.getenv(f"{base}{suffix}", "").strip()
        if k:
            keys.append(k)
    return keys

GOOGLE_KEYS   = _key_chain("GOOGLE_API_KEY")
GROQ_KEYS     = _key_chain("GROQ_API_KEY")
OLLAMA_KEYS   = _key_chain("OLLAMA_API_KEY")   # ollama.com cloud (API de pago/créditos)
CEREBRAS_KEYS = _key_chain("CEREBRAS_API_KEY") # cerebras.ai (de pago tras trial)
HF_TOKEN      = os.getenv("HF_TOKEN", "")
OUTPUT_DIR    = Path(os.getenv("OUTPUT_DIR", "output_audio"))
OLLAMA_HOST   = os.getenv("OLLAMA_HOST", "http://localhost:11434")
LLAMA_MODEL   = os.getenv("LLAMA_MODEL", "llama3.1:8b")
GROQ_MODEL    = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
OCLOUD_MODEL  = os.getenv("OLLAMA_CLOUD_MODEL", "gemma4:31b")
CEREBRAS_MODEL= os.getenv("CEREBRAS_MODEL", "gpt-oss-120b")

# Groq sienta detrás de Cloudflare: un UA de navegador evita el bloqueo 1010
HTTP_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36")

# Modelos MMS-TTS verificados contra huggingface.co (2026-11-22).
# OJO: no existe mms-tts-{lengua} genérico para todas — MMS publica por variante
# (ISO 639-3 / sufijos -dialect_). Tzotzil (tzo) y Tzeltal (tzh) NO tienen
# checkpoint publicado.
LANGUAGES = {
    # ── lenguas principales ──
    "nah": {"name": "Náhuatl (Altiplano)",   "mms": "facebook/mms-tts-azz",                        "hint": "náhuatl del Altiplano de Puebla, México central"},
    "yua": {"name": "Maya Yucateco",         "mms": "facebook/mms-tts-yua",                        "hint": "maya yucateco (maya peninsular)"},
    "mix": {"name": "Mixteco de Alcozauca",  "mms": "facebook/mms-tts-xta",                        "hint": "mixteco de Alcozauca, Guerrero (Tu'un savi)"},
    "zap": {"name": "Zapoteco del Istmo",    "mms": "facebook/mms-tts-zai",                        "hint": "zapoteco del Istmo de Tehuantepec, Oaxaca"},
    "oto": {"name": "Otomí de Querétaro",    "mms": "facebook/mms-tts-otq",                        "hint": "otomí de Querétaro (hñähñu)"},
    "mam": {"name": "Mam",                   "mms": "facebook/mms-tts-mam-dialect_central",        "hint": "mam central (lengua maya de Chiapas/Guatemala)"},
    "hus": {"name": "Huasteco / Teenek",     "mms": "facebook/mms-tts-hus-dialect_centralveracruz","hint": "huasteco / teenek de Veracruz"},
    "maz": {"name": "Mazateco",              "mms": "facebook/mms-tts-maz",                        "hint": "mazateco de Oaxaca"},
    "tri": {"name": "Triqui de Copala",      "mms": "facebook/mms-tts-tri",                        "hint": "triqui de Copala, Oaxaca"},
    "cya": {"name": "Chatino de Nopala",     "mms": "facebook/mms-tts-cya",                        "hint": "chatino de Nopala, Oaxaca"},
    "hui": {"name": "Wixárika / Huichol",    "mms": "facebook/mms-tts-hui",                        "hint": "wixárika / huichol"},
    "huv": {"name": "Huave / Ikoots",        "mms": "facebook/mms-tts-huv",                        "hint": "huave / ikoots de San Mateo del Mar, Oaxaca"},
    "tsz": {"name": "Purépecha",             "mms": "facebook/mms-tts-tsz",                        "hint": "purépecha / p'urhépecha de Michoacán"},
    "toc": {"name": "Totonaco",              "mms": "facebook/mms-tts-toc",                        "hint": "totonaco de la Sierra Norte de Puebla"},
    "tpp": {"name": "Tepehua",               "mms": "facebook/mms-tts-tpp",                        "hint": "tepehua"},
    "mfy": {"name": "Mayo / Yoreme",         "mms": "facebook/mms-tts-mfy",                        "hint": "mayo / yoreme de Sonora y Sinaloa"},
    "cab": {"name": "Popoloca",              "mms": "facebook/mms-tts-cab",                        "hint": "popoloca / ngigua"},
    # ── variantes de náhuatl ──
    "nah-gro": {"name": "Náhuatl de Guerrero",          "mms": "facebook/mms-tts-ngu", "hint": "náhuatl de Guerrero"},
    "nah-oax": {"name": "Náhuatl del Norte de Oaxaca",  "mms": "facebook/mms-tts-nhy", "hint": "náhuatl del Norte de Oaxaca"},
    "nah-hua": {"name": "Náhuatl de la Huasteca",       "mms": "facebook/mms-tts-nhe", "hint": "náhuatl de la Huasteca oriental"},
    "nah-mor": {"name": "Náhuatl de Morelos/Oaxaca",    "mms": "facebook/mms-tts-nch", "hint": "náhuatl de la Huasteca (mms-tts-nch)"},
    "nah-mic": {"name": "Náhuatl de Michoacán",         "mms": "facebook/mms-tts-ncl", "hint": "náhuatl de Michoacán"},
    "nah-tla": {"name": "Náhuatl de Tlamacazapa",       "mms": "facebook/mms-tts-nuz", "hint": "náhuatl de Tlamacazapa, Guerrero"},
    # ── variantes de zapoteco y mixteco frecuentes ──
    "zap-val": {"name": "Zapoteco del Valle",   "mms": "facebook/mms-tts-zab", "hint": "zapoteco del Valle de Oaxaca (Tlacolula)"},
    "zap-sie": {"name": "Zapoteco de la Sierra","mms": "facebook/mms-tts-zaa", "hint": "zapoteco de la Sierra de Juárez"},
    "mix-ata": {"name": "Mixteco de Atatlahuca","mms": "facebook/mms-tts-mib", "hint": "mixteco de Atatlahuca, Oaxaca"},
    # ── demo ──
    "spa": {"name": "Español (demo)", "mms": None, "hint": "español"},
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

def transcribe_with_groq(audio_path: Path, language: str = "es") -> Optional[str]:
    """Transcribe con Groq Whisper API (gratis, ~segundos). Rota GROQ_API_KEY.._5."""
    boundary = "----conversorboundary"
    audio_bytes = audio_path.read_bytes()
    parts = []
    for name, val in [("model", "whisper-large-v3-turbo"), ("language", language),
                      ("response_format", "text")]:
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{val}\r\n'.encode())
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{audio_path.name}"\r\n'
                 f'Content-Type: audio/mpeg\r\n\r\n'.encode() + audio_bytes + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    body = b"".join(parts)
    for i, key in enumerate(GROQ_KEYS):
        try:
            req = urllib.request.Request(
                "https://api.groq.com/openai/v1/audio/transcriptions", data=body,
                headers={"Authorization": f"Bearer {key}", "User-Agent": HTTP_UA,
                         "Content-Type": f"multipart/form-data; boundary={boundary}"},
                method="POST")
            with urllib.request.urlopen(req, timeout=180) as r:
                text = r.read().decode("utf-8").strip()
            print(f"  ✅ Transcripción Groq Whisper ({len(text)} chars)")
            return text
        except urllib.error.HTTPError as e:
            print(f"  ⚠️  Groq STT key{i+1}: HTTP {e.code} — probando siguiente")
        except Exception as e:
            print(f"  ⚠️  Groq STT key{i+1}: {e}")
    return None

def transcribe(audio_path: Path, stt: str = "auto") -> Optional[str]:
    """'auto': Groq Whisper si hay key, si no Whisper local."""
    if stt in ("auto", "groq") and GROQ_KEYS:
        t = transcribe_with_groq(audio_path)
        if t or stt == "groq":
            return t
        print("  🔄 Groq STT falló — usando Whisper local...")
    if stt in ("auto", "local"):
        return transcribe_with_whisper(audio_path)
    return None

# ─── STEP 3: TRADUCCIÓN A LENGUA INDÍGENA ──────────────────────────────────
def _translation_prompt(text: str, lang_code: str) -> str:
    lang_info = LANGUAGES[lang_code]
    return f"""Translate the following text to {lang_info['name']} ({lang_info['hint']}).

RULES:
- Output ONLY the translation, no explanations or notes.
- Use authentic vocabulary and correct grammar of the language.
- If a word has no direct equivalent, use the most common loanword in that language.

Text (Spanish):
{text}

Translation to {lang_info['name']}:"""

def _chat_completion(url: str, keys: list, model: str, prompt: str,
                     extra: dict = None, label: str = "") -> Optional[str]:
    """POST OpenAI-compatible chat completions con rotación de keys."""
    payload = {"model": model, "temperature": 0.3,
               "messages": [{"role": "user", "content": prompt}]}
    if extra:
        payload.update(extra)
    body = json.dumps(payload).encode()
    for i, key in enumerate(keys):
        try:
            req = urllib.request.Request(
                url, data=body,
                headers={"Content-Type": "application/json",
                         "Authorization": f"Bearer {key}",
                         "User-Agent": HTTP_UA},
                method="POST")
            with urllib.request.urlopen(req, timeout=120) as r:
                resp = json.loads(r.read())
            text_out = resp["choices"][0]["message"].get("content", "").strip()
            if text_out:
                return text_out
        except urllib.error.HTTPError as e:
            tag = f"{label or url} key{i+1}"
            if e.code in (400, 401, 402, 403):
                print(f"  ⚠️  {tag}: HTTP {e.code} — key inválida/sin crédito, probando siguiente")
            elif e.code == 429:
                print(f"  ⚠️  {tag}: 429 rate limit — probando siguiente key")
            else:
                print(f"  ⚠️  {tag}: HTTP {e.code}")
            continue
        except Exception as e:
            print(f"  ⚠️  {label or url} key{i+1}: {e}")
            continue
    return None

def translate_with_gemini(text: str, lang_code: str, retries: int = 2) -> Optional[str]:
    """Traduce con Gemini, rotando GOOGLE_API_KEY.._5 (la cuota es por key)."""
    prompt = _translation_prompt(text, lang_code)
    for key in GOOGLE_KEYS:
        for attempt in range(retries):
            try:
                payload = {"contents": [{"parts": [{"text": prompt}]}],
                           "generationConfig": {"temperature": 0.3, "maxOutputTokens": 2000}}
                req = urllib.request.Request(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}",
                    data=json.dumps(payload).encode(),
                    headers={"Content-Type": "application/json"}, method="POST")
                with urllib.request.urlopen(req, timeout=30) as r:
                    resp = json.loads(r.read())
                translation = resp["candidates"][0]["content"]["parts"][0]["text"].strip()
                print(f"  ✅ Traducido (Gemini): {translation[:80]}...")
                return translation
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < retries - 1:
                    time.sleep(15 * (attempt + 1))
                elif e.code in (400, 401, 403):
                    print(f"  ⚠️  Gemini key …{key[-6:]}: HTTP {e.code} — probando siguiente")
                    break
                else:
                    print(f"  ⚠️  Gemini: HTTP {e.code}")
                    break
            except Exception as e:
                print(f"  ⚠️  Gemini: {e}")
                break
    return None

def translate_with_groq(text: str, lang_code: str) -> Optional[str]:
    """Groq cloud (gratis con cuenta) — gpt-oss-120b u otro modelo OpenAI-compatible."""
    t = _chat_completion("https://api.groq.com/openai/v1/chat/completions",
                         GROQ_KEYS, GROQ_MODEL, _translation_prompt(text, lang_code),
                         extra={"max_completion_tokens": 2000, "reasoning_effort": "low"},
                         label="Groq")
    if t:
        print(f"  ✅ Traducido (Groq {GROQ_MODEL}): {t[:80]}...")
    return t

def translate_with_ollama_cloud(text: str, lang_code: str) -> Optional[str]:
    """Ollama Cloud (ollama.com) — requiere créditos; gemma4/multimodal disponible."""
    t = _chat_completion("https://ollama.com/v1/chat/completions",
                         OLLAMA_KEYS, OCLOUD_MODEL, _translation_prompt(text, lang_code),
                         extra={"max_completion_tokens": 2000, "stream": False},
                         label="OllamaCloud")
    if t:
        print(f"  ✅ Traducido (Ollama Cloud {OCLOUD_MODEL}): {t[:80]}...")
    return t

def translate_with_cerebras(text: str, lang_code: str) -> Optional[str]:
    """Cerebras cloud — tier de pago tras trial."""
    t = _chat_completion("https://api.cerebras.ai/v1/chat/completions",
                         CEREBRAS_KEYS, CEREBRAS_MODEL, _translation_prompt(text, lang_code),
                         extra={"max_completion_tokens": 2000},
                         label="Cerebras")
    if t:
        print(f"  ✅ Traducido (Cerebras {CEREBRAS_MODEL}): {t[:80]}...")
    return t

def _ollama_local_model() -> Optional[str]:
    """Devuelve LLAMA_MODEL si está instalado, o el primer modelo llama* local."""
    try:
        req = urllib.request.Request(f"{OLLAMA_HOST}/api/tags")
        with urllib.request.urlopen(req, timeout=5) as r:
            models = [m["name"] for m in json.loads(r.read()).get("models", [])]
        if LLAMA_MODEL in models:
            return LLAMA_MODEL
        llamas = [m for m in models if "llama" in m.lower()]
        pick = (llamas or models or [None])[0]
        if pick and pick != LLAMA_MODEL:
            print(f"  ⚠️  {LLAMA_MODEL} no instalado — usando {pick}")
        return pick
    except Exception:
        return LLAMA_MODEL  # sin servicio; el caller reporta el error

def translate_with_llama(text: str, lang_code: str, retries: int = 2) -> Optional[str]:
    """Traduce con Llama local vía Ollama (sin API key, sin costo, sin nube).
    Requiere: `ollama serve` corriendo y un modelo llama descargado."""
    lang_name = LANGUAGES[lang_code]["name"]
    prompt    = _translation_prompt(text, lang_code)
    model     = _ollama_local_model()

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0.3},
    }
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                f"{OLLAMA_HOST}/api/chat",
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"}, method="POST"
            )
            with urllib.request.urlopen(req, timeout=180) as r:
                resp = json.loads(r.read())
            translation = resp["message"]["content"].strip()
            print(f"  ✅ Traducido a {lang_name} (Llama local): {translation[:80]}...")
            return translation
        except urllib.error.URLError as e:
            if attempt == 0:
                print(f"  ⚠️  Ollama no responde en {OLLAMA_HOST} — ejecuta `ollama serve`")
            else:
                print(f"  ❌ Error Llama/Ollama: {e}")
                return None
        except Exception as e:
            print(f"  ❌ Error Llama/Ollama: {e}")
            return None
    return None

def _looks_degenerate(src: str, out: str) -> bool:
    """Detecta traducciones alucinadas: loops de tokens o salida desproporcionada.
    Común en lenguas de bajos recursos — mejor fallar que sintetizar basura."""
    if len(out) > max(2000, len(src) * 8):
        return True
    toks = out.split()
    if len(toks) >= 20:
        from collections import Counter
        top = Counter(toks).most_common(1)[0][1]
        if top / len(toks) > 0.25:
            return True
    return False

# Orden 'auto': gratis primero (Groq), luego Gemini (si hay key), nubes de pago, local al final.
TRANSLATORS = {
    "groq":         (translate_with_groq,         GROQ_KEYS,     "GROQ_API_KEY"),
    "gemini":       (translate_with_gemini,       GOOGLE_KEYS,   "GOOGLE_API_KEY"),
    "ollama-cloud": (translate_with_ollama_cloud, OLLAMA_KEYS,   "OLLAMA_API_KEY"),
    "cerebras":     (translate_with_cerebras,     CEREBRAS_KEYS, "CEREBRAS_API_KEY"),
    "llama":        (translate_with_llama,        None,          "Ollama local"),
}
AUTO_ORDER = ["groq", "gemini", "ollama-cloud", "cerebras", "llama"]

def translate(text: str, lang_code: str, translator: str = "auto") -> Optional[str]:
    """Traduce con el motor elegido. 'auto' prueba cada backend con keys disponibles."""
    order = AUTO_ORDER if translator == "auto" else [translator]
    for name in order:
        fn, keys, env_hint = TRANSLATORS[name]
        if keys is not None and not keys:
            if translator != "auto":
                print(f"  ⚠️  {env_hint} no configurada")
            continue
        t = fn(text, lang_code)
        if t:
            if _looks_degenerate(text, t):
                print(f"  ⚠️  {name} produjo salida degenerada (loop/alucinación) — descartada")
                t = None
            else:
                return t
        if translator != "auto":
            return None
        print(f"  🔄 {name} falló — probando siguiente motor...")
    print("  ❌ Ningún traductor disponible. Opciones gratis:")
    print("     · Groq:  crea key en console.groq.com → export GROQ_API_KEY")
    print("     · Local: instala Ollama → ollama pull llama3.1:8b → --translator llama")
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
        hf_tok    = HF_TOKEN or None  # modelos MMS son públicos; "" rompe el header
        tokenizer = AutoTokenizer.from_pretrained(model_id, token=hf_tok)
        model     = VitsModel.from_pretrained(model_id, token=hf_tok)
        
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
def convert(input_source: str, lang_code: str = "nah", output_name: str = None,
            translator: str = "auto", stt: str = "auto") -> dict:
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
            
            print("\n📝 PASO 2: Transcribiendo audio...")
            spanish_text = transcribe(mp3_dest, stt)
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
        translation = translate(spanish_text, lang_code, translator)
    
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
    parser.add_argument("--translator", "-t", default="auto",
                        choices=["auto", "groq", "gemini", "ollama-cloud", "cerebras", "llama"],
                        help="Traductor: auto (prueba todos), groq (gratis), gemini, "
                             "ollama-cloud, cerebras, o llama (Ollama local)")
    parser.add_argument("--stt", default="auto", choices=["auto", "groq", "local"],
                        help="Transcripción: auto (Groq si hay key), groq (Whisper API), local (whisper CLI)")
    
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
    
    result = convert(args.input, args.lang, args.output, args.translator, args.stt)
    sys.exit(0 if result.get("files") else 1)


if __name__ == "__main__":
    main()
