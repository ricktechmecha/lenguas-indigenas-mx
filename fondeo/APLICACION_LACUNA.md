# Lacuna Fund — plantilla para la próxima convocatoria

> ⚠️ **Estado:** la convocatoria ACTS/Lacuna del 13-nov-2026 **ya cerró**
> (era para usar datasets Lacuna existentes, $10k, equipos del Sur Global).
> Esta plantilla queda lista para la próxima llamada de Lacuna Fund
> (suelen abrir 1–2 veces al año — monitorear lacunafund.org/apply/).
> El proyecto encaja PERFECTO en su tesis: datasets abiertos para ML en
> contextos de bajos recursos del Sur Global.

---

## Posicionamiento (por qué Lacuna es el fondo ideal)

Lacuna financia **datasets abiertos** — y el cuello de botella medido de
este proyecto es exactamente eso: no hay corpus de habla consentidos para
las lenguas mexicanas desatendidas. Nuestro plan no pide "un modelo":
pide **el dataset que falta**, con gobernanza comunitaria desde el diseño.

## Project title

**Lenguas Vivas MX: corpus de habla abierto y consentido para 3 lenguas
indígenas mexicanas desatendidas**

## Summary (~150 palabras, EN)

> We request funding to create and release an open, community-governed
> speech corpus for three Mexican indigenous languages with no usable
> digital voice — starting with Yucatec Maya (yua), Isthmus Zapotec (zai)
> and a third language selected with community partners (candidates:
> Wixárika hch, Tzotzil tzo, Tzeltal tzh — the only ones with zero published
> voice checkpoints). The corpus will include parallel text-audio pairs,
> speaker metadata, consent records per CARE Principles for Indigenous Data
> Governance, and a documentation playbook. We will validate utility by
> fine-tuning open TTS models (VITS/MMS) and reporting honest
> speaker-validated scores. All data will be openly licensed for research
> and community use.

## Why these languages / why now

- Our published coverage matrix shows exactly which languages have voice,
  which don't, and which have no data at all — the selection is evidence-
  driven, not arbitrary.
- ~7M speakers in Mexico; most content (health, education, government)
  exists only in Spanish.
- Frontier LLMs fail measurably (0.00–0.49); the gap is data, not algorithm.

## Dataset specification (lo que entregaríamos)

| Componente | Detalle |
|---|---|
| Lenguas | 3 (yua + zai + una tier-C por decisión comunitaria) |
| Hablantes | 15–25 por lengua, remunerados, con consent informado |
| Horas estimadas | ~20–40h por lengua (frases + lectura + conversación) |
| Formato | WAV 16kHz + transcripción ES + traducción validada |
| Licencia | CC-BY / community-governed charter (CARE) |
| Repo | HuggingFace dataset + documentación |

## Presupuesto orientativo (USD)

- Grabación + compensación hablantes: $12–18k
- Validación + talleres comunitarios: $4–6k
- Herramientas + publicación: $2k
- **Total: ~$20–26k** (alineado a montos típicos Lacuna)

## Checklist para cuando abra la convocatoria

- [ ] Confirmar que somos elegibles (Lacuna pide equipos, a veces Global South — CDMX califica como contexto; somos individuo → buscar partner institucional si lo piden: universidad, OSC)
- [ ] Definir 3ª lengua con comunidad socia
- [ ] Carta de apoyo de la comunidad/organización local
- [ ] Presupuesto detallado + carta de compromiso de datos abiertos
- [ ] Monitorear: lacunafund.org/apply + newsletter
