#!/usr/bin/env python3
"""Tests del núcleo de lenguas-indigenas — stdlib unittest, sin red ni GPU.

Cubre las funciones puras del pipeline: resolución de lenguas, aliases,
mapeo MMS→Google, guards anti-basura del LLM, normalización TTS y chunks.

    python3 -m unittest discover -s tests -v
"""
import sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import conversor as cv
import gtranslate as gt


class TestResolveLanguage(unittest.TestCase):
    def test_curated_nah(self):
        info = cv.resolve_language("nah")
        self.assertEqual(info["mms"], "facebook/mms-tts-azz")

    def test_alias_macrolanguage(self):
        # 'que' (Quechua macrolengua) → variante quz del catálogo MMS
        info = cv.resolve_language("que")
        self.assertIsNotNone(info)
        self.assertIn("quz", info["mms"])

    def test_iso_from_catalog(self):
        info = cv.resolve_language("quz")
        self.assertIsNotNone(info)
        self.assertTrue(info["mms"].startswith("facebook/mms-tts-"))

    def test_unknown_returns_none(self):
        self.assertIsNone(cv.resolve_language("nahuatl"))
        self.assertIsNone(cv.resolve_language("zzz"))

    def test_text_only_language(self):
        # hch wixárika: perfil existe pero SIN checkpoint de voz
        info = cv.resolve_language("hch")
        self.assertIsNotNone(info)
        self.assertIsNone(info["mms"])

    def test_spa_has_mms_checkpoint(self):
        # Regresión: 'spa' era demo sin voz aunque el catálogo sí tiene checkpoint
        self.assertEqual(cv.LANGUAGES["spa"]["mms"], "facebook/mms-tts-spa")

    def test_suggestions_for_typo(self):
        sugg = cv.suggest_languages("nahuatl")
        self.assertTrue(sugg)
        self.assertTrue(any("nah" in s for s in sugg))


class TestGoogleMapping(unittest.TestCase):
    def test_identical_codes(self):
        self.assertEqual(gt.gt_code("facebook/mms-tts-yua"), "yua")

    def test_renamed_codes(self):
        self.assertEqual(gt.gt_code("facebook/mms-tts-zai"), "zap")
        self.assertEqual(gt.gt_code("facebook/mms-tts-quz"), "qu")

    def test_dialect_slug_falls_back_to_base(self):
        self.assertEqual(gt.gt_code("facebook/mms-tts-mam-dialect_central"), "mam")

    def test_unmapped_returns_none(self):
        # azz (náhuatl Zacapoaxtla) NO tiene par Google — nhe es otra variante
        self.assertIsNone(gt.gt_code("facebook/mms-tts-azz"))
        self.assertIsNone(gt.gt_code(None))
        self.assertIsNone(gt.gt_code(""))

    def test_google_supported_flags(self):
        self.assertTrue(cv.google_supported("yua"))
        self.assertTrue(cv.google_supported("nah-hua"))   # mms nhe → Google nhe
        self.assertFalse(cv.google_supported("nah"))       # azz sin par
        self.assertFalse(cv.google_supported("hch"))


class TestOutputGuards(unittest.TestCase):
    def test_refusal_detected(self):
        self.assertTrue(cv._looks_refusal("I'm sorry, I can't provide that translation."))
        self.assertTrue(cv._looks_refusal("Lo siento, no puedo proporcionar eso."))

    def test_real_translation_not_refusal(self):
        self.assertFalse(cv._looks_refusal("Kawá, kawá wá?"))
        self.assertFalse(cv._looks_refusal("Le chan xi'ipalo' ku janal waaj."))

    def test_llm_preamble_detected(self):
        # Caso real capturado por E2E: Llama respondió con preámbulo, no traducción
        preamble = ("I'm happy to help with the translation. However, I need to "
                    "clarify that I'll be using the Wixárika language")
        self.assertTrue(cv._looks_refusal(preamble))

    def test_degenerate_loop(self):
        loop = "kualtin " * 30
        self.assertTrue(cv._looks_degenerate("hola", loop))

    def test_degenerate_oversized(self):
        self.assertTrue(cv._looks_degenerate("hola", "x" * 3000))

    def test_normal_output_ok(self):
        self.assertFalse(cv._looks_degenerate(
            "El niño come pan.", "Le chan ku janal waaj tu yotoch."))


class TestTTSTextPrep(unittest.TestCase):
    def test_normalize_coverage(self):
        text, info = cv.normalize_for_tts("abc", {"a", "b"})
        self.assertEqual(info["coverage"], round(2 / 3, 3))
        self.assertIn("c", info["dropped"])

    def test_normalize_full_coverage(self):
        _, info = cv.normalize_for_tts("abc", {"a", "b", "c"})
        self.assertEqual(info["coverage"], 1.0)
        self.assertEqual(info["dropped"], [])

    def test_apostrophe_swap_to_known(self):
        # Si el vocab tiene ' pero no `, normaliza hacia el conocido
        text, _ = cv.normalize_for_tts("maʼaku", {"m", "a", "k", "u", "'"})
        self.assertIn("'", text)

    def test_chunks_respect_limit(self):
        long_text = ". ".join(["palabra"] * 200) + "."
        chunks = cv._tts_chunks(long_text, limit=100)
        self.assertGreater(len(chunks), 1)
        for c in chunks:
            self.assertLessEqual(len(c), 220)  # margen de seguridad

    def test_chunks_preserve_empty(self):
        self.assertEqual(cv._tts_chunks("   "), [])


class TestGtranslateChunks(unittest.TestCase):
    def test_chunks_split_long_text(self):
        text = "Primera oración. " * 200
        chunks = list(gt._chunks(text, limit=500))
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(c) <= 500 for c in chunks))

    def test_chunks_preserve_short(self):
        chunks = list(gt._chunks("Hola mundo."))
        self.assertEqual(chunks, ["Hola mundo."])


class TestTranslateExNoNetwork(unittest.TestCase):
    def test_google_unsupported_explicit_returns_none(self):
        # 'hch' no tiene par Google ni keys → (None, None) sin tocar red
        t, engine = cv.translate_ex("hola", "hch", "google")
        self.assertIsNone(t)
        self.assertIsNone(engine)

    def test_invalid_translator_rejected(self):
        with self.assertRaises(KeyError):
            cv.translate_ex("hola", "yua", "no-existe")


class TestCatalogAndCoverage(unittest.TestCase):
    def test_language_catalog_shape(self):
        import app
        cat = app.language_catalog()
        self.assertGreater(len(cat), 30)
        for row in cat:
            self.assertIn("code", row)
            self.assertIn("name", row)
            self.assertIn("voice", row)
            self.assertIn("engine", row)

    def test_catalog_spa_engine_none(self):
        import app
        cat = {r["code"]: r for r in app.language_catalog()}
        self.assertEqual(cat["spa"]["engine"], "none")
        self.assertTrue(cat["spa"]["voice"])

    def test_coverage_tiers_structure(self):
        cov = cv  # noqa
        import app
        data = app.coverage()
        for tier in ("A", "B", "C"):
            self.assertIn(tier, data.get("tiers", {}))
        self.assertGreater(len(data["tiers"]["A"]), 100)


class TestConvertInvalidLanguage(unittest.TestCase):
    def test_invalid_lang_returns_error_dict(self):
        res = cv.convert("hola", "lengua-que-no-existe-xyz")
        self.assertIn("error", res)
        self.assertIsInstance(res.get("suggestions"), list)


if __name__ == "__main__":
    unittest.main()
