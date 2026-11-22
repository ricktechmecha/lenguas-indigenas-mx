# NLnet — Open Internet Stack "Restack" — borrador de propuesta

**Fondo:** Restack (sucesor de NGI Zero) — grants R&D **€5,000–€50,000**,
llamadas abiertas cada ~2 meses. Verificado 2026-11-22:
siguiente ventana de deadline ~**3-ene-2027** (ciclo abierto desde 3-nov).
Portal: nlnet.nl → Apply for funding → Restack / open call.

> Restack financia "digital commons" en toda la pila: datos abiertos,
> software libre, estándares abiertos. Nuestro encaje: **open speech data +
> open models + open evaluation** para lenguas desatendidas = internet stack
> más inclusivo.

---

## Project title

**Voces Abiertas: corpus de habla consentido y modelos abiertos para
lenguas indígenas de bajos recursos**

## Abstract (~150 palabras, EN)

> We propose to build the missing data layer for linguistic equity on the
> open internet: a consent-governed speech corpus for Mexican indigenous
> languages (starting with Yucatec Maya and Isthmus Zapotec), used to
> fine-tune open speech models (VITS/MMS-TTS for voice, LoRA adapters for
> translation) and to publish the evaluation harness that makes progress
> measurable. Motivation is measured, not rhetorical: frontier LLMs score
> 0.00–0.49 on back-translation into these languages while open NMT reaches
> 0.58–0.75 — the bottleneck is community-owned data, which no commercial
> actor will fund. All outputs (audio, text, code, evals) will be open
> license and reusable by any community worldwide.

## Why this fits Restack

- **Open data commons:** the corpus itself is the contribution — CARE-
  governed, openly licensed, documented.
- **Open source everywhere:** pipeline already MIT; models are open
  (MMS/VITS/NLLB); evaluation tools open.
- **User autonomy:** communities own their linguistic data — the opposite
  of vendor lock-in.
- **Reusability:** playbook replicable for any of the ~6,880 uncovered
  languages in our coverage matrix.

## Work plan (12 meses, hitos)

1. **Meses 1–3:** protocolo de consentimiento + grabación piloto (30–50
   hablantes, maya yucateco + zapoteco del Istmo), gobernanza comunitaria.
2. **Meses 4–6:** limpieza/segmentación del corpus; fine-tune VITS desde
   checkpoint MMS base; evaluación con hablantes.
3. **Meses 7–9:** adaptador de traducción (LoRA sobre NLLB/LLM abierto)
   entrenado con pares del corpus + diccionarios abiertos.
4. **Meses 10–12:** publicación del dataset + modelos + harness de
   evaluación; playbook replicable; blogpost técnico abierto.

## Budget (EUR, propuesta)

| Concepto | EUR |
|---|---|
| Compensación hablantes + logística grabación | 18,000 |
| GPU cloud (fine-tuning ~200–400h) | 10,000 |
| Validación con comunidades (talleres) | 8,000 |
| Desarrollo + documentación + diseminación | 9,000 |
| Contingencia | 5,000 |
| **Total** | **~50,000** |

> Si el tope del ciclo es menor, escalar a ~€25k: solo maya yucateco,
> corpus más pequeño, mismos entregables de datos abiertos.

## Current status / proof of work

- Pipeline E2E público y verificado: `python3 app.py` → texto/YouTube →
  audio en lengua destino (116 lenguas con cobertura completa hoy).
- Matriz de cobertura mundial honesta: 116 completas / 901 voz-sin-
  traducción / 3 solo-texto / ~6,880 sin datos.
- Métricas publicadas: `docs/MAPA_DEL_HUECO.md` (LLM 0.00–0.49 vs NMT
  0.58–0.75 en 8 lenguas).
- Repo: https://github.com/ricktechmecha/lenguas-indigenas-mx

## Equipo

- **Rick Rodríguez** — desarrollador independiente, CDMX. Construyó todo el
  pipeline, la evaluación y la matriz de cobertura.
- **[Por confirmar]** Lingüista/antropólogo aliado para gobernanza del
  corpus; comunidad socia en Yucatán (por formalizar — mencionar nombre si
  existe antes de enviar).
