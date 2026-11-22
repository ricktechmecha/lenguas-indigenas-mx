#!/usr/bin/env python3
"""
gtranslate.py — backend de traducción vía Google Translate (NMT dedicado).

Por qué existe: los LLM generalistas fallan en lenguas de bajos recursos
(gpt-oss-120b ≈ 0.01 en back-translation a zapoteco). Google Translate tiene
modelos NMT entrenados para ~249 lenguas, incluidas náhuatl de la Huasteca
(nhe), maya yucateco (yua), zapoteco (zap), mam, q'eqchi' (kek), quechua,
aymara y guaraní.

Dos modos:
  - GOOGLE_TRANSLATE_API_KEY definida → API oficial Cloud Translation v2.
  - sin key → endpoint web público sin autenticación (client=gtx). NO es una
    API con SLA ni términos para uso en producción: sirve para prototipo y
    evaluación; para publicar/operar usar la API oficial.

El mapa GT_BY_MMS va de slug MMS (ISO 639-3 [+ -script_x]) → código Google.
Solo se listan pares donde la VARIANTE coincide razonablemente; p.ej. Google
'nhe' es náhuatl de la Huasteca oriental, por eso NO se usa para 'azz'.
"""
import json, os, time, urllib.parse, urllib.request
from typing import Optional

# Códigos de 3 letras idénticos en Google y en el catálogo MMS (verif. 2026-11).
_SAME = ("ace ach alz awa ban bbc bem bts btx dyu fon hil iba ilo jam kac kek kri "
         "mai mak mam mfe min new nhe nus pag pam pap sah shn sus tpi udm war yua").split()

GT_BY_MMS = {c: c for c in _SAME}
GT_BY_MMS.update({
    # América
    "zai": "zap",   # Google 'zap' sin variante declarada; su salida usa léxico del Istmo (lidxi, jñaa)
    "quz": "qu", "ayr": "ay", "grn": "gn", "hat": "ht",
    # África
    "amh": "am", "bam": "bm", "ewe": "ee", "hau": "ha", "kin": "rw", "nya": "ny",
    "orm": "om", "sna": "sn", "som": "so", "swh": "sw", "tir": "ti", "yor": "yo", "aka": "ak",
    # Asia / Pacífico
    "asm": "as", "ben": "bn", "bod": "bo", "guj": "gu", "hin": "hi", "ind": "id",
    "jav": "jw", "kan": "kn", "kaz": "kk", "khm": "km", "kir": "ky", "kor": "ko",
    "lao": "lo", "mal": "ml", "mar": "mr", "mya": "my", "ory": "or", "pan": "pa",
    "sun": "su", "tam": "ta", "tat": "tt", "tel": "te", "tgk": "tg", "tgl": "tl",
    "tha": "th", "vie": "vi", "zlm": "ms", "bak": "ba", "smo": "sm", "fij": "fj",
    "urd-script_arabic": "ur", "uig-script_arabic": "ug", "azj-script_latin": "az",
    # Medio Oriente / Europa
    "ara": "ar", "fas": "fa", "heb": "iw", "tur": "tr", "rus": "ru", "ukr": "uk",
    "bul": "bg", "cat": "ca", "cym": "cy", "deu": "de", "ell": "el", "eng": "en",
    "fin": "fi", "fra": "fr", "hun": "hu", "isl": "is", "lav": "lv", "nld": "nl",
    "pol": "pl", "por": "pt", "ron": "ro", "swe": "sv", "spa": "es",
})

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/131.0 Safari/537.36"

def gt_code(mms_id: Optional[str]) -> Optional[str]:
    """Código Google para un checkpoint 'facebook/mms-tts-xxx' (o None)."""
    if not mms_id:
        return None
    slug = mms_id.replace("facebook/mms-tts-", "")
    return GT_BY_MMS.get(slug) or GT_BY_MMS.get(slug.split("-")[0])

def google_translate(text: str, target: str, source: str = "es", timeout: int = 30,
                     retries: int = 2) -> Optional[str]:
    """Traduce text source→target. Devuelve None si falla (el caller hace fallback)."""
    for attempt in range(retries + 1):
        out = _google_translate_once(text, target, source, timeout, quiet=attempt < retries)
        if out:
            return out
        time.sleep(1 + attempt)
    return None

def _google_translate_once(text, target, source, timeout, quiet=False) -> Optional[str]:
    key = os.getenv("GOOGLE_TRANSLATE_API_KEY", "").strip()
    try:
        if key:
            body = urllib.parse.urlencode({"q": text, "source": source, "target": target,
                                           "format": "text", "key": key}).encode()
            req = urllib.request.Request(
                "https://translation.googleapis.com/language/translate/v2", data=body,
                headers={"User-Agent": UA}, method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read())
            return data["data"]["translations"][0]["translatedText"].strip() or None
        out = []
        for chunk in _chunks(text):
            body = urllib.parse.urlencode({"client": "gtx", "sl": source, "tl": target,
                                           "dt": "t", "q": chunk}).encode()
            req = urllib.request.Request(
                "https://translate.googleapis.com/translate_a/single", data=body,
                headers={"User-Agent": UA}, method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read())
            out.append("".join(seg[0] for seg in data[0] if seg and seg[0]))
        return " ".join(out).strip() or None
    except Exception as e:
        if not quiet:
            print(f"  ⚠️  Google Translate ({target}): {e}")
        return None

def _chunks(text: str, limit: int = 1800):
    """Parte por oraciones para no exceder el límite del endpoint."""
    import re
    buf = ""
    for sent in re.split(r"(?<=[.!?…])\s+", text.strip()):
        if buf and len(buf) + len(sent) + 1 > limit:
            yield buf
            buf = ""
        while len(sent) > limit:
            yield sent[:limit]
            sent = sent[limit:]
        buf = f"{buf} {sent}".strip()
    if buf:
        yield buf

if __name__ == "__main__":
    import sys
    tl = sys.argv[1] if len(sys.argv) > 1 else "yua"
    print(google_translate(" ".join(sys.argv[2:]) or "Buenos días, bienvenidos a la comunidad.", tl))
