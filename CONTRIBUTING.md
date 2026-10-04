# Contributing

Contributions welcome — especially around new languages, local translation fallbacks,
and dataset tooling.

## How to contribute

1. Fork the repo and create a branch (`git checkout -b feat/my-change`).
2. Keep the single-file pipeline readable — `conversor.py` is intentionally simple.
3. Test with **one language first** before batch changes:

   ```bash
   python3 conversor.py "Texto de prueba" --lang nah
   ```

4. Open a PR describing what changed and which language(s) you validated.

## Rules

- **No API keys in code.** Keys come from environment variables only.
- **Honesty in docs.** This project orchestrates existing models (Whisper, Gemini, MMS-TTS);
  it does not train new ones. Keep that framing in docs and comments.
- **Sanitize before committing:** run `grep -rn "AIza\|hf_\|api_key" .` — must return nothing.
- Do not add heavy dependencies without discussion; the value of the project is simplicity.

## Good first contributions

- Local/offline translation fallback (e.g., an open model via Ollama) for environments
  without Gemini access.
- Mapping for additional MMS-TTS languages (`--list-langs` shows supported codes).
- Better error messages when keys or models are missing.
