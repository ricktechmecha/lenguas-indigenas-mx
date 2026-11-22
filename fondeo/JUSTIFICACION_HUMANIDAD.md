# Por qué esto ayuda a la humanidad — la justificación maestra

> Documento base para todas las solicitudes de fondeo. Todo lo que aquí se
> afirma está medido y es verificable en el repo — nada de promesas vagas.

## El problema en una frase

**7 millones de personas en México hablan lenguas indígenas; para internet,
la mayoría de esas lenguas no existen.** No es metáfora: no hay voz, no hay
traducción usable, no hay datos. Cuando el gobierno, un hospital o una
emergencia necesita decir algo en maya, náhuatl o zapoteco, hoy no hay
manera automática de hacerlo.

## La evidencia medida (no opinión)

| Hecho | Dónde está la prueba |
|---|---|
| Los LLM frontera FALLAN en estas lenguas | zapoteco: 0.00–0.01 con gpt-oss-120b (se niega o inventa). Documentado en `docs/MAPA_DEL_HUECO.md` |
| El NMT dedicado sí produce lengua real | Google NMT: 0.58–0.75 round-trip en 8 lenguas (maya, náhuatl, mam, k'ekchí, zapoteco, quechua, aymara, guaraní) |
| La voz ya existe pero nadie la conecta | Meta MMS-TTS tiene ~999 checkpoints; nadie había orquestado traducción+voz+evaluación honesta para el mundo |
| El hueco es mundial | ~6,880 lenguas vivas (ISO 639-3) sin datos ni voz en ningún sistema mainstream — `docs/LENGUAS_COBERTURA_MUNDIAL.md` |
| Funciona de verdad HOY | Pipeline E2E verificado: texto y video de YouTube → audio en lengua destino (`python3 app.py`) |

## Por qué la humanidad lo necesita

1. **Accesibilidad = derecho, no lujo.** La información de salud, educación,
   alertas de desastre y servicios gubernamentales que solo existen en
   español excluyen a millones. Audio en lengua propia es la vía de acceso
   para comunidades con baja alfabetización en español.
2. **La voz es identidad.** Una lengua sin presencia digital muere más rápido.
   Cada checkpoint MMS que se usa, cada corpus que se graba con consentimiento,
   es una lengua que sigue existiendo en el siglo XXI.
3. **Soberanía de datos indígenas.** Las comunidades deciden cómo se usan sus
   voces y textos (CARE Principles). Este proyecto nace con esa regla, no la
   agrega después — es lo que los financiadores de impacto buscan.
4. **Bien público, no mercado.** 7M de hablantes fragmentados en 68 lenguas no
   es un mercado para Big Tech — por eso nadie lo construye. Es exactamente
   el tipo de bien público que Mozilla, NLnet, Lacuna e ISOC financian.
5. **El modelo de negocio no es la respuesta; la infraestructura sí.** No
   pedimos que nadie "compre traducción". Pedimos datos, cómputo y tiempo para
   construir la capa abierta que cualquier comunidad, gobierno o startup
   pueda usar después.

## Por qué este equipo/proyecto merece el apoyo

- **Ya funciona** — no es una idea: repo público, pipeline E2E, sitio en vivo,
  métricas publicadas. La mayoría de las propuestas de fondeo son "vamos a
  construir"; esta es "ya construimos la prueba de concepto y medimos el hueco".
- **Honestidad técnica como metodología** — publicamos nuestros scores malos
  (0.00 en zapoteco con LLM) junto a los buenos. Eso es lo que hace creíble el
  plan: sabemos exactamente dónde falla y por qué.
- **Stack 100% abierto y reproducible** — Whisper, MMS-TTS, NLLB, WALS,
  PHOIBLE, Google NMT (API pública documentada). Cualquier revisor puede
  correr `python3 app.py` y verificarlo en 5 minutos.
- **Plan por tiers con recursos explícitos** — `docs/PLAN_RECURSOS_POR_IDIOMA.md`
  dice exactamente qué falta por lengua y qué se pide por ello. Los jueces
  odian ambigüedad; esto es una lista de compras.
- **Enfoque México → mundo** — empezamos donde el problema es más agudo
  (68 agrupaciones INALI) y la arquitectura ya escala a cualquier ISO 639-3.

## El pedido concreto

| Fondo | Monto | Para qué |
|---|---|---|
| Mozilla Fellowship | $125k/12m | tiempo completo: corpus comunitario + validación + playbook replicable |
| NLnet Restack | €5–50k | R&D: fine-tune TTS/traducción para tier C + alineación de doblaje |
| Lacuna Fund | ~$10–30k | datasets de habla consentidos (el requisito #1) |
| UNESCO PP | hasta $26k | proyecto piloto documentado con comisión nacional |
| GoFundMe | lo que la comunidad dé | demo/video + micro-grabaciones de control |

## Frase de cierre (usable en cualquier solicitud)

> *"No estamos pidiendo que la tecnología 'aprenda' estas lenguas por
> accidente. Estamos construyendo, con las comunidades dueñas de las voces,
> la infraestructura abierta para que el próximo sistema —de salud, de
> educación, de emergencia— pueda hablarles en su propia lengua."*
