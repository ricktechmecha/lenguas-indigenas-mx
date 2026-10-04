# Security & Responsible Use

## API keys

- `GOOGLE_API_KEY` and `HF_TOKEN` are read **only** from environment variables.
- Never commit `.env` files, keys, or tokens — they are in `.gitignore`. Keep it that way.
- If a key is ever committed by accident, rotate it immediately, then scrub history.

## Generated content

- Translations into low-resource languages are produced by Gemini Flash and **contain errors**.
  Do not present generated audio as authoritative or as "the voice of a community".
- MMS-TTS voices are synthetic. Distributing generated audio as if it were recorded by native
  speakers raises indigenous data-sovereignty concerns (see UNESCO IDIL principles). Always
  label output as machine-generated and obtain consent when working with real communities.

## Inputs

- `conversor.py` downloads YouTube audio with `yt-dlp`. Download only content you have the
  right to use; respect the source platform's terms of service.
- Output `.wav` files may contain third-party content — treat them as derivative works.

## Reporting

If you find a security issue or leaked credential in this repo, open a private advisory via
GitHub Security Advisories rather than a public issue.
