# ROADMAP DE FONDEO — Lenguas Indígenas MX
*Actualizado: 22-nov-2026*

## 🔴 DEADLINES — en orden de urgencia

| # | Fondeo | Premio | Deadline | Estado | Doc |
|---|--------|--------|----------|--------|-----|
| 1 | **Mozilla Foundation Fellowship** | $125,000 USD / 12 meses | **17-dic-2026** (LOI ligera, no app completa) | 🟡 Borrador listo | `APLICACION_MOZILLA_FELLOWSHIP.md` |
| 2 | **NLnet Restack** | €5,000–50,000 | 3-ene-2027 | ⚠️ **GenAI fuera de scope** salvo >1M usuarios — solo aplicar reformulado como open-data commons si sobra tiempo | `APLICACION_NLNET_RESTACK.md` |
| 3 | **FLOSS/fund** | Variable | Rolling | 🟡 `funding.json` creado — falta enviar en floss.fund/submit | — |
| 4 | **GitHub Sponsors** | Recurrente | Ya | 🟡 `FUNDING.yml` creado — falta activar en github.com/sponsors | — |
| 5 | **GoFundMe / Donadora** | Meta $40,000 MXN | Cuando tengas el video | 🟡 Copy y guion listos | `CAMPAÑA_GOFUNDME.md` |

## 👁️ PRÓXIMO CICLO — prepararse desde ya

| Fondeo | Monto | Notas |
|--------|-------|-------|
| **Lacuna Fund NLP** | hasta $250K | EL grant perfecto (lenguas bajos recursos LATAM). Ciclo ~anual, cerró 13-oct-2026. Requisito clave: corpus abierto con comunidad — la campaña de grabación ES la preparación |
| **Meta Llama Impact** | $35K–500K | ✅ YA elegible en papel — `conversor.py` ahora tiene `--translator llama` local |
| **AmericasNLP 2027** | Visibilidad académica | Papers ~ene-abr 2027. Escribir technical report del pipeline |
| **Google Gemini Competition** | hasta $300K | Sin edición nueva confirmada; el pipeline ya usa Gemini |
| **MIT Solve / Fast Forward** | Variable | Ciclos anuales Q1 2027 |

## 📋 Requisitos detallados por programa → ver `REQUISITOS_Y_DOCUMENTOS.md`

Nuevos hallazgos (22-nov):
- Mozilla = solo **Letter of Intent** el 17-dic (ligera) — full app solo si te invitan (mar-2027)
- Restack: GenAI fuera de scope — depriorizar
- SECIHTI: registrarse en **Rizoma** + alta PFAE en SAT = llave federal
- SACPC Lenguas Indígenas $100K: titular debe ser hablante → socio maya
- Jugada maestra: email UADY (desbloquea SECTEI/SECIHTI/Lacuna/SACPC)

## ✅ Checklist semanal

- [ ] Push de `funding.json`, `FUNDING.yml`, `conversor.py` (Llama fallback) a GitHub
- [ ] Activar GitHub Sponsors: github.com/sponsors → enroll
- [ ] Enviar funding.json en floss.fund/submit
- [ ] Enviar aplicación Mozilla Fellowship (copiar de `APLICACION_MOZILLA_FELLOWSHIP.md`)
- [ ] Enviar aplicación NLnet Restack en nlnet.nl/propose
- [ ] Generar audios demo (`python3 conversor.py "..." --lang yua`)
- [ ] Grabar video 60s según `CAMPAÑA_GOFUNDME.md`
- [ ] Publicar campaña GoFundMe o Donadora
- [ ] `brew install ollama && ollama pull llama3.1:8b` (para probar fallback local)

## 💰 Ingresos en paralelo (mientras caen los grants)

- Outlier / DataAnnotation / Mercor — $20-45 USD/hr evaluando modelos, este repo es el CV
- Freelance: bots WhatsApp + automatización AI para negocios locales
- Los grants son lotería: disparar a TODOS, no apostar a uno
