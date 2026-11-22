#!/usr/bin/env python3
"""
app.py — Frontend web del conversor de lenguas (stdlib puro, sin build steps).

    python3 app.py            → http://127.0.0.1:8000

Solo escucha en localhost. Un trabajo a la vez (el TTS es pesado en CPU).
"""
import json, re, sys, threading, time, traceback
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import conversor as cv

HOST, PORT = "127.0.0.1", 8000
OUTPUT_DIR = Path("output_audio").resolve()

JOBS: dict = {}          # id -> {status, steps, result, error}
JOBS_LOCK = threading.Lock()
BUSY = threading.Lock()  # TTS es CPU-pesado: una conversión a la vez

# ─── catálogo para la UI ────────────────────────────────────────────────────
def language_catalog() -> list:
    """Curadas primero + stubs sin voz; el campo libre acepta cualquier ISO."""
    from gtranslate import gt_code
    rows = []
    for code, info in cv.LANGUAGES.items():
        has_voice = bool(info.get("mms")) or code == "spa"
        rows.append({
            "code": code, "name": info["name"],
            "voice": has_voice,
            "engine": "google" if code != "spa" and (info.get("gt") or gt_code(info.get("mms"))) else "llm",
            "iso": code if len(code) == 3 else None,
        })
    return rows

def run_job(job_id: str, inp: str, lang: str, translator: str):
    def step(s):
        with JOBS_LOCK:
            JOBS[job_id]["steps"].append(s)
            JOBS[job_id]["step"] = s
    try:
        res = cv.convert(inp, lang, translator=translator,
                         on_step=step, fallback_say=False)
        with JOBS_LOCK:
            j = JOBS[job_id]
            j["status"] = "done" if res.get("files") else "error"
            j["result"] = {
                "lang_name": res.get("lang_name"),
                "engine": res.get("engine"),
                "translation": res.get("translation"),
                "source_text": res.get("source_text"),
                "tts": res.get("tts"),
                "text_only": bool(res.get("text_only")),
                "error": res.get("error"),
                "files": {k: Path(v).name for k, v in res.get("files", {}).items()},
            }
            if not j["result"]["files"] and not j["result"]["error"]:
                j["result"]["error"] = "Sin resultado"
    except Exception:
        with JOBS_LOCK:
            JOBS[job_id]["status"] = "error"
            JOBS[job_id]["error"] = traceback.format_exc(limit=3)
    finally:
        BUSY.release()

# ─── HTTP ───────────────────────────────────────────────────────────────────
PAGE = r"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lenguas Indígenas — texto/video → audio</title>
<style>
:root{--bg:#0f1419;--card:#1a2230;--acc:#4cc9f0;--ok:#7bf1a8;--warn:#ffd166;--bad:#ef476f;--txt:#e8eef5}
*{box-sizing:border-box}body{margin:0;font:15px/1.5 -apple-system,system-ui,sans-serif;background:var(--bg);color:var(--txt)}
main{max-width:760px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:1.4rem;margin:0 0 4px}.sub{color:#9fb0c3;margin-bottom:20px}
.card{background:var(--card);border-radius:14px;padding:18px;margin-bottom:16px}
label{display:block;font-size:.8rem;color:#9fb0c3;margin:10px 0 4px;text-transform:uppercase;letter-spacing:.04em}
input[type=text],textarea,select{width:100%;background:#0d1420;color:var(--txt);border:1px solid #2a3a52;border-radius:8px;padding:10px;font:inherit}
textarea{min-height:90px;resize:vertical}
.row{display:flex;gap:10px;flex-wrap:wrap}.row>*{flex:1;min-width:180px}
button{background:var(--acc);color:#04121a;border:0;border-radius:8px;padding:12px 22px;font:inherit;font-weight:600;cursor:pointer;margin-top:14px}
button:disabled{opacity:.5;cursor:wait}
.note{background:#241d10;border:1px solid #6b5518;color:var(--warn);border-radius:10px;padding:10px 14px;font-size:.9rem;margin-top:14px}
.steps{display:flex;gap:6px;margin:12px 0;flex-wrap:wrap}
.steps span{font-size:.75rem;padding:4px 10px;border-radius:99px;background:#0d1420;color:#6b7c90}
.steps span.on{background:var(--acc);color:#04121a}.steps span.done{background:#14532d;color:var(--ok)}
.badges{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}
.badge{font-size:.75rem;padding:3px 10px;border-radius:99px}
.b-ok{background:#14532d;color:var(--ok)}.b-info{background:#123a52;color:var(--acc)}.b-warn{background:#4a3510;color:var(--warn)}.b-no{background:#3a1420;color:var(--bad)}
tr_out{display:block;background:#0d1420;border-radius:8px;padding:12px;white-space:pre-wrap;margin-top:6px}
.mono{font-family:ui-monospace,Menlo,monospace;font-size:.85rem}
audio{width:100%;margin-top:10px}a{color:var(--acc)}
.err{color:var(--bad)}.hidden{display:none}
</style></head><body><main>
<h1>🌿 Lenguas Indígenas — texto/video → audio</h1>
<div class="sub">Conversor open-source · Meta MMS-TTS + traducción multi-motor</div>

<div class="note"><b>Aviso honesto:</b> la traducción automática a lenguas de bajos recursos puede tener errores — verifícala con un hablante nativo. La voz es <b>síntesis</b> (MMS-TTS), no una persona real. Los textos sin voz publicada se entregan solo como texto.</div>

<div class="card">
<label>Lengua destino</label>
<div class="row">
  <select id="lang"></select>
  <input type="text" id="iso" placeholder="o ISO 639-3 libre (ej. quz, haw, hawaiiano…)">
</div>
<label>Texto en español</label>
<textarea id="txt" placeholder="Escribe aquí…"></textarea>
<label>— o URL de YouTube —</label>
<input type="text" id="url" placeholder="https://youtube.com/watch?v=…">
<div class="row">
  <div><label>Motor</label>
    <select id="engine"><option value="auto">Auto (mejor disponible)</option><option value="google">Google Translate</option><option value="groq">Groq (LLM)</option><option value="llama">Ollama local</option></select></div>
</div>
<button id="go">Generar</button>
</div>

<div id="prog" class="card hidden"><b>Progreso</b><div class="steps" id="steps"></div>
<div id="status" class="mono"></div></div>

<div id="res" class="card hidden"><b>Resultado</b><div class="badges" id="badges"></div>
<div id="result"></div></div>
</main><script>
const $=s=>document.querySelector(s);
const STEP_TXT={download:'Descargando video',transcribe:'Transcribiendo',translate:'Traduciendo',tts:'Sintetizando voz',done:'Listo'};
let langs={};
fetch('/api/languages').then(r=>r.json()).then(d=>{
  langs=d;
  const sel=$('#lang');
  d.forEach(l=>{const o=document.createElement('option');o.value=l.code;
    o.textContent=l.name+(l.voice?'':'  (solo texto)')+(l.engine==='google'?'  ★Google':'');
    sel.appendChild(o);});
});
$('#go').onclick=async()=>{
  const lang=$('#iso').value.trim()||$('#lang').value;
  const inp=$('#txt').value.trim()||$('#url').value.trim();
  if(!lang||!inp){alert('Elige lengua y pega texto o URL');return;}
  $('#go').disabled=true;$('#res').classList.add('hidden');$('#prog').classList.remove('hidden');
  $('#steps').innerHTML='';$('#status').textContent='Iniciando…';
  const eng=$('#engine').value;
  const r=await fetch('/api/convert',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({input:inp,lang,translator:eng})});
  const {job}=await r.json();
  const t=setInterval(async()=>{
    const j=await (await fetch('/api/jobs/'+job)).json();
    const st=$('#steps');const done=new Set(j.steps||[]);
    st.innerHTML=['download','transcribe','translate','tts','done'].map(k=>
      `<span class="${k==='done'&&j.status==='done'?'done':done.has(k)?'done':k===j.step?'on':''}">${STEP_TXT[k]}</span>`).join('');
    $('#status').textContent=j.status==='running'?'Procesando…':j.status;
    if(j.status==='done'||j.status==='error'){clearInterval(t);finish(j);}
  },1200);
};
function finish(j){
  $('#go').disabled=false;
  const r=j.result||{};const box=$('#res');box.classList.remove('hidden');
  const b=$('#badges');b.innerHTML='';
  const badge=(t,c)=>b.insertAdjacentHTML('beforeend',`<span class="badge ${c}">${t}</span>`);
  if(r.engine&&r.engine!=='none')badge('motor: '+r.engine,'b-info');
  if(r.tts){if(r.tts.coverage<1)badge(`alfabeto ${(r.tts.coverage*100).toFixed(0)}%`,'b-warn');else badge('alfabeto 100%','b-ok');badge(r.tts.seconds+'s audio','b-ok');}
  if(r.text_only)badge('SOLO TEXTO (sin voz MMS)','b-no');
  let h='';
  if(j.status==='error'){h+=`<div class="err">Error: ${j.error||r.error||'desconocido'}</div>`;}
  if(r.translation)h+=`<label>Traducción</label><div class="mono">${esc(r.translation)}</div>`;
  if(r.source_text&&r.translation)h+=`<label>Texto fuente</label><div class="mono">${esc(r.source_text).slice(0,600)}</div>`;
  const f=r.files||{};
  if(f.audio){h+=`<label>Audio</label><audio controls src="/audio/${f.audio}"></audio>
    <div><a href="/audio/${f.audio}" download>⬇ Descargar .wav</a></div>`;}
  $('#result').innerHTML=h;
}
function esc(s){return String(s??'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
</script></body></html>"""

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, body, ctype="application/json", extra=None):
        data = body if isinstance(body, bytes) else body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items(): self.send_header(k, v)
        self.end_headers(); self.wfile.write(data)
    def _json(self, code, obj): self._send(code, json.dumps(obj, ensure_ascii=False))

    def do_GET(self):
        u = urlparse(self.path); p = u.path
        if p == "/":
            self._send(200, PAGE, "text/html; charset=utf-8"); return
        if p == "/api/languages":
            self._json(200, language_catalog()); return
        m = re.fullmatch(r"/api/jobs/([0-9a-f]{12})", p)
        if m:
            with JOBS_LOCK:
                j = JOBS.get(m.group(1))
                pub = None if j is None else {k: j[k] for k in ("status", "steps", "step", "result", "error") if k in j}
            self._json(200 if pub else 404, pub or {"error": "job not found"}); return
        m = re.fullmatch(r"/audio/([\w.\-]+\.wav)", p)
        if m:
            f = (OUTPUT_DIR / m.group(1)).resolve()
            if f.parent == OUTPUT_DIR and f.exists():
                self._send(200, f.read_bytes(), "audio/wav"); return
            self._json(404, {"error": "not found"}); return
        self._json(404, {"error": "not found"})

    def do_POST(self):
        if urlparse(self.path).path != "/api/convert":
            self._json(404, {"error": "not found"}); return
        try:
            n = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            self._json(400, {"error": "JSON inválido"}); return
        inp, lang = (body.get("input") or "").strip(), (body.get("lang") or "").strip().lower()
        if not inp or not lang:
            self._json(400, {"error": "faltan input/lang"}); return
        if not BUSY.acquire(blocking=False):
            self._json(429, {"error": "Ya hay una conversión en curso — espera a que termine"}); return
        jid = f"{int(time.time()*1000)%10**12:012x}"
        with JOBS_LOCK:
            JOBS[jid] = {"status": "running", "steps": [], "step": None,
                         "result": None, "error": None}
        threading.Thread(target=run_job, args=(jid, inp, lang,
                                               body.get("translator", "auto")), daemon=True).start()
        self._json(202, {"job": jid})

if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    srv = ThreadingHTTPServer((HOST, PORT), H)
    print(f"🌿 http://{HOST}:{PORT}  (Ctrl+C para salir)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
