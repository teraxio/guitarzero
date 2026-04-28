# GZBR — Pipeline de Videos · Punto de Recuperación

> **Actualizado:** 2026-04-06 | **Mac:** MacBook Air M1 | **Disco:** /Volumes/Disk JLV

---

## ¿Dónde estamos?

La máquina se congeló **antes de instalar las dependencias**. El script ya está creado y listo. Solo falta correr la instalación.

---

## Paso 1 — Instalar dependencias (1 sola vez)

Abre una **ventana nueva de Terminal** y ejecuta:

```
bash "/Volumes/Disk JLV/GuitarZerotoBandRock/VIDEOS/_SCRIPTS_PROCESAMIENTO/instalar_dependencias.sh"
```

Tarda ~10 minutos. Espera el mensaje: `Instalación completa.`

---

## Paso 2 — Verificar que todo quedó bien

```
ffmpeg -version
python3 -c "import ffmpeg, whisper, webrtcvad; print('TODO OK')"
```

Si dice `TODO OK` → listo para procesar videos.

---

## Paso 3 — Procesar videos

```
# Un ICA completo
python3 "/Volumes/Disk JLV/GuitarZerotoBandRock/VIDEOS/_SCRIPTS_PROCESAMIENTO/procesar_videos.py" --ica ICA-01

# Solo un nivel
python3 "...procesar_videos.py" --ica ICA-01 --nivel PRINCIPIANTE

# Todos los pendientes de una vez
python3 "...procesar_videos.py" --todos
```

Los videos listos quedan en: `/Volumes/Disk JLV/GuitarZerotoBandRock/VIDEOS/_PROCESADOS_SKOOL/`

---

## Estado de dependencias al 2026-04-06

| Herramienta | Estado |
| --- | --- |
| Python 3.9.6 | ✅ OK |
| numpy | ✅ OK |
| FFmpeg | ❌ Falta instalar |
| ffmpeg-python | ❌ Falta instalar |
| openai-whisper | ❌ Falta instalar |
| mlx-whisper (GPU M1) | ❌ Falta instalar |
| webrtcvad | ❌ Falta instalar |

---

## Estructura de carpetas

```
/Volumes/Disk JLV/GuitarZerotoBandRock/VIDEOS/
├── 00-INTRODUCCION/
├── ICA-01/ … ICA-11/
│   ├── PRINCIPIANTE/
│   │   ├── raw/       ← videos crudos del Samsung aquí
│   │   └── editados/  ← procesados automáticamente
│   └── INTERMEDIO/
│       ├── raw/
│       └── editados/
├── _PROCESADOS_SKOOL/          ← listos para subir a Skool
└── _SCRIPTS_PROCESAMIENTO/     ← scripts y este archivo
```

**Total estimado:** ~115 videos (11 ICAs × Principiante + Intermedio + Introducción)

---

## Lo que hace el script automáticamente

1. Elimina GPS y metadatos del Samsung (privacidad)
2. Corta silencios largos (>0.8 seg)
3. Transcribe y genera subtítulos .SRT con Whisper (GPU Metal M1)
4. Corta palabras de relleno (ums, eehs)
5. Corrección de color y brillo
6. Añade intro y outro GZBR (si existen en `assets/`)
7. Exporta H.264 1080p optimizado para Skool

**Costo:** $0 — todo corre local en tu Mac, sin internet

---

## Si se vuelve a congelar la máquina

Dile a Claude Code (por WhatsApp/OpenClaw):

> "Retomar pipeline de videos GZBR"

Tiene todo guardado en memoria y arranca sin preguntar nada.

---

*Generado por Claude Code · 2026-04-06*
