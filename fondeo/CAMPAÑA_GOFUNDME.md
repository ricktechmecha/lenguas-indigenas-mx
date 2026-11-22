# CAMPAÑA DE FONDEO — "Que el internet hable tu lengua"
*Copy listo para GoFundMe/Donadora + guion de video + checklist de assets*

---

## 🎯 Estrategia en 3 líneas

El donante NO entiende "pipeline de orquestación de modelos". SÍ entiende:
> **"Una abuelita en Yucatán no puede escuchar información de salud en maya. Construí la tecnología que lo resuelve. Ayúdame a grabar a los hablantes."**

Ángulo emocional + gasto concreto (pagar a hablantes nativos) + demo audible = campaña fundable.

---

## 📋 DATOS DE LA CAMPAÑA

**Título (ES):** `Que el internet hable maya: grabemos la primera biblioteca de voz indígena abierta`
**Título (EN):** `Help the internet speak Maya: building the first open indigenous voice library`

**Meta:** **$40,000 MXN** (~$2,000 USD)
*(alcanzable, y el 100% va a la acción visible: pagar hablantes + equipo)*

**Desglose público (transparencia = confianza = donativos):**
| Concepto | MXN |
|---|---|
| Remuneración a hablantes nativos (~15 hrs grabación, $1,500/hablante) | 22,500 |
| Equipo de grabación + viajes a comunidad | 10,000 |
| Validación y publicación del corpus | 4,500 |
| Comisión plataforma (~7%) | 3,000 |

---

## ✍️ COPY DE LA CAMPAÑA (ESPAÑOL)

*(Pegar directo en GoFundMe/Donadora — ajustar nombres)*

> ### Imagina que el internet nunca aprendió tu idioma
>
> En México, ~7 millones de personas hablan una lengua indígena. Para ellas, el internet casi no existe: las alertas de salud, los videos educativos, la información de sus derechos — todo llega en español, o no llega.
>
> Mi abuela [ajustar — usar historia real tuya] nació hablando maya. Aprendió español de adulta. Hoy, si quisiera escuchar las noticias en su propia lengua, no hay botón para eso. No existe.
>
> ### Construí la tecnología — falta la voz
>
> Soy desarrollador independiente en CDMX. Construí y publiqué (código abierto, gratis) una herramienta que convierte cualquier texto o video de YouTube en audio hablado en **8 lenguas indígenas mexicanas**: náhuatl, maya yucateco, mixteco, zapoteco, otomí, tzotzil, tzeltal y mam. Funciona hoy, en una computadora normal, sin pagarle a ninguna empresa de Silicon Valley.
>
> **👉 [VIDEO: escúchala funcionando]**
>
> Lo que falta es lo más humano: **voces reales**. La inteligencia artificial aprende de grabaciones, y casi no hay grabaciones abiertas de lenguas indígenas mexicanas — las que existen son grabaciones de misas o tribunales de hace décadas.
>
> ### Tu donativo paga directamente a hablantes nativos
>
> Con esta campaña vamos a Yucatán a grabar a hablantes nativos de maya — remunerados de forma justa — para crear el **primer corpus de voz abierto y gobernado por la propia comunidad**. Cada peso:
> - Paga a hablantes nativos por grabar y validar audios
> - Compra el equipo básico de grabación
> - Publica todo gratis y abierto, para que cualquier gobierno, escuela o app pueda hablar maya
>
> Los hablantes firman consentimiento informado y la comunidad decide cómo se usa su voz — no es extracción, es soberanía.
>
> ### ¿Por qué importa?
>
> Cuando el corpus exista: una radio comunitaria podrá publicar en maya el mismo día; una clínica podrá explicar un medicamento en la lengua de la paciente; un niño podrá escuchar un cuento en la lengua de sus abuelos. Por eso todo el proyecto es open-source: para que no dependa de mí, sino de todos.
>
> **Dona, comparte, o si hablas una lengua indígena — escríbeme.** Gracias de corazón. 🌿

## ✍️ SHORT VERSION (para compartir en redes)

> El internet le habla a 7 millones de mexicanos en un idioma que no es el suyo. Construí una herramienta gratis que convierte videos y textos a audio en 8 lenguas indígenas. Ahora necesito grabar hablantes nativos en Yucatán para crear la primera biblioteca de voz abierta en maya. Cada peso paga a hablantes. 🌿 [LINK]

## ✍️ ENGLISH VERSION (short, para GoFundMe internacional)

> 7 million Mexicans speak an indigenous language — and the internet barely speaks back. I built a free, open-source tool that turns any text or YouTube video into spoken audio in 8 Mexican indigenous languages. Now I need to record native speakers in Yucatán to create the first community-governed open voice corpus in Maya. Every dollar pays the speakers themselves. 🌿 [LINK]

---

## 🎬 GUION VIDEO DEMO (60 seg) — grabar con QuickTime + narración

| Tiempo | Pantalla | Voz en off (grábalo tú) |
|---|---|---|
| 0-5s | Texto grande: "7 millones de mexicanos no pueden escuchar el internet" | "Imagina que el internet nunca aprendió tu idioma." |
| 5-15s | Terminal corriendo `conversor.py --list-langs` (zoom a la tabla) | "Construí una herramienta gratuita que habla 8 lenguas indígenas mexicanas." |
| 15-30s | Correr `conversor.py "Bienvenidos a la comunidad..." --lang yua` en tiempo real (acelerar esperas) | "Le escribes cualquier texto — o le pegas un video de YouTube — y te lo devuelve hablado." |
| 30-40s | ▶️ Reproducir el .wav en maya generado — MOSTRAR el audio player | "Escucha. Esto es maya yucateco, generado hace diez segundos, sin empresas de por medio." |
| 40-50s | Tu cara / texto: "Falta la voz real" | "Pero la IA necesita voces reales — y casi no existen grabaciones abiertas. Vamos a Yucatán a grabarlas, pagando a los hablantes." |
| 50-60s | Texto: meta $40,000 + link + "cada peso paga a hablantes nativos" | "Dona lo que sea. Que el internet hable tu lengua." |

**Truco de grabación:** grabar terminal con `cmd+shift+5` (grabador nativo macOS), narración aparte con el cel o QuickTime, juntar en CapCut (gratis) o iMovie.

### Audios demo a generar ANTES del video:
```bash
export GOOGLE_API_KEY="tu_key"
export HF_TOKEN="tu_token"
cd ~/Documents/lenguas-indigenas
python3 conversor.py "Bienvenidos. Hoy aprendemos juntos a cuidar el agua de nuestra comunidad." --lang yua --output demo_maya
python3 conversor.py "Tu salud es importante. Escucha esta información en tu propia lengua." --lang nah --output demo_nahuatl
python3 conversor.py "Los abuelos nos enseñaron que la tierra se cuida sembrando." --lang zap --output demo_zapoteco
```

---

## 📸 ASSETS NECESARIOS (checklist)

- [ ] **Video demo 60s** (lo más importante — ver guion arriba)
- [ ] **Foto de portada de campaña** — tú + algo que comunique tech+lengua (ej. pantalla con la terminal + texto "¿Y si el internet hablara maya?"). 1200x675px mínimo
- [ ] **3 audios .wav** de muestra (maya, náhuatl, zapoteco) — subirlos al video y a un GitHub Release para linkear
- [ ] **Screenshot del repo GitHub** (prueba de que es real y público)
- [ ] **1-2 fotos tuyas** reales (confianza = cara real, no avatar)
- [ ] Foto del terreno/comunidad en Yucatán si la tienes
- [ ] GIF corto del pipeline corriendo (para README + redes)

## 📣 PLAN DE DIFUSIÓN (donde ponerla)

1. **Tu WhatsApp/familia/amigos primero** — el 70% de GoFundMe viene de tu red; sin empuje inicial la campaña se ve muerta
2. **LinkedIn** — post con el video + historia del proyecto
3. **Twitter/X** — hilo técnico (repo + demo audio) apuntando a comunidad OSS/ML (#IndigenousNLP, @huggingface)
4. **Reddit** — r/opensource, r/mexico (cuidado con self-promo rules — postear el PROYECTO, link campaña en comentarios)
5. **Comunidades NLP** — discord de HF, AmericasNLP mailing list, foros INALI
6. **Product Hunt / Hacker News** — "Show HN: turn YouTube videos into indigenous-language audio" (el PROYECTO, no la campaña — la campaña vive en tu perfil)

## ⚠️ Reglas de la casa para no matar la campaña

- Actualización de progreso cada 3-5 días (aunque sea "grabamos a María, 3 horas de audio") — campañas con updates recaudan 2x más
- Responder TODOS los comentarios/mensajes en <24h
- Nunca inflar lo que hace el software — la honestidad técnica es tu marca
- Si usas Donadora en vez de GoFundMe: tiene asesoría gratis incluida y mejor fit con causas MX
