# GZBR Tutorials

Pipeline completo de tutoriales de GuitarZerotoBandRock.
Rutas relativas a: `/Volumes/Disk JLV/GuitarZerotoBandRock/gzbr-tutorials/`

## Estructura

```
00-CURRICULUM/        Plan maestro del curso (niveles, módulos, lecciones)
01-SCRIPTS/           Guiones por nivel
  nivel-01-principiante/
  nivel-02-intermedio/
  nivel-03-avanzado/
02-VIDEOS-RAW/        Grabaciones en bruto (antes de editar)
03-VIDEOS-EDITED/     Videos finales listos para publicar
04-ASSETS/
  thumbnails/         Miniaturas (.png / .jpg)
  tabs-pdf/           Tablaturas en PDF
  audio-backing/      Bases / backing tracks
  overlays/           Gráficos, lower-thirds, intro/outro
05-METADATA/          Títulos, descripciones, tags, SEO (JSON/MD por lección)
06-PUBLISHED/
  skool/              Ya subidos a Skool
  youtube/            Ya subidos a YouTube
_TEMPLATES/           Plantillas reutilizables (script, metadata, etc.)
_ARCHIVE/             Material descartado o versiones viejas
```

## Flujo de trabajo

1. **Plan** → `00-CURRICULUM/`
2. **Guión** → `01-SCRIPTS/nivel-XX/LECCION-NN.md`
3. **Grabar** → `02-VIDEOS-RAW/LECCION-NN.mp4`
4. **Editar** → `03-VIDEOS-EDITED/LECCION-NN-final.mp4`
5. **Metadata** → `05-METADATA/LECCION-NN.json`
6. **Publicar** → mover a `06-PUBLISHED/skool/` o `06-PUBLISHED/youtube/`

## Convención de nombres

- Lecciones: `L{NN}-{slug-corto}` (ej. `L01-primer-acorde`)
- Videos finales: `{nivel}-L{NN}-final.mp4`
- Thumbs: `{nivel}-L{NN}.png`

## Lanzamiento

Meta GZBR V8.3: **31 mayo 2026**
