#!/usr/bin/env python3
"""
Conversor de Texto/Video a Audio en Lenguas Indígenas de México
================================================================
Pipeline: YouTube URL / texto → MP3 → transcripción → traducción → audio en lengua indígena

Lenguas soportadas (vía Meta MMS-TTS):
  - 17 lenguas mexicanas curadas + variantes (ver LANGUAGES / --list-langs)
  - CUALQUIER código ISO 639-3 con checkpoint MMS (~1,100 lenguas del mundo)
    vía data/mms_checkpoints.json — ej: --lang que (quechua), --lang arb (árabe)
  - Perfiles propios en languages_extra.json (ver languages_extra.json.example)

Dependencias:
  pip install transformers soundfile yt-dlp playwright
  pip install scipy numpy  (para audio)
"""

import os, sys, json, time, subprocess, tempfile, base64, shutil
import urllib.request, urllib.error
from pathlib import Path
from typing import Optional

from gtranslate import google_translate, gt_code

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
# NOTA (verif. WALS/ISO 2026-11): corregidos varios códigos mal etiquetados —
# mms-tts-tri es Tiriyo (Surinam) NO Triqui; el triqui real es trc/trs.
# mms-tts-maz es Mazahua, no Mazateco (mazatecos reales: maj, mzi).
# mms-tts-cab es Garífuna, no Popoloca (popoloca real: pls).
# mms-tts-hui es Huli (Papúa N.G.); Wixárika (hch) NO tiene checkpoint.
LANGUAGES = {
    # ── lenguas principales ──
    "nah": {"name": "Náhuatl de Zacapoaxtla",  "mms": "facebook/mms-tts-azz",                        "hint": "náhuatl de la Sierra Norte de Puebla (Zacapoaxtla)"},
    "yua": {"name": "Maya Yucateco",           "mms": "facebook/mms-tts-yua",                        "hint": "maya yucateco (maya peninsular)"},
    "mix": {"name": "Mixteco de Alcozauca",    "mms": "facebook/mms-tts-xta",                        "hint": "mixteco de Alcozauca, Guerrero (Tu'un savi)"},
    "zap": {"name": "Zapoteco del Istmo",      "mms": "facebook/mms-tts-zai",                        "hint": "zapoteco del Istmo de Tehuantepec, Oaxaca (VSO)"},
    "oto": {"name": "Otomí de Querétaro",      "mms": "facebook/mms-tts-otq",                        "hint": "otomí de Querétaro (hñähñu)"},
    "mam": {"name": "Mam",                     "mms": "facebook/mms-tts-mam-dialect_central",        "hint": "mam central (lengua maya VSO de Chiapas/Guatemala)"},
    "hus": {"name": "Huasteco / Teenek",       "mms": "facebook/mms-tts-hus-dialect_centralveracruz","hint": "huasteco / teenek de Veracruz"},
    "maz": {"name": "Mazahua",                 "mms": "facebook/mms-tts-maz",                        "hint": "mazahua (jñatjo), Estado de México"},
    "maz-jal": {"name": "Mazateco de Jalapa de Díaz", "mms": "facebook/mms-tts-maj",                 "hint": "mazateco de Jalapa de Díaz, Oaxaca"},
    "maz-ixc": {"name": "Mazateco de Ixcatlán",      "mms": "facebook/mms-tts-mzi",                  "hint": "mazateco de Ixcatlán, Oaxaca"},
    "tri": {"name": "Triqui de Copala",        "mms": "facebook/mms-tts-trc",                        "hint": "triqui de Copala, Oaxaca"},
    "tri-chi": {"name": "Triqui de Chicahuaxtla","mms": "facebook/mms-tts-trs",                      "hint": "triqui de Chicahuaxtla, Oaxaca"},
    "cya": {"name": "Chatino de Nopala",       "mms": "facebook/mms-tts-cya",                        "hint": "chatino de Nopala, Oaxaca"},
    "huv": {"name": "Huave / Ikoots",          "mms": "facebook/mms-tts-huv",                        "hint": "huave / ikoots de San Mateo del Mar, Oaxaca"},
    "tsz": {"name": "Purépecha",               "mms": "facebook/mms-tts-tsz",                        "hint": "purépecha / p'urhépecha de Michoacán (SVO)"},
    "toc": {"name": "Totonaco",                "mms": "facebook/mms-tts-toc",                        "hint": "totonaco (Coyutla), Sierra Norte de Puebla/Veracruz"},
    "tpp": {"name": "Tepehua",                 "mms": "facebook/mms-tts-tpp",                        "hint": "tepehua de Pisaflores, Veracruz"},
    "mfy": {"name": "Mayo / Yoreme",           "mms": "facebook/mms-tts-mfy",                        "hint": "mayo / yoreme de Sonora y Sinaloa"},
    "pls": {"name": "Popoloca",                "mms": "facebook/mms-tts-pls",                        "hint": "popoloca de San Marcos Tlacoyalco / ngigua, Puebla"},
    "cab": {"name": "Garífuna",                "mms": "facebook/mms-tts-cab",                        "hint": "garífuna (Centroamérica: Honduras, Guatemala, Belice)"},
    # ── variantes de náhuatl ──
    "nah-gro": {"name": "Náhuatl de Guerrero",          "mms": "facebook/mms-tts-ngu", "hint": "náhuatl de Guerrero (Xalitla)"},
    "nah-oax": {"name": "Náhuatl del Norte de Oaxaca",  "mms": "facebook/mms-tts-nhy", "hint": "náhuatl del Norte de Oaxaca"},
    "nah-hua": {"name": "Náhuatl de la Huasteca",       "mms": "facebook/mms-tts-nhe", "hint": "náhuatl de la Huasteca oriental"},
    "nah-mor": {"name": "Náhuatl Huasteca Central",     "mms": "facebook/mms-tts-nch", "hint": "náhuatl de la Huasteca central (mms-tts-nch)"},
    "nah-mic": {"name": "Náhuatl de Michoacán",         "mms": "facebook/mms-tts-ncl", "hint": "náhuatl de Michoacán"},
    "nah-tla": {"name": "Náhuatl de Tlamacazapa",       "mms": "facebook/mms-tts-nuz", "hint": "náhuatl de Tlamacazapa, Guerrero"},
    # ── variantes de zapoteco y mixteco frecuentes ──
    "zap-val": {"name": "Zapoteco del Valle",   "mms": "facebook/mms-tts-zab", "hint": "zapoteco del Valle de Oaxaca (Tlacolula)"},
    "zap-sie": {"name": "Zapoteco de la Sierra","mms": "facebook/mms-tts-zaa", "hint": "zapoteco de la Sierra de Juárez"},
    "mix-ata": {"name": "Mixteco de Atatlahuca","mms": "facebook/mms-tts-mib", "hint": "mixteco de Atatlahuca, Oaxaca"},
    # ── sin checkpoint MMS (solo traducción, sin voz propia) ──
    "hch": {"name": "Wixárika / Huichol",      "mms": None,                                       "hint": "wixárika / huichol — SIN checkpoint MMS, candidato a entrenar"},
    "tzo": {"name": "Tzotzil",                 "mms": None,                                       "hint": "tzotzil — SIN checkpoint MMS, candidato a entrenar"},
    "tzh": {"name": "Tzeltal",                 "mms": None,                                       "hint": "tzeltal — SIN checkpoint MMS, candidato a entrenar"},
    # ── demo ──
    "spa": {"name": "Español (demo)", "mms": None, "hint": "español"},
}

# ─── RESOLUCIÓN UNIVERSAL DE LENGUA ─────────────────────────────────────────
# Orden: LANGUAGES (curado MX) → languages_extra.json (packs del usuario) →
# data/mms_checkpoints.json (cualquier ISO 639-3 con checkpoint MMS publicado).
_MMS_CATALOG: Optional[dict] = None

# Macrolenguas ISO 639-2/639-3 → variante MMS representativa.
# MMS publica por lengua individual, no por macrolengua.
LANG_ALIASES = {
    "que": "quz",   # Quechua → Quechua sureño (Cusco)
    "swa": "swh",   # Swahili → Swahili
    "aym": "ayr",   # Aymara → Aymara central
}

def _extra_languages() -> dict:
    """Packs de lengua del usuario: languages_extra.json en cwd o junto al script.
    Esquema: {"code": {"name": ..., "mms": "facebook/mms-tts-xxx"|null, "hint": ...}}"""
    for p in (Path("languages_extra.json"),
              Path(__file__).resolve().parent / "languages_extra.json"):
        if p.exists():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"  ⚠️  {p.name} inválido: {e}")
    return {}

def _mms_catalog() -> dict:
    """Catálogo local de checkpoints MMS (999 códigos verificados vs HF)."""
    global _MMS_CATALOG
    if _MMS_CATALOG is None:
        cat = Path(__file__).resolve().parent / "data" / "mms_checkpoints.json"
        try:
            _MMS_CATALOG = json.loads(cat.read_text(encoding="utf-8")) if cat.exists() else {}
        except Exception:
            _MMS_CATALOG = {}
    return _MMS_CATALOG

def resolve_language(code: str) -> Optional[dict]:
    """Resuelve un código de lengua a {name, mms, hint}. Cachea en LANGUAGES."""
    code = code.strip().lower()
    if code in LANGUAGES:
        return LANGUAGES[code]
    for code_key in (code, code.replace("-", "_")):
        extra = _extra_languages().get(code_key)
        if extra:
            info = {"name": extra.get("name", code_key),
                    "mms":  extra.get("mms"),
                    "hint": extra.get("hint", extra.get("name", code_key))}
            LANGUAGES[code_key] = info
            return info
    catalog = _mms_catalog()
    if code not in catalog and code in LANG_ALIASES and LANG_ALIASES[code] in catalog:
        alias = LANG_ALIASES[code]
        info = {"name": f"Lengua '{code}' (via {alias})",
                "mms":  catalog[alias],
                "hint": f"the language with ISO 639-3 code {alias}"}
        LANGUAGES[code] = info
        print(f"  🌍 '{code}' → variante MMS '{alias}' ({catalog[alias]})")
        return info
    if code in catalog:
        info = {"name": f"Lengua ISO 639-3 '{code}'",
                "mms":  catalog[code],
                "hint": f"the language with ISO 639-3 code {code}"}
        LANGUAGES[code] = info
        print(f"  🌍 '{code}' resuelto desde catálogo MMS → {catalog[code]}")
        print(f"      (sin perfil curado: agrega nombre/pista en languages_extra.json)")
        return info
    return None

def suggest_languages(code: str) -> list:
    """Códigos parecidos para el mensaje de error."""
    code = code.strip().lower()
    pool = list(LANGUAGES) + list(_extra_languages()) + list(_mms_catalog())
    return [c for c in pool if c.startswith(code[:2]) or code[:2] in c][:8]

# ─── STEP 1: DESCARGA DE VIDEO ──────────────────────────────────────────────
def download_youtube(url: str, out_dir: Path) -> Optional[Path]:
    """Descarga audio de YouTube con la lib yt_dlp (sin ffmpeg: Groq acepta m4a/webm).
    Usa cookies del navegador Chrome si están disponibles."""
    out_dir.mkdir(parents=True, exist_ok=True)
    out_template = str(out_dir / "%(id)s.%(ext)s")
    import yt_dlp
    base = {"format": "bestaudio/best", "outtmpl": out_template,
            "quiet": True, "no_warnings": True, "noplaylist": True}
    # cookies del navegador: si fallan (perfil bloqueado/permisos), reintentar sin ellas
    attempts = [dict(base, cookiesfrombrowser=("chrome",)), base]
    info = None
    last_err = None
    for opts in attempts:
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
            break
        except Exception as e:
            last_err = e
    if not info:
        print(f"  ❌ Error descarga YouTube: {last_err}")
        return None
    # localizar el archivo descargado por id+ext
    vid = info.get("id") or info.get("url", "").split("v=")[-1].split("&")[0]
    cands = sorted(out_dir.glob(f"{vid}.*"), key=lambda f: f.stat().st_mtime)
    audio = [f for f in cands if f.suffix in (".m4a", ".webm", ".mp3", ".opus", ".ogg")]
    pick = (audio or cands or [None])[-1]
    if pick:
        print(f"  ✅ Audio descargado: {pick.name} ({pick.stat().st_size // 1024}KB)")
        return pick
    print("  ❌ yt-dlp: no se encontró el archivo de audio")
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
    mime = {".mp3": "audio/mpeg", ".m4a": "audio/mp4", ".webm": "audio/webm",
            ".ogg": "audio/ogg", ".opus": "audio/ogg", ".wav": "audio/wav",
            ".flac": "audio/flac"}.get(audio_path.suffix.lower(), "audio/mpeg")
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{audio_path.name}"\r\n'
                 f'Content-Type: {mime}\r\n\r\n'.encode() + audio_bytes + b"\r\n")
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

# ─── PERFILES TIPOLÓGICOS (WALS → prompt) ──────────────────────────────────
_LANG_PROFILES: Optional[dict] = None

def _lang_profiles() -> dict:
    """Carga data/language_profiles.csv (generado por tools/build_language_profiles.py)."""
    global _LANG_PROFILES
    if _LANG_PROFILES is None:
        import csv
        p = Path(__file__).resolve().parent / "data" / "language_profiles.csv"
        try:
            _LANG_PROFILES = {r["iso639_3"]: r for r in csv.DictReader(p.open(encoding="utf-8"))}
        except Exception:
            _LANG_PROFILES = {}
    return _LANG_PROFILES

def _profile_for(code: str) -> Optional[dict]:
    """Devuelve la fila tipológica WALS del código resuelto (vía ISO del checkpoint)."""
    info = LANGUAGES.get(code) or resolve_language(code) or {}
    mms = info.get("mms") or ""
    slug = mms.replace("facebook/mms-tts-", "") if "mms-tts-" in mms else code
    iso = slug.split("-")[0].split("_")[0]
    return _lang_profiles().get(iso)

def _grammar_notes(code: str) -> str:
    """Convierte la fila WALS en notas de estructura para el prompt."""
    p = _profile_for(code) or {}
    notes = []
    if p.get("family"):
        notes.append(f"- Language family: {p['family']}" + (f" (genus: {p['genus']})" if p.get("genus") else ""))
    if p.get("word_order") and "No dominant" not in p["word_order"]:
        notes.append(f"- BASIC WORD ORDER: {p['word_order']} — restructure the sentence to this order; do NOT keep Spanish SVO.")
    if p.get("subj_verb"):
        notes.append(f"- Subject–verb: {p['subj_verb']}.")
    if p.get("obj_verb"):
        notes.append(f"- Object–verb: {p['obj_verb']}.")
    if p.get("adposition"):
        notes.append(f"- Adpositions: {p['adposition']}.")
    if p.get("genitive"):
        notes.append(f"- Possession: {p['genitive']}.")
    if p.get("adj_noun"):
        notes.append(f"- Adjective–noun order: {p['adj_noun']}.")
    if p.get("verb_synthesis"):
        notes.append(f"- Verbs: {p['verb_synthesis']} (mark person/tense on the verb accordingly).")
    if p.get("affix_position"):
        notes.append(f"- Morphology: {p['affix_position']} (attach affixes to the correct side of the stem).")
    if not notes:
        return ""
    return "\nGRAMMAR (typology from WALS, wals.info — follow it when composing the sentence):\n" + "\n".join(notes) + "\n"

# ─── STEP 3: TRADUCCIÓN A LENGUA INDÍGENA ──────────────────────────────────
def _translation_prompt(text: str, lang_code: str) -> str:
    lang_info = LANGUAGES[lang_code]
    return f"""Translate the following text to {lang_info['name']} ({lang_info['hint']}).
{_grammar_notes(lang_code)}
RULES:
- Output ONLY the translation, no explanations or notes.
- Use authentic vocabulary and correct grammar of the language — restructure word order to the target language, do not translate word-by-word in Spanish order.
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

def translate_with_google(text: str, lang_code: str) -> Optional[str]:
    """Google Translate (NMT dedicado). Solo para lenguas con par verificado
    MMS↔Google (ver gtranslate.GT_BY_MMS) o campo "gt" en languages_extra.json."""
    info = LANGUAGES[lang_code]
    code = info.get("gt") or gt_code(info.get("mms"))
    if not code:
        return None
    t = google_translate(text, code)
    if t:
        print(f"  ✅ Traducido (Google Translate '{code}'): {t[:80]}...")
    return t

def google_supported(lang_code: str) -> bool:
    info = LANGUAGES.get(lang_code) or {}
    return bool(info.get("gt") or gt_code(info.get("mms")))

_REFUSALS = ("i'm sorry", "i’m sorry", "i am sorry", "sorry, i can", "i can't provide",
             "i can’t provide", "i cannot provide", "lo siento", "no puedo proporcionar",
             "no dispongo de", "as an ai", "i don't have enough", "i don’t have enough")

def _looks_refusal(out: str) -> bool:
    """El LLM se negó o se disculpó en vez de traducir — NO es una traducción,
    y sintetizarla produciría audio falso."""
    head = out.strip().lower()[:160]
    return any(r in head for r in _REFUSALS)

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
    "google":       (translate_with_google,       None,          "Google Translate"),
    "groq":         (translate_with_groq,         GROQ_KEYS,     "GROQ_API_KEY"),
    "gemini":       (translate_with_gemini,       GOOGLE_KEYS,   "GOOGLE_API_KEY"),
    "ollama-cloud": (translate_with_ollama_cloud, OLLAMA_KEYS,   "OLLAMA_API_KEY"),
    "cerebras":     (translate_with_cerebras,     CEREBRAS_KEYS, "CEREBRAS_API_KEY"),
    "llama":        (translate_with_llama,        None,          "Ollama local"),
}
# NMT dedicado primero (cuando hay par verificado); LLMs después.
AUTO_ORDER = ["google", "groq", "gemini", "ollama-cloud", "cerebras", "llama"]

def translate_ex(text: str, lang_code: str, translator: str = "auto") -> tuple:
    """Traduce y devuelve (traducción | None, motor usado | None)."""
    order = AUTO_ORDER if translator == "auto" else [translator]
    for name in order:
        fn, keys, env_hint = TRANSLATORS[name]
        if keys is not None and not keys:
            if translator != "auto":
                print(f"  ⚠️  {env_hint} no configurada")
            continue
        if name == "google" and not google_supported(lang_code):
            if translator != "auto":
                print(f"  ⚠️  Google Translate no tiene par verificado para '{lang_code}'")
                return None, None
            continue
        t = fn(text, lang_code)
        if t:
            if _looks_degenerate(text, t):
                print(f"  ⚠️  {name} produjo salida degenerada (loop/alucinación) — descartada")
            elif name != "google" and _looks_refusal(t):
                print(f"  ⚠️  {name} se negó a traducir — descartado (no es una traducción)")
            else:
                return t, name
        if translator != "auto":
            return None, None
        print(f"  🔄 {name} falló — probando siguiente motor...")
    print("  ❌ Ningún traductor produjo una traducción utilizable.")
    print("     · Groq:  crea key en console.groq.com → export GROQ_API_KEY")
    print("     · Local: instala Ollama → ollama pull llama3.1:8b → --translator llama")
    return None, None

def translate(text: str, lang_code: str, translator: str = "auto") -> Optional[str]:
    """Traduce con el motor elegido. 'auto' prueba cada backend disponible."""
    return translate_ex(text, lang_code, translator)[0]

# ─── STEP 4: TTS EN LENGUA INDÍGENA ─────────────────────────────────────────
_TTS_CACHE: dict = {}
_APOSTROPHES = "'’ʼ‘ꞌ`´"

def _tts_load(model_id: str):
    """Carga (y cachea) tokenizer+modelo MMS — evita recargar en cada petición."""
    if model_id not in _TTS_CACHE:
        from transformers import VitsModel, AutoTokenizer
        print(f"  🔊 Cargando modelo MMS-TTS: {model_id}")
        hf_tok = HF_TOKEN or None  # modelos MMS son públicos; "" rompe el header
        _TTS_CACHE[model_id] = (AutoTokenizer.from_pretrained(model_id, token=hf_tok),
                                VitsModel.from_pretrained(model_id, token=hf_tok))
    return _TTS_CACHE[model_id]

def normalize_for_tts(text: str, vocab: set) -> tuple:
    """Adapta el texto al alfabeto que el checkpoint conoce y mide qué se pierde.
    MMS descarta en silencio los caracteres fuera de su vocabulario, lo que
    cambia la pronunciación (p.ej. saltillo/glotal escrito con otro apóstrofo).
    Devuelve (texto, {"coverage": 0-1, "dropped": [chars]})."""
    import unicodedata
    text = unicodedata.normalize("NFC", text)
    known_apos = [a for a in _APOSTROPHES if a in vocab]
    if known_apos:
        for a in _APOSTROPHES:
            if a not in vocab:
                text = text.replace(a, known_apos[0])
    letters = [c for c in text.lower() if c.isalpha() or c in _APOSTROPHES]
    dropped = sorted({c for c in letters if c not in vocab})
    lost = sum(1 for c in letters if c not in vocab)
    cov = 1 - lost / len(letters) if letters else 1.0
    return text, {"coverage": round(cov, 3), "dropped": dropped}

def _tts_chunks(text: str, limit: int = 220) -> list:
    """Oraciones cortas: VITS se degrada y gasta mucha RAM con entradas largas."""
    import re
    chunks, buf = [], ""
    for part in re.split(r"(?<=[.!?…;:])\s+|\n+", text.strip()):
        part = part.strip()
        if not part:
            continue
        while len(part) > limit:
            cut = part.rfind(" ", 0, limit)
            cut = cut if cut > 40 else limit
            chunks.append(part[:cut]); part = part[cut:].strip()
        if buf and len(buf) + len(part) + 1 > limit:
            chunks.append(buf); buf = part
        else:
            buf = f"{buf} {part}".strip()
    if buf:
        chunks.append(buf)
    return chunks

def synthesize(text: str, lang_code: str, out_path: Path) -> Optional[dict]:
    """MMS-TTS → .wav. Devuelve info {"coverage", "dropped", "seconds"} o None."""
    try:
        import torch, scipy.io.wavfile as wavfile
        import numpy as np
        model_id = LANGUAGES[lang_code]["mms"]
        if not model_id:
            return None
        tokenizer, model = _tts_load(model_id)
        text, info = normalize_for_tts(text, set(tokenizer.get_vocab()))
        if info["dropped"]:
            print(f"  ⚠️  Grafemas fuera del alfabeto del modelo (se omiten al hablar): "
                  f"{' '.join(info['dropped'])} — cobertura {info['coverage']:.0%}")
        rate = model.config.sampling_rate
        pause = np.zeros(int(rate * 0.25), dtype=np.float32)
        waves = []
        for chunk in _tts_chunks(text):
            inputs = tokenizer(chunk, return_tensors="pt")
            if inputs["input_ids"].shape[-1] == 0:
                continue
            with torch.no_grad():
                waves += [model(**inputs).waveform.squeeze().numpy(), pause]
        if not waves:
            print("  ❌ TTS: ningún carácter del texto está en el alfabeto del modelo")
            return None
        waveform = np.concatenate(waves[:-1])
        wavfile.write(str(out_path), rate=rate,
                      data=(np.clip(waveform, -1, 1) * 32767).astype(np.int16))
        info["seconds"] = round(len(waveform) / rate, 1)
        print(f"  ✅ Audio generado: {out_path.name} ({info['seconds']}s)")
        return info
    except ImportError:
        print("  ⚠️  transformers no instalado — usa: pip install transformers scipy")
        return None
    except Exception as e:
        print(f"  ❌ Error TTS: {e}")
        return None

def tts_mms_local(text: str, lang_code: str, out_path: Path) -> bool:
    """Genera audio usando Meta MMS-TTS (requiere transformers instalado)."""
    return synthesize(text, lang_code, out_path) is not None

def tts_mac_say(text: str, out_path: Path):
    """Fallback: TTS en español con `say` de macOS.
    Devuelve el Path del audio generado (mp3 con ffmpeg, m4a con afconvert)."""
    aiff_path = out_path.with_suffix(".aiff")
    try:
        subprocess.run(["say", "-v", "Paulina", "-o", str(aiff_path), text],
                       check=True, capture_output=True, timeout=60)
        if shutil.which("ffmpeg"):
            subprocess.run(["ffmpeg", "-i", str(aiff_path), "-q:a", "4",
                            str(out_path), "-y"], check=True, capture_output=True, timeout=30)
            final = out_path
        else:
            # afconvert es nativo de macOS: AIFF → M4A (AAC), sin ffmpeg
            final = out_path.with_suffix(".m4a")
            subprocess.run(["afconvert", "-f", "m4af", "-d", "aac",
                            str(aiff_path), str(final)],
                           check=True, capture_output=True, timeout=30)
        aiff_path.unlink(missing_ok=True)
        print(f"  ✅ Audio (español fallback): {final.name}")
        return final
    except Exception as e:
        print(f"  ❌ say fallback: {e}")
        return None

# ─── PIPELINE PRINCIPAL ──────────────────────────────────────────────────────
def convert(input_source: str, lang_code: str = "nah", output_name: str = None,
            translator: str = "auto", stt: str = "auto",
            on_step=None, fallback_say: bool = True) -> dict:
    """
    Convierte texto o video de YouTube a audio en lengua indígena.
    
    Args:
        input_source: URL de YouTube o texto directo
        lang_code: código de lengua (nah, yua, mix, zap, oto, tzo, tzh, mam)
        output_name: nombre base para el archivo de salida
    
    Returns:
        dict con paths de archivos generados
    """
    lang_info = resolve_language(lang_code)
    if not lang_info:
        sugg = suggest_languages(lang_code)
        print(f"❌ Lengua '{lang_code}' sin checkpoint MMS ni perfil.")
        print(f"   Curadas: {list(LANGUAGES.keys())}")
        print(f"   O cualquier ISO 639-3 con checkpoint MMS (--list-mms).")
        if sugg:
            print(f"   ¿Quisiste decir?: {sugg}")
        return {"error": f"Lengua '{lang_code}' sin checkpoint MMS ni perfil.",
                "suggestions": sugg or []}
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    base_name = output_name or f"audio_{lang_code}_{int(time.time())}"
    
    result = {"lang": lang_code, "lang_name": lang_info["name"], "files": {}}
    step_cb = on_step or (lambda *_: None)
    
    print(f"\n{'='*60}")
    print(f"🌿 CONVERSOR LENGUAS INDÍGENAS DE MÉXICO")
    print(f"   Lengua: {lang_info['name']} ({lang_code})")
    print(f"   Fuente: {input_source[:60]}...")
    print(f"{'='*60}")
    
    # ── PASO 1: Obtener texto en español ──
    spanish_text = None
    
    if input_source.startswith(("http://", "https://", "www.")):
        step_cb("download")
        print("\n📥 PASO 1: Descargando video...")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path  = Path(tmp)
            mp3_file  = download_youtube(input_source, tmp_path)
            if not mp3_file:
                print("❌ No se pudo descargar el video")
                return result
            
            # Save audio (conservar extensión real: m4a/webm/mp3…)
            mp3_dest = OUTPUT_DIR / f"{base_name}{mp3_file.suffix}"
            mp3_dest.write_bytes(mp3_file.read_bytes())
            result["files"]["audio_fuente"] = str(mp3_dest)
            
            step_cb("transcribe")
            print("\n📝 PASO 2: Transcribiendo audio...")
            spanish_text = transcribe(mp3_dest, stt)
    else:
        print("\n📝 PASO 1: Texto recibido directamente")
        spanish_text = input_source
    
    if not spanish_text:
        print("❌ Sin texto para procesar")
        result["error"] = "No se pudo obtener texto de la fuente"
        return result
    result["source_text"] = spanish_text
    
    # Save transcription/text
    txt_path = OUTPUT_DIR / f"{base_name}_es.txt"
    txt_path.write_text(spanish_text, encoding="utf-8")
    result["files"]["texto_es"] = str(txt_path)
    print(f"\n📄 Texto: {spanish_text[:100]}...")
    
    # ── PASO 2/3: Traducir ──
    step = 3 if "audio_fuente" in result["files"] else 2
    print(f"\n🔄 PASO {step}: Traduciendo a {lang_info['name']}...")
    
    step_cb("translate")
    if lang_code == "spa":
        translation, engine = spanish_text, "none"
    else:
        translation, engine = translate_ex(spanish_text, lang_code, translator)
    
    if not translation:
        print("❌ Sin traducción")
        result["error"] = "Ningún motor produjo una traducción utilizable para esta lengua"
        return result
    result["translation"], result["engine"] = translation, engine
    
    trad_path = OUTPUT_DIR / f"{base_name}_{lang_code}.txt"
    trad_path.write_text(translation, encoding="utf-8")
    result["files"]["texto_indigena"] = str(trad_path)
    
    # ── PASO 3/4: TTS ──
    step += 1
    print(f"\n🔊 PASO {step}: Generando audio en {lang_info['name']}...")
    
    audio_out = OUTPUT_DIR / f"{base_name}_{lang_code}.wav"
    
    if not lang_info.get("mms") and lang_code != "spa":
        # Sin checkpoint MMS: leerlo con una voz en español sería audio falso.
        print("  ℹ️  Esta lengua no tiene voz MMS publicada — se entrega solo texto.")
        result["text_only"] = True
        step_cb("done")
        return result
    
    step_cb("tts")
    tts_info = synthesize(translation, lang_code, audio_out)
    success = tts_info is not None
    if success:
        result["tts"] = tts_info
    elif not fallback_say:
        result["error"] = "La síntesis de voz falló"
    if not success and fallback_say:
        print(f"  ⚠️  MMS-TTS no disponible — instalando dependencias...")
        print(f"      Ejecuta: pip install transformers scipy torch")
        print(f"  🔄 Usando fallback macOS say (en español)...")
        audio_out = OUTPUT_DIR / f"{base_name}_es_fallback.mp3"
        fb = tts_mac_say(translation, audio_out)
        if fb:
            success, audio_out = True, fb
        else:
            success = False
    
    if success:
        result["files"]["audio"] = str(audio_out)
    step_cb("done")
    
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
  python conversor.py --list-langs        # curadas MX
  python conversor.py --list-mms          # ~1,100 checkpoints MMS del mundo

  # Cualquier lengua del mundo con checkpoint MMS (ISO 639-3)
  python conversor.py "Hola mundo" --lang que   # quechua
  python conversor.py "Hola mundo" --lang haw   # hawaiano

  # Agrega tus propios perfiles en languages_extra.json
  # (ver languages_extra.json.example y docs/CUALQUIER_IDIOMA.md)
        """
    )
    parser.add_argument("input", nargs="?", help="URL de YouTube o texto en español")
    parser.add_argument("--lang", "-l", default="nah",
                        help="Código curado, ISO 639-3 MMS, o pack de languages_extra.json "
                             "(default: nah=Náhuatl)")
    parser.add_argument("--output", "-o", default=None,
                        help="Nombre base para archivos de salida")
    parser.add_argument("--list-langs", action="store_true",
                        help="Listar lenguas curadas (México)")
    parser.add_argument("--list-mms", action="store_true",
                        help="Listar todos los códigos ISO 639-3 con checkpoint MMS")
    parser.add_argument("--outdir", default="output_audio",
                        help="Directorio de salida (default: output_audio)")
    parser.add_argument("--translator", "-t", default="auto",
                        choices=["auto", "google", "groq", "gemini", "ollama-cloud", "cerebras", "llama"],
                        help="Traductor: auto (Google NMT si hay par, luego LLMs), google, groq, gemini, "
                             "ollama-cloud, cerebras, o llama (Ollama local)")
    parser.add_argument("--stt", default="auto", choices=["auto", "groq", "local"],
                        help="Transcripción: auto (Groq si hay key), groq (Whisper API), local (whisper CLI)")
    
    args = parser.parse_args()
    
    global OUTPUT_DIR
    OUTPUT_DIR = Path(args.outdir)
    
    if args.list_langs:
        print("\n🌿 LENGUAS CURADAS (MÉXICO)\n")
        print(f"{'Código':<8} {'Nombre':<28} {'Modelo TTS'}")
        print("-"*60)
        for code, info in LANGUAGES.items():
            mms = info["mms"] or "— (usa español)"
            print(f"  {code:<8} {info['name']:<28} {mms}")
        extra = _extra_languages()
        if extra:
            print(f"\n📦 PACKS EXTRA (languages_extra.json): {list(extra.keys())}")
        print(f"\n🌍 + {len(_mms_catalog())} códigos ISO 639-3 del mundo (--list-mms)")
        print()
        return

    if args.list_mms:
        catalog = _mms_catalog()
        print(f"\n🌍 CHECKPOINTS MMS DISPONIBLES ({len(catalog)} códigos)\n")
        codes = sorted(catalog)
        for i in range(0, len(codes), 8):
            print("  " + "  ".join(f"{c:<24}" for c in codes[i:i+8]))
        print(f"\nUsa cualquiera directo: --lang <codigo>  (ej: --lang que)")
        print()
        return
    
    if not args.input:
        parser.print_help()
        return
    
    result = convert(args.input, args.lang, args.output, args.translator, args.stt)
    sys.exit(0 if result.get("files") else 1)


if __name__ == "__main__":
    main()
