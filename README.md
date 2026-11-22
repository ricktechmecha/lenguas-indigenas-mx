# Lenguas Indígenas MX 🇲🇽

**Convert text or YouTube videos into spoken audio in Mexican indigenous languages.**

An accessibility-focused pipeline that takes Spanish content (plain text or a YouTube URL) and produces a `.wav` narration in one of 8 indigenous languages of Mexico — orchestrating existing open models rather than training new ones.

```
Text / YouTube URL
      │
      ▼
  yt-dlp ──► audio (mp3)
      │
      ▼
  Whisper (local CLI or Groq API) ──► Spanish transcript
      │
      ▼
  LLM translation ──► target language
  (Groq · Gemini · Ollama Cloud · Cerebras · local Llama)
      │
      ▼
  Meta MMS-TTS ──► .wav in indigenous language
```

## Supported languages

| Code | Language | Approx. speakers | MMS-TTS model |
|------|----------|------------------|----------------|
| `nah` | Náhuatl | 1.7 M | `facebook/mms-tts-nah` |
| `yua` | Maya Yucateco | 800 K | `facebook/mms-tts-yua` |
| `mix` | Mixteco (Tu'un savi) | 500 K | `facebook/mms-tts-mix` |
| `zap` | Zapoteco | 400 K | `facebook/mms-tts-zap` |
| `oto` | Otomí / Hñähñu | 300 K | `facebook/mms-tts-oto` |
| `tzo` | Tzotzil | 400 K | `facebook/mms-tts-tzo` |
| `tzh` | Tzeltal | 500 K | `facebook/mms-tts-tzh` |
| `mam` | Mam | 600 K | `facebook/mms-tts-mam` |

Mexico has 68 linguistic groupings and 364 variants (INALI). MMS-TTS also ships checkpoints for specific regional variants (e.g. Náhuatl de Guerrero `ngu`, Náhuatl del Norte de Oaxaca `nhy`, Náhuatl de la Huasteca `nch`) — mapping INALI variants to their closest MMS checkpoint is on the roadmap.

## Install

Requires **Python 3.12** plus a few system tools:

```bash
# System dependencies (macOS example)
brew install yt-dlp openai-whisper ffmpeg

# Python dependencies
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## API keys

Only **one** working translator backend is needed — the rest are optional fallbacks.
Keys can live in a `.env` file in the project root (auto-loaded, gitignored) or as env vars.

```bash
# Option A — Groq (recommended: free tier, fast, also powers Whisper STT)
export GROQ_API_KEY="gsk_..."          # console.groq.com — free

# Option B — Google Gemini
export GOOGLE_API_KEY="AIza..."        # aistudio.google.com — free tier

# Option C — fully offline, no keys at all
brew install ollama && ollama pull llama3.1:8b && ollama serve
# then run with --translator llama

# Optional extras
export HF_TOKEN="hf_..."               # only if HF rate-limits model downloads
export OLLAMA_API_KEY="..."            # ollama.com cloud (paid credits)
export CEREBRAS_API_KEY="..."          # cerebras.ai (paid)
```

**Key rotation:** numbered variants are picked up automatically —
`GROQ_API_KEY`, `GROQ_API_KEY_2` … `_5` are tried in order on rate-limit or
auth errors. Works for `GOOGLE_API_KEY`, `OLLAMA_API_KEY` and `CEREBRAS_API_KEY` too.

## Usage

```bash
# List supported languages
python3 conversor.py --list-langs

# Spanish text → audio in Náhuatl
python3 conversor.py "Bienvenidos a la comunidad. Hoy aprenderemos juntos." --lang nah

# YouTube video → audio in Maya Yucateco
python3 conversor.py "https://youtube.com/watch?v=VIDEO_ID" --lang yua

# Custom output directory
python3 conversor.py "texto" --lang mix --outdir ./salida

# Fully offline: translate with local Llama via Ollama instead of Gemini
# (requires: brew install ollama && ollama pull llama3.1:8b && ollama serve)
python3 conversor.py "texto" --lang nah --translator llama
```

**Translator options** (`--translator`):

| Value | Backend | Cost |
|-------|---------|------|
| `auto` (default) | Tries every backend with a configured key: groq → gemini → ollama-cloud → cerebras → llama | — |
| `groq` | Groq cloud, `openai/gpt-oss-120b` (set `GROQ_MODEL` to override) | Free tier |
| `gemini` | Google Gemini 2.0 Flash | Free tier |
| `ollama-cloud` | ollama.com hosted models (`OLLAMA_CLOUD_MODEL`, default `gemma4:31b`) | Paid credits |
| `cerebras` | cerebras.ai (`CEREBRAS_MODEL`, default `gpt-oss-120b`) | Paid |
| `llama` | Local Llama via [Ollama](https://ollama.com) — no key, works offline | Free |

**Transcription options** (`--stt`, YouTube input only): `auto` (default — Groq
Whisper API when `GROQ_API_KEY` is set, else local `whisper` CLI), `groq`, `local`.

Output `.wav` files are written to `output_audio/` by default.

## Honest limitations

- **This is orchestration, not new models.** Whisper, Gemini and MMS-TTS do the heavy lifting; this project wires them into a usable accessibility tool.
- **Translation quality varies.** Gemini's output in low-resource languages contains errors — always have a native speaker review content meant for communities.
- **MMS-TTS voices are synthetic** and generic; they are not recordings of community members and should not be presented as such.
- **MMS models are released under CC-BY-NC-4.0** (non-commercial). This code is MIT, but generated audio falls under the models' license terms.

## Ethics & data sovereignty

Indigenous languages are living heritage, not raw material. If you extend this tool to collect recordings:

- Obtain informed consent from speakers before recording or publishing audio.
- Do not distribute generated speech as "the voice of a community."
- Share resulting datasets openly, with communities retaining agency over their use.

## Roadmap

- [ ] Map INALI's 364 language variants to specific MMS checkpoints
- [ ] Corpus mode: guided recording sessions with native speakers for an open dataset
- [ ] Human-review workflow for translations (community validation loop)
- [x] Local open-source LLM fallback for translation (offline / key-free operation via Ollama)
- [ ] Batch mode for institutional content (schools, community radio, public notices)

## Why this exists

Public institutions in Mexico are legally required to communicate in indigenous languages, yet almost no content reaches native speakers in audio form. This tool lowers the cost of producing that audio — for accessibility, preservation, and reach.

## License

Code: [MIT](LICENSE). Models retain their own licenses (MMS-TTS: CC-BY-NC-4.0; Whisper: MIT).
