#!/usr/bin/env python3
"""
app.py — Sitio del conversor de lenguas (stdlib puro, sin build steps).

    python3 app.py   →  http://127.0.0.1:8000

Rutas:
  /           landing explicativa + visión + qué falta
  /cobertura  tabla mundial interactiva de cobertura por lengua
  /convertir  la herramienta (texto/YouTube → audio)
  /api/*      JSON (languages, coverage, convert, jobs, audio)
"""
import json, re, sys, threading, time, traceback
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import conversor as cv

HOST, PORT = "127.0.0.1", 8000
OUTPUT_DIR = Path("output_audio").resolve()
COBERTURA = ROOT / "data" / "cobertura.json"

JOBS: dict = {}
JOBS_LOCK = threading.Lock()
BUSY = threading.Lock()  # TTS es CPU-pesado: una conversión a la vez

# ─── catálogo ───────────────────────────────────────────────────────────────
def language_catalog() -> list:
    from gtranslate import gt_code
    rows = []
    for code, info in cv.LANGUAGES.items():
        has_voice = bool(info.get("mms")) or code == "spa"
        rows.append({
            "code": code, "name": info["name"],
            "voice": has_voice,
            "engine": ("none" if code == "spa" else
                       "google" if code != "spa" and (info.get("gt") or gt_code(info.get("mms"))) else "llm"),
        })
    return rows

def coverage() -> dict:
    return json.loads(COBERTURA.read_text()) if COBERTURA.exists() else {"tiers": {}}

def run_job(job_id: str, inp: str, lang: str, translator: str):
    def step(s):
        with JOBS_LOCK:
            JOBS[job_id]["steps"].append(s)
            JOBS[job_id]["step"] = s
    try:
        res = cv.convert(inp, lang, translator=translator,
                         on_step=step, fallback_say=False)
        # Back-translation de verificación: si Google soporta la lengua,
        # re-traducir a español para que el usuario vea el significado.
        try:
            from gtranslate import google_translate, gt_code
            info = cv.resolve_language(lang) or {}
            mms = info.get("mms") or ""
            slug = mms.rsplit("-tts-", 1)[-1] if "-tts-" in mms else (mms or lang)
            gt = gt_code(slug)
            tr = res.get("translation")
            if gt and tr and len(tr) < 4000:
                bt = google_translate(tr, "es", source=gt)
                if bt:
                    res["back_translation"] = bt
        except Exception:
            pass
        with JOBS_LOCK:
            j = JOBS[job_id]
            j["status"] = "done" if res.get("files") else "error"
            j["result"] = {
                "lang_name": res.get("lang_name"),
                "engine": res.get("engine"),
                "translation": res.get("translation"),
                "back_translation": res.get("back_translation"),
                "source_text": res.get("source_text"),
                "tts": res.get("tts"),
                "text_only": bool(res.get("text_only")),
                "error": res.get("error"),
                "suggestions": res.get("suggestions"),
                "files": {k: Path(v).name for k, v in res.get("files", {}).items()},
            }
            if not j["result"]["files"] and not j["result"]["error"]:
                j["result"]["error"] = "Sin resultado"
    except Exception:
        with JOBS_LOCK:
            JOBS[job_id]["status"] = "error"
            JOBS[job_id]["error"] = traceback.format_exc(limit=3).strip().splitlines()[-1]
    finally:
        BUSY.release()

# ─── CSS compartido ─────────────────────────────────────────────────────────
CSS = """
:root{--bg:#0b0f14;--card:#151d29;--acc:#4cc9f0;--ok:#7bf1a8;--warn:#ffd166;--bad:#ef476f;--txt:#e8eef5;--mut:#9fb0c3}
html{color-scheme:dark}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}body{margin:0;font:16px/1.6 -apple-system,system-ui,sans-serif;background:var(--bg);color:var(--txt)}
a{color:var(--acc);text-decoration:none}
:focus-visible{outline:2px solid var(--acc);outline-offset:2px;border-radius:4px}
.skip{position:absolute;left:-9999px;top:0;background:var(--acc);color:#04121a;padding:10px 16px;z-index:9;border-radius:0 0 8px 0}
.skip:focus{left:0}
main{max-width:960px;margin:0 auto;padding:32px 18px 80px}
h1,h2{ text-wrap:balance}h1{font-size:2rem;line-height:1.2;margin:.2em 0}h2.h2{font-size:1.3rem;margin:1.6em 0 .4em}
.sub{color:var(--mut);font-size:1.05rem}
.card{background:var(--card);border-radius:14px;padding:20px;margin:16px 0}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.tier{border-radius:12px;padding:16px;border:1px solid #26334a}
.tier b{font-size:1.6rem;display:block}.t-ok{border-color:#1d5c38}.t-warn{border-color:#6b5518}.t-info{border-color:#123a52}
.tag{display:inline-block;font-size:.72rem;padding:2px 9px;border-radius:99px;margin:2px 4px 2px 0}
.tag.ok{background:#14532d;color:var(--ok)}.tag.warn{background:#4a3510;color:var(--warn)}
.tag.info{background:#123a52;color:var(--acc)}.tag.no{background:#3a1420;color:var(--bad)}
table{width:100%;border-collapse:collapse;font-size:.85rem;margin-top:8px}
th,td{padding:6px 8px;border-bottom:1px solid #223047;text-align:left;vertical-align:top}
th{color:var(--mut);font-size:.75rem;text-transform:uppercase;letter-spacing:.04em;position:sticky;top:0;background:var(--card)}
td code{color:var(--acc);font-size:.8rem}
input[type=text],textarea,select{width:100%;background:#0d1420;color:var(--txt);border:1px solid #2a3a52;border-radius:8px;padding:10px;font:inherit}
textarea{min-height:90px;resize:vertical}
label{display:block;font-size:.78rem;color:var(--mut);margin:12px 0 4px;text-transform:uppercase;letter-spacing:.04em}
button{background:var(--acc);color:#04121a;border:0;border-radius:8px;padding:12px 22px;font:inherit;font-weight:600;cursor:pointer;margin-top:14px;touch-action:manipulation;transition:background .15s,transform .05s}
button:hover{background:#6fd3f7}
button:active{transform:scale(.98)}
button:disabled{opacity:.5;cursor:wait}
.note{background:#241d10;border:1px solid #6b5518;color:var(--warn);border-radius:10px;padding:12px 16px;font-size:.92rem}
.steps{display:flex;gap:6px;margin:12px 0;flex-wrap:wrap}
.steps span{font-size:.75rem;padding:4px 10px;border-radius:99px;background:#0d1420;color:#93a7bf}
.steps span.on{background:var(--acc);color:#04121a}.steps span.done{background:#14532d;color:var(--ok)}
.badges{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}
.badge{font-size:.75rem;padding:3px 10px;border-radius:99px}
.b-ok{background:#14532d;color:var(--ok)}.b-info{background:#123a52;color:var(--acc)}.b-warn{background:#4a3510;color:var(--warn)}.b-no{background:#3a1420;color:var(--bad)}
.mono{font-family:ui-monospace,Menlo,monospace;font-size:.88rem;background:#0d1420;border-radius:8px;padding:12px;white-space:pre-wrap;margin-top:6px;overflow-wrap:anywhere;font-variant-numeric:tabular-nums}
audio{width:100%;margin-top:10px}
.err{color:var(--bad)}.hidden{display:none}
.nav{display:flex;gap:14px;font-size:.9rem;margin-bottom:8px}.nav a{padding:6px 12px;border-radius:8px;background:var(--card);touch-action:manipulation}
.nav a:hover{background:#1d2a3d}
.flow{display:flex;gap:8px;flex-wrap:wrap;align-items:center;font-size:.85rem;margin:10px 0}
.flow span{background:#0d1420;border:1px solid #2a3a52;padding:6px 12px;border-radius:8px}
.flow i{color:var(--acc);font-style:normal}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}
.filters input,.filters select{width:auto;flex:1;min-width:140px}
#tbody tr:hover{background:#182234}
.lbl{display:block;font-size:.78rem;color:var(--mut);margin:12px 0 4px;text-transform:uppercase;letter-spacing:.04em}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
footer{color:var(--mut);font-size:.8rem;text-align:center;margin-top:48px}
"""

def page(title, body):
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#0b0f14"><title>{title}</title>
<style>{CSS}</style></head><body><a class="skip" href="#main">Saltar al contenido</a><main id="main">{body}</main>
<footer>lenguas-indigenas · open source · honesto por diseño</footer></body></html>"""

NAV = '<nav class="nav" aria-label="Principal"><a href="/">← Qué es esto</a><a href="/cobertura">Cobertura mundial</a><a href="/convertir">▶ Probar el conversor</a></nav>'

PAGE_LANDING = page("Lenguas Indígenas — voz para lenguas que la tecnología olvidó", NAV + r"""
<h1>🌿 Lenguas que la tecnología olvidó</h1>
<div class="sub">Conversor open-source: texto o video de YouTube → <b>audio hablado</b> en la lengua que elijas.
Empezó con México; hoy cubre el mundo. Honestidad técnica: mostramos lo que funciona Y lo que no.</div>

<div class="card">
<h2 class="h2" style="margin-top:0">¿Qué hace?</h2>
<div class="flow"><span>Texto ES / YouTube</span><i>→</i><span>Transcripción (Whisper)</span><i>→</i><span>Traducción</span><i>→</i><span>Voz sintética (MMS-TTS)</span><i>→</i><span>.wav</span></div>
<p style="color:var(--mut);font-size:.92rem;margin-bottom:0">La traducción usa el mejor motor disponible por lengua:
NMT dedicado de Google cuando existe par verificado, LLM (Groq/local) como respaldo. La voz es
<b>MMS-TTS de Meta</b> — checkpoints abiertos para ~1,000 lenguas. <b>No inventamos modelos:</b>
orquestamos los mejores que existen y medimos dónde fallan.</p>
</div>

<h2 class="h2">📊 Cobertura real hoy (verificada, no promesa)</h2>
<div class="grid" id="tiers"><div class="card">Cargando…</div></div>
<div class="card" style="text-align:center"><a href="/cobertura">Ver la tabla mundial completa →</a>
&nbsp;·&nbsp;<a href="/convertir">Probar el conversor →</a></div>

<h2 class="h2">🎬 La visión: doblar series y películas</h2>
<div class="card">
<p>El pipeline completo para <b>doblaje de contenido</b> (audio de una serie/película → mismo audio en otra lengua):</p>
<div class="flow"><span>Audio ES/EN</span><i>→</i><span>Whisper (ya funciona)</span><i>→</i><span>Traducción</span><i>→</i><span>TTS por línea</span><i>→</i><span>ffmpeg: alinear + mezclar + mux</span><i>→</i><span>Audio doblado</span></div>
<p style="color:var(--mut);font-size:.92rem">Lo que YA tenemos: STT del idioma fuente, traducción y voz.
Lo que falta investigar: <b>alineación temporal</b> (que cada línea quepa en su escena — herramientas:
aeneas, stable-ts, o TTS por segmento con timestamps), mezcla/leveling con ffmpeg, y subtítulos
opcionales. Nada de esto requiere modelos nuevos — es ingeniería de pipeline.</p>
</div>

<h2 class="h2">🧩 Qué falta por tier — la lista de recursos</h2>
<div class="card">
<table>
<tr><th scope="col">Tier</th><th scope="col">Lenguas</th><th scope="col">Qué YA funciona</th><th scope="col">Qué FALTA (lo que pedimos)</th></tr>
<tr><td>🟢 A</td><td>116</td><td>Traducción NMT + voz + alfabeto verificado</td><td>Validación por hablante nativo, más dominios, variantes dialectales</td></tr>
<tr><td>🟡 B</td><td>901</td><td>Voz MMS lista</td><td><b>Traducción:</b> corpus paralelo ES↔lengua, diccionarios, fine-tune NLLB/LLM con datos comunitarios</td></tr>
<tr><td>🔵 C</td><td>3</td><td>Traducción LLM tentativa</td><td><b>Todo:</b> voz (fine-tune TTS con corpus consentido), traducción, validación</td></tr>
<tr><td>🔴 D</td><td>~6,880</td><td>—</td><td><b>Stack completo:</b> datos de habla (Common Voice/FLORES/equivalentes), ortografía, comunidad socia, TTS+ASR+traducción propios</td></tr>
</table>
<p style="color:var(--mut);font-size:.85rem">Para las ~6,880 del tier D la ruta es la misma en todas:
<b>consentimiento comunitario → corpus abierto → fine-tune de modelos base abiertos
(MMS/VITS para voz, XLS-R/Whisper para oído, NLLB/LLM para traducción)</b>.
Ese es el proyecto de fondeo: no pedimos dinero para "un traductor" — pedimos datos y cómputo
para cerrar el hueco que los LLMs frontera no resuelven (medido: 0.01 en zapoteco).</p>
</div>

<div class="note"><b>⚠️ Aviso honesto:</b> la traducción automática a lenguas de bajos recursos puede tener errores —
verifícala con un hablante nativo antes de usarla en producción. La voz es <b>síntesis</b>
(Meta MMS-TTS), no una persona real. No distribuyas audio generado como "voz de la comunidad"
sin consentimiento. Código y datos: MIT/CC-BY según fuente.</div>
""")

PAGE_COBERTURA = page("Cobertura mundial de lenguas", NAV + r"""
<h1>🌍 Cobertura mundial</h1>
<div class="sub">Cada lengua registrada clasificada por lo que el sistema puede hacer HOY.
Generado desde <code>data/cobertura.json</code> — regenerar con
<code>tools/build_coverage_matrix.py</code>.</div>

<div class="card">
<div class="filters">
<input type="text" id="q" name="q" placeholder="Buscar lengua o ISO…" aria-label="Buscar lengua o código ISO" autocomplete="off">
<select id="tier" aria-label="Filtrar por tier de cobertura"><option value="">Todos los tiers</option><option value="A">🟢 A — voz + traducción</option><option value="B">🟡 B — solo voz</option><option value="C">🔵 C — solo texto</option></select>
<select id="reg" aria-label="Filtrar por región"></select>
<span id="count" style="color:var(--mut);font-size:.85rem;align-self:center" aria-live="polite"></span>
</div>
<div style="max-height:65vh;overflow:auto"><table>
<thead><tr><th scope="col">ISO</th><th scope="col">Lengua</th><th scope="col">Región</th><th scope="col">Familia</th><th scope="col">Orden</th><th scope="col">Google</th></tr></thead>
<tbody id="tbody"></tbody></table></div>
<div id="more" style="text-align:center;margin-top:10px"></div>
</div>
<div class="note">🔴 Tier D (sin datos en el registro): ~6,880 lenguas ISO 639-3 sin checkpoint MMS ni
datos cargados — ver sección Tier D en <code>docs/LENGUAS_COBERTURA_MUNDIAL.md</code>.</div>
<script>
let DATA=[],ROWS=[],PAGE=0;const PER=100;const $=s=>document.querySelector(s);
fetch('/api/coverage').then(r=>r.json()).then(d=>{
  for(const t of ['A','B','C'])for(const l of d.tiers[t]||[])DATA.push({...l,tier:t});
  const regs=[...new Set(DATA.map(l=>l.region))].sort();
  $('#reg').innerHTML='<option value="">Todas las regiones</option>'+regs.map(r=>`<option>${esc(r)}</option>`).join('');
  draw();
}).catch(()=>{$('#count').textContent='Error cargando datos';});
function draw(){
  const q=$('#q').value.toLowerCase(),t=$('#tier').value,r=$('#reg').value;
  ROWS=DATA.filter(l=>(!t||l.tier===t)&&(!r||l.region===r)&&(!q||l.name.toLowerCase().includes(q)||l.iso.includes(q)||l.family.toLowerCase().includes(q)));
  $('#count').textContent=ROWS.length+' lenguas';
  PAGE=0;render();
}
function render(){
  const rows=ROWS.slice(0,(PAGE+1)*PER);
  $('#tbody').innerHTML=rows.map(l=>`<tr><td><code>${l.iso}</code></td><td>${esc(l.name)}</td><td>${esc(l.region)}</td><td>${esc(l.family)}</td><td>${esc(l.order)}</td><td>${l.google==='—'?'—':'<span class="tag ok">'+l.google+'</span>'}</td></tr>`).join('');
  const left=ROWS.length-rows.length;
  $('#more').innerHTML=left>0?`<button type="button" id="morebtn">Mostrar ${Math.min(PER,left)} más (${left} restantes)</button>`:'';
  const mb=$('#morebtn');if(mb)mb.onclick=()=>{PAGE++;render();};
}
['q','tier','reg'].forEach(id=>$('#'+id).addEventListener('input',draw));
function esc(s){return String(s??'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
</script>""")

PAGE_APP = page("Conversor — texto/video → audio", NAV + r"""
<div class="note"><b>Aviso honesto:</b> la traducción automática a lenguas de bajos recursos puede tener errores —
verifícala con un hablante nativo. La voz es <b>síntesis</b> (MMS-TTS), no una persona real.</div>
<div class="card">
<label for="lang">Lengua destino</label>
<div style="display:flex;gap:10px;flex-wrap:wrap">
  <select id="lang" style="flex:2;min-width:200px" aria-describedby="lang-hint"></select>
  <input type="text" id="iso" name="iso" placeholder="o ISO 639-3 libre (ej. quz, haw…)" aria-label="Código ISO 639-3 libre" spellcheck="false" style="flex:1;min-width:160px">
</div>
<label for="txt">Texto en español</label>
<textarea id="txt" name="text" placeholder="Escribe aquí…"></textarea>
<label for="url">— o URL de YouTube —</label>
<input type="url" id="url" name="url" placeholder="https://youtube.com/watch?v=…" autocomplete="off" spellcheck="false">
<label for="engine">Motor de traducción</label>
<select id="engine"><option value="auto">Auto (mejor disponible)</option><option value="google">Google Translate</option><option value="groq">Groq (LLM)</option><option value="llama">Ollama local</option></select>
<button id="go" type="button">Generar</button>
</div>
<div id="prog" class="card hidden" aria-live="polite"><b>Progreso</b><div class="steps" id="steps" aria-hidden="true"></div><div id="status" class="mono" role="status"></div></div>
<div id="res" class="card hidden" aria-live="polite"><b>Resultado</b><div class="badges" id="badges"></div><div id="result"></div></div>
<script>
const $=s=>document.querySelector(s);
const STEP_TXT={download:'Descargando video',transcribe:'Transcribiendo',translate:'Traduciendo',tts:'Sintetizando voz',done:'Listo'};
fetch('/api/languages').then(r=>r.json()).then(d=>{
  const sel=$('#lang');
  d.forEach(l=>{const o=document.createElement('option');o.value=l.code;
    o.textContent=l.name+(l.voice?'':'  (solo texto)')+(l.engine==='google'?'  ★Google':'');
    sel.appendChild(o);});
  sel.value='yua';
}).catch(()=>{$('#status')&&($('#status').textContent='Error cargando lenguas');});
$('#go').onclick=async()=>{
  const lang=$('#iso').value.trim()||$('#lang').value;
  const inp=$('#txt').value.trim()||$('#url').value.trim();
  if(!lang||!inp){$('#status').textContent='Elige lengua y pega texto o URL';$('#prog').classList.remove('hidden');$('#res').classList.add('hidden');return;}
  $('#go').disabled=true;$('#res').classList.add('hidden');$('#prog').classList.remove('hidden');
  $('#steps').innerHTML='';$('#status').textContent='Iniciando…';
  try{
    const r=await fetch('/api/convert',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({input:inp,lang,translator:$('#engine').value})});
    const j0=await r.json();
    if(j0.error){$('#go').disabled=false;$('#status').textContent='Error: '+j0.error;return;}
    let polls=0;
    const t=setInterval(async()=>{
      polls++;
      if(polls>400){clearInterval(t);$('#go').disabled=false;
        $('#status').textContent='Tiempo agotado — el job sigue en el servidor, reintenta más tarde.';return;}
      try{
        const j=await (await fetch('/api/jobs/'+j0.job)).json();
        const done=new Set(j.steps||[]);
        $('#steps').innerHTML=['download','transcribe','translate','tts','done'].map(k=>
          `<span class="${k==='done'&&j.status==='done'?'done':done.has(k)?'done':k===j.step?'on':''}">${STEP_TXT[k]}</span>`).join('');
        $('#status').textContent=j.status==='running'?'Procesando…':(j.status==='error'?'Error':'Listo');
        if(j.status==='done'||j.status==='error'){clearInterval(t);finish(j);}
      }catch(e){/* reintenta en el próximo tick */}
    },1200);
  }catch(e){$('#go').disabled=false;$('#status').textContent='Error de red: '+e;}
};
function finish(j){
  $('#go').disabled=false;const r=j.result||{};$('#res').classList.remove('hidden');
  const b=$('#badges');b.innerHTML='';
  const badge=(t,c)=>b.insertAdjacentHTML('beforeend',`<span class="badge ${c}">${t}</span>`);
  if(r.engine&&r.engine!=='none')badge('motor: '+r.engine,'b-info');
  if(r.tts){badge(r.tts.coverage<1?`alfabeto ${(r.tts.coverage*100).toFixed(0)}%`:'alfabeto 100%',r.tts.coverage<1?'b-warn':'b-ok');badge(r.tts.seconds+'s audio','b-ok');}
  if(r.text_only)badge('SOLO TEXTO (sin voz MMS)','b-no');
  let h='';
  if(j.status==='error'||r.error)h+=`<div class="err" role="alert">Error: ${esc(j.error||r.error||'desconocido')}</div>`;
  if(r.suggestions&&r.suggestions.length)h+=`<div style="color:var(--warn);font-size:.85rem;margin-top:4px">¿Quisiste decir? ${r.suggestions.map(esc).join(', ')}</div>`;
  if(r.translation)h+=`<div class="lbl">Traducción</div><div class="mono">${esc(r.translation)}</div>`;
  if(r.back_translation)h+=`<div class="lbl">↩ Significa en español (verificación)</div><div class="mono" style="border-color:#1d5c38">${esc(r.back_translation)}</div>`;
  if(r.source_text&&r.translation)h+=`<div class="lbl">Texto fuente</div><div class="mono">${esc(r.source_text).slice(0,600)}</div>`;
  const f=r.files||{};
  const AUDIO_EXT=/\.(wav|webm|m4a|mp3|ogg|opus)$/;
  for(const [k,name] of Object.entries(f)){
    if(AUDIO_EXT.test(name))
      h+=`<div class="lbl">${k==='audio'?'Audio':k==='audio_fuente'?'Audio fuente':'Audio'}</div><audio controls src="/audio/${name}"></audio><div><a href="/audio/${name}" download>⬇ Descargar ${name}</a></div>`;
    else if(name.endsWith('.txt'))
      h+=`<div><a href="/audio/${name}" download>⬇ ${k}: ${name}</a></div>`;
  }
  $('#result').innerHTML=h;
}
function esc(s){return String(s??'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
</script>""")

PAGES = {"/": PAGE_LANDING, "/cobertura": PAGE_COBERTURA, "/convertir": PAGE_APP}

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, body, ctype="application/json", extra=None):
        data = body if isinstance(body, bytes) else body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy",
                         "default-src 'self'; style-src 'unsafe-inline'; media-src 'self' blob:")
        for k, v in (extra or {}).items(): self.send_header(k, v)
        self.end_headers(); self.wfile.write(data)
    def _json(self, code, obj): self._send(code, json.dumps(obj, ensure_ascii=False))

    def do_GET(self):
        u = urlparse(self.path); p = u.path
        if p in PAGES:
            self._send(200, PAGES[p], "text/html; charset=utf-8"); return
        if p == "/api/languages":
            self._json(200, language_catalog()); return
        if p == "/api/coverage":
            self._json(200, coverage()); return
        m = re.fullmatch(r"/api/jobs/([0-9a-f]{12})", p)
        if m:
            with JOBS_LOCK:
                j = JOBS.get(m.group(1))
                pub = None if j is None else {k: j[k] for k in ("status", "steps", "step", "result", "error") if k in j}
            self._json(200 if pub else 404, pub or {"error": "job not found"}); return
        m = re.fullmatch(r"/audio/([\w.\-]+\.(?:wav|webm|m4a|mp3|ogg|opus|txt))", p)
        if m:
            f = (OUTPUT_DIR / m.group(1)).resolve()
            if f.parent == OUTPUT_DIR and f.exists():
                mime = {".wav": "audio/wav", ".webm": "audio/webm", ".m4a": "audio/mp4",
                        ".mp3": "audio/mpeg", ".ogg": "audio/ogg", ".opus": "audio/ogg",
                        ".txt": "text/plain; charset=utf-8"}.get(f.suffix.lower(), "application/octet-stream")
                self._send(200, f.read_bytes(), mime); return
            self._json(404, {"error": "not found"}); return
        self._json(404, {"error": "not found"})

    def do_POST(self):
        if urlparse(self.path).path != "/api/convert":
            self._json(404, {"error": "not found"}); return
        try:
            n = min(int(self.headers.get("Content-Length", 0)), 2_000_000)
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
            # pruning: los jobs son efímeros; conservar solo la última hora
            cutoff = time.time() - 3600
            for old in [k for k, j in JOBS.items() if j.get("_ts", 0) < cutoff]:
                JOBS.pop(old, None)
            JOBS[jid] = {"status": "running", "steps": [], "step": None,
                         "result": None, "error": None, "_ts": time.time()}
        threading.Thread(target=run_job, args=(jid, inp, lang,
                                               body.get("translator", "auto")), daemon=True).start()
        self._json(202, {"job": jid})

if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    srv = ThreadingHTTPServer((HOST, PORT), H)
    print(f"🌿 http://{HOST}:{PORT}  —  / · /cobertura · /convertir")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
