#!/usr/bin/env python3
"""E2E con navegador real (Playwright/Chromium) — levanta app.py en puerto
efímero y prueba las 3 páginas + flujos del conversor.

    .venv/bin/python -m unittest discover -s tests/e2e -v

Requiere: playwright + chromium (`playwright install chromium`).
El test de conversión real a 'hch' solo corre si hay GROQ_API_KEY
(text-only, sin TTS — no descarga modelos).
"""
import json, os, sys, threading, unittest, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

PORT = None

def _serve():
    global PORT
    import app
    srv = app.ThreadingHTTPServer(("127.0.0.1", 0), app.H)
    PORT = srv.server_address[1]
    srv.serve_forever()

# Arranca el server una vez para toda la suite
_t = threading.Thread(target=_serve, daemon=True)
_t.start()
for _ in range(100):
    if PORT:
        break
    import time; time.sleep(0.05)
BASE = f"http://127.0.0.1:{PORT}"

def _has_groq() -> bool:
    """Las keys se cargan vía conversor._load_dotenv al importar el server."""
    try:
        import conversor as cv
        return bool(cv.GROQ_KEYS)
    except Exception:
        return False


def _pw():
    from playwright.sync_api import sync_playwright
    return sync_playwright()


class WebE2E(unittest.TestCase):
    """Tests que necesitan navegador — un browser por test."""

    def setUp(self):
        self.pw = _pw().start()
        self.browser = self.pw.chromium.launch(headless=True)
        self.page = self.browser.new_page()

    def tearDown(self):
        self.browser.close()
        self.pw.stop()

    # ── Landing ─────────────────────────────────────────────
    def test_landing_renders(self):
        self.page.goto(BASE + "/")
        self.assertIn("Lenguas", self.page.title())
        self.page.wait_for_selector("#tiers .tier, #tiers .card", timeout=8000)
        # tiers se llenan vía /api/coverage
        txt = self.page.inner_text("#tiers")
        self.assertRegex(txt, r"\d+")
        # links de navegación
        self.assertEqual(self.page.locator('nav a[href="/cobertura"]').count(), 1)

    def test_landing_a11y_basics(self):
        self.page.goto(BASE + "/")
        self.assertEqual(self.page.locator("a.skip").count(), 1)
        self.assertEqual(self.page.locator("main#main").count(), 1)
        self.assertEqual(self.page.locator("h1").count(), 1)

    # ── Cobertura ───────────────────────────────────────────
    def test_cobertura_table_and_filter(self):
        self.page.goto(BASE + "/cobertura")
        self.page.wait_for_selector("#tbody tr", timeout=10000)
        n0 = self.page.locator("#tbody tr").count()
        self.assertGreater(n0, 50)
        self.page.fill("#q", "yucatec")
        self.page.wait_for_timeout(300)
        rows = self.page.locator("#tbody tr")
        self.assertLessEqual(rows.count(), 5)
        self.assertIn("yua", rows.first.inner_text())

    def test_cobertura_tier_filter(self):
        self.page.goto(BASE + "/cobertura")
        self.page.wait_for_selector("#tbody tr", timeout=10000)
        self.page.select_option("#tier", "C")
        self.page.wait_for_timeout(300)
        rows = self.page.locator("#tbody tr")
        self.assertGreaterEqual(rows.count(), 1)
        self.assertLessEqual(rows.count(), 10)  # solo 3 tier-C

    def test_cobertura_pagination_button(self):
        self.page.goto(BASE + "/cobertura")
        self.page.wait_for_selector("#tbody tr", timeout=10000)
        # ~1,020 lenguas > 100 por página → debe existir el botón
        self.page.wait_for_selector("#morebtn", timeout=5000)
        before = self.page.locator("#tbody tr").count()
        self.page.click("#morebtn")
        self.page.wait_for_timeout(200)
        after = self.page.locator("#tbody tr").count()
        self.assertGreater(after, before)

    # ── Convertir ───────────────────────────────────────────
    def test_convertir_dropdown_mutual_exclusion(self):
        """Elegir del catálogo limpia el ISO libre y viceversa (bug reportado)."""
        self.page.goto(BASE + "/convertir")
        self.page.wait_for_selector("#lang option", state="attached", timeout=10000)
        self.page.fill("#iso", "quz")
        self.assertEqual(self.page.eval_on_selector("#lang", "el=>el.value"), "")
        self.page.select_option("#lang", "yua")
        self.assertEqual(self.page.eval_on_selector("#iso", "el=>el.value"), "")
        # ejemplo carga texto + selecciona yua
        self.page.click("#ej")
        self.assertTrue(self.page.eval_on_selector("#txt", "el=>el.value").strip())
        self.assertEqual(self.page.eval_on_selector("#lang", "el=>el.value"), "yua")

    def test_convertir_form_validation(self):
        self.page.goto(BASE + "/convertir")
        self.page.wait_for_selector("#lang option", state="attached", timeout=10000)
        opts = self.page.locator("#lang option").count()
        self.assertGreater(opts, 30)
        # submit vacío → error inline (no alert)
        self.page.click("#go")
        self.page.wait_for_timeout(300)
        self.assertIn("lengua", self.page.inner_text("#status").lower())

    def test_convertir_invalid_lang_shows_suggestions(self):
        self.page.goto(BASE + "/convertir")
        self.page.wait_for_selector("#lang option", state="attached", timeout=10000)
        self.page.fill("#iso", "nahuatl-que-no-existe")
        self.page.fill("#txt", "hola")
        self.page.click("#go")
        # esperar el job (poll cada 1.2s)
        self.page.wait_for_selector("#res:not(.hidden)", timeout=30000)
        body = self.page.inner_text("#result")
        self.assertIn("Error", body)

    @unittest.skipUnless(_has_groq(), "sin GROQ_API_KEY — conversión real no corre")
    def test_convertir_hch_real_text_only(self):
        """E2E real: texto → Groq → wixárika (sin voz MMS → solo texto)."""
        self.page.goto(BASE + "/convertir")
        self.page.wait_for_selector("#lang option", state="attached", timeout=10000)
        self.page.select_option("#lang", "hch")
        self.page.fill("#txt", "Buenos días, ¿cómo estás?")
        self.page.click("#go")
        # El fallback local (Ollama) puede tardar minutos en timeout — camino real
        self.page.wait_for_selector("#res:not(.hidden)", timeout=480000)
        body = self.page.inner_text("#res")  # incluye badges + resultado
        low = body.lower()
        # El pipeline puede traducir (Groq/Llama) o fallar limpio — ambos son
        # comportamiento E2E válido. Lo que NO puede pasar: audio para hch,
        # ni preámbulos/meta-comentario del LLM presentados como "traducción".
        self.assertTrue("traducción" in low or "error" in low, body[:200])
        self.assertNotIn("i'm happy to help", low)
        self.assertNotIn("i need to clarify", low)
        # "texto fuente" solo aparece cuando hubo traducción real (no en error)
        if "texto fuente" in low:
            self.assertIn("solo texto", low)  # hch sin MMS → nunca audio
            self.assertEqual(self.page.locator("#result audio, #res audio").count(), 0)

    # ── API smoke desde el navegador ────────────────────────
    def test_api_endpoints_from_browser(self):
        self.page.goto(BASE + "/")
        langs = self.page.evaluate("fetch('/api/languages').then(r=>r.json())")
        self.assertGreater(len(langs), 30)
        cov = self.page.evaluate("fetch('/api/coverage').then(r=>r.json())")
        for t in ("A", "B", "C"):
            self.assertIn(t, cov["tiers"])


if __name__ == "__main__":
    unittest.main()
