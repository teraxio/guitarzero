# GZBR — Flujo de Producción de Videos para Skool

**Proyecto:** Guitar Zero to Band Rock (GZBR)
**Actualizado:** 2026-04-06
**Stack:** 100% local, sin APIs externas, sin costos recurrentes

---

## Resumen Ejecutivo

Grabas en Samsung → conectas por USB → corres 1 comando → listo para subir a Skool.
El script hace todo automáticamente en tu MacBook Air M1.

---

## Estructura de Carpetas en Disk JLV

```
/Volumes/Disk JLV/GuitarZerotoBandRock/VIDEOS/
├── 00-INTRODUCCION/
│   ├── raw/          ← Videos crudos del Samsung
│   └── editados/     ← Videos procesados
├── ICA-01/ a ICA-11/
│   ├── PRINCIPIANTE/
│   │   ├── raw/
│   │   └── editados/
│   └── INTERMEDIO/
│       ├── raw/
│       └── editados/
├── _PROCESADOS_SKOOL/         ← Copia final para subir
└── _SCRIPTS_PROCESAMIENTO/
    ├── procesar_videos.py     ← Script principal
    ├── instalar_dependencias.sh
    └── assets/
        ├── intro_gzbr.mp4     ← Coloca tu intro aquí
        └── outro_gzbr.mp4     ← Coloca tu outro aquí
```

**Total:** ~115 videos | 11 ICAs × (5 Principiante + 5 Intermedio) + Introducción

---

## Setup Inicial (1 sola vez)

Abre Terminal en tu Mac y ejecuta:

```bash
bash "/Volumes/Disk JLV/GuitarZerotoBandRock/VIDEOS/_SCRIPTS_PROCESAMIENTO/instalar_dependencias.sh"
```

Instala: FFmpeg + Whisper (GPU M1) + librerías Python (~10 min primera vez)

---

## Flujo de Trabajo (cada vez que grabes)

### PASO 1 — Grabar en Samsung
- Modo: horizontal (landscape), 1080p mínimo
- No importa la iluminación perfecta, el script corrige el color

### PASO 2 — Transferir al Mac
- Conectar Samsung con **cable USB**
- Abrir **Smart Switch**
- Copiar a: `/Volumes/Disk JLV/GuitarZerotoBandRock/VIDEOS/[ICA-XX]/[NIVEL]/raw/`

### PASO 3 — Procesar (1 comando)

```bash
# Un ICA completo (ambos niveles)
python3 "/Volumes/Disk JLV/GuitarZerotoBandRock/VIDEOS/_SCRIPTS_PROCESAMIENTO/procesar_videos.py" --ica ICA-03

# Solo un nivel
python3 "/Volumes/Disk JLV/GuitarZerotoBandRock/VIDEOS/_SCRIPTS_PROCESAMIENTO/procesar_videos.py" --ica ICA-03 --nivel PRINCIPIANTE

# Todos los videos pendientes
python3 "/Volumes/Disk JLV/GuitarZerotoBandRock/VIDEOS/_SCRIPTS_PROCESAMIENTO/procesar_videos.py" --todos

# Video individual
python3 "/Volumes/Disk JLV/GuitarZerotoBandRock/VIDEOS/_SCRIPTS_PROCESAMIENTO/procesar_videos.py" --archivo /ruta/video.mp4
```

### PASO 4 — Subir a Skool
- Los videos listos están en: `_PROCESADOS_SKOOL/`
- Arrastrar y soltar en Skool
- El archivo SRT de subtítulos está junto al MP4 si lo necesitas

---

## Lo que hace el Script Automáticamente

| Paso | Qué hace | Tecnología |
|---|---|---|
| 1 | Elimina GPS y metadatos del Samsung | FFmpeg |
| 2 | Corta silencios largos (>0.8 seg) | FFmpeg silenceremove |
| 3 | Transcribe y genera subtítulos .SRT | Whisper (GPU Metal M1) |
| 4 | Corta palabras de relleno (ums, eehs) | Whisper timestamps + FFmpeg |
| 5 | Corrección de color y brillo | FFmpeg normalize/eq |
| 6 | Añade intro y outro GZBR | FFmpeg concat |
| 7 | Exporta H.264 1080p optimizado web | FFmpeg x264 faststart |

**Costo:** $0 — todo corre en tu Mac, sin internet

---

## Por Voz desde WhatsApp

Di a Claude Code vía OpenClaw:

> "Procesa los videos del ICA-03 nivel principiante"
> "Procesa todos los videos pendientes"
> "Procesa el video de introducción"

---

## Intro y Outro GZBR

Para activar intro/outro, coloca tus archivos en:
```
_SCRIPTS_PROCESAMIENTO/assets/intro_gzbr.mp4
_SCRIPTS_PROCESAMIENTO/assets/outro_gzbr.mp4
```
- Duración recomendada: 5-10 segundos
- Resolución: 1920×1080
- Si no existen, el script los omite sin errores

---

## Consideraciones Redes Sociales USA

1. **Metadatos GPS** → eliminados automáticamente en cada video
2. **IP al subir** → usar VPN (servidor USA) en TikTok/Instagram
3. **Cuentas** → registrar con número USA: Google Voice o TextNow (gratis)
4. **Monetización** → Wise o Payoneer para cuenta bancaria USA (gratis)

---

## Comandos de Diagnóstico

```bash
# Verificar que FFmpeg está instalado
ffmpeg -version

# Ver videos pendientes de procesar
find "/Volumes/Disk JLV/GuitarZerotoBandRock/VIDEOS" -name "*.mp4" -path "*/raw/*" | wc -l

# Ver videos ya procesados
find "/Volumes/Disk JLV/GuitarZerotoBandRock/VIDEOS" -name "*.mp4" -path "*/editados/*" | wc -l

# Ver todos listos para Skool
ls "/Volumes/Disk JLV/GuitarZerotoBandRock/VIDEOS/_PROCESADOS_SKOOL/"
```

---

## Volumen Total Estimado

| Contenido | Videos |
|---|---|
| Introducción | ~5 |
| 11 ICAs × 5 Principiante | 55 |
| 11 ICAs × 5 Intermedio | 55 |
| **TOTAL** | **~115 videos** |

---

*Generado por Claude Code — 2026-04-06*
*Actualizar este documento: pedirle a Claude Code vía WhatsApp/OpenClaw*
