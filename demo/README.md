# Demo — prueba el conversor en 30 segundos

```bash
# 1) Texto → audio maya (el más rápido; usa Google NMT + MMS, ~1 min la 1ª vez)
python3 conversor.py --demo texto --lang yua

# 2) Pipeline completo: audio local → transcripción → traducción → voz
python3 conversor.py --demo audio --lang yua
#    (demo_es.m4a = frase en español generada con `say` de macOS)

# 3) Tu propio audio/video descargado
python3 conversor.py ~/Downloads/mi_audio.mp3 --lang nah

# 4) O en la web: python3 app.py → /convertir → botón "Cargar ejemplo"
```

`texto_demo.txt` tiene 3 frases de prueba. `demo_es.m4a` es voz sintética
de macOS (Monica) — sirve para probar transcripción sin depender de YouTube.
