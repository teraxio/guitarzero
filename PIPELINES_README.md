# GZBR Sistema Operativo — 3 Pipelines

Creado: 30 Abr 2026 | Alineado con Plan de Negocios V9.1

---

## Arquitectura

```
Pipeline_Fundraising/   → Efectivo para infraestructura USA
Pipeline_Produccion/    → Contenido Skool (videos, subtítulos, thumbnails)
Pipeline_LLC/           → Celular, línea, cuenta, LLC Delaware
```

Cadena causal: **Fundraising → Efectivo → Infraestructura → LLC → Lanzamiento 1 Jul 2026**

---

## Pipeline 1: Fundraising

**Objetivo:** $1,140 USD vía 3 eventos split de barra en Mayo 2026

### Estructura
```
Pipeline_Fundraising/
  eventos/          ← Info por evento (fecha, bar, resultado)
  _finanzas/        ← registro.txt (una línea por ingreso: monto fecha concepto)
```

### Comandos
```bash
# Registrar ingreso de evento
echo "350 2026-05-10 evento1_bar_nombre" >> Pipeline_Fundraising/_finanzas/registro.txt

# Ver total recaudado
awk '{sum+=$1} END{print "$"sum" de $1140"}' Pipeline_Fundraising/_finanzas/registro.txt
```

### Plan B (decisión al 1 Jul)
- **$700+**: Proceder con Stripe Atlas LLC
- **$400-700**: Soft launch persona física MX (Plan B1 del V9.1)
- **<$400**: Posponer lanzamiento (Plan B2 del V9.1)

---

## Pipeline 2: Producción

**Objetivo:** Stockpile de 10+ videos publicables para 1 Jul

### Estructura
```
Pipeline_Produccion/
  00_grabaciones_crudas/    ← ICA sube video original aquí
  01_procesados/            ← (reservado para procesamiento intermedio)
  02_listos_aprobacion/     ← Script genera carpeta con video+srt+thumb+json
  03_aprobados_skool/       ← JLV mueve manualmente tras aprobar
  04_publicados/            ← Publicados en Skool
  _logs/                    ← pipeline.log + daily briefs
  procesar_video.sh         ← Script principal
  reporte_diario.sh         ← Genera Daily Brief 7am
```

### Comandos
```bash
# Procesar un video nuevo
./Pipeline_Produccion/procesar_video.sh /path/to/video.mp4

# Ver log de procesamiento
tail -50 Pipeline_Produccion/_logs/pipeline.log

# Aprobar un video (mover manualmente)
mv Pipeline_Produccion/02_listos_aprobacion/20260501_nombre/ Pipeline_Produccion/03_aprobados_skool/

# Ejecutar reporte diario manual
./Pipeline_Produccion/reporte_diario.sh
```

### Dependencias del script procesar_video.sh
- `ffmpeg` / `ffprobe` — extracción metadata + thumbnail
- `whisper` (OpenAI) — subtítulos ES + EN
- Instalar: `pip install openai-whisper` y `brew install ffmpeg`

### Remotion (render final)
```bash
# Render horizontal (Skool)
cd ~/gzbr-tutorials && npx remotion render GZBRTemplate output.mp4

# Render vertical (Reels/TikTok)
cd ~/gzbr-tutorials && npx remotion render GZBRTemplate-Vertical output_vertical.mp4
```

---

## Pipeline 3: LLC / Infraestructura USA

**Objetivo:** LLC Delaware operativa con Stripe Billing antes del 1 Jul

### Estructura
```
Pipeline_LLC/
  01_efectivo/        ← Comprobantes de efectivo consolidado
  02_celular_linea/   ← Recibos celular + activación línea USA
  03_cuenta_USA/      ← Mercury Bank docs
  04_LLC_delaware/    ← Stripe Atlas docs, EIN, artículos
```

### Secuencia (no paralelizable)
1. Consolidar efectivo (fin Mayo)
2. Comprar celular usado + línea USA prepagada (Jun S1)
3. Aplicar Stripe Atlas con número USA (Jun S2)
4. Recibir EIN + abrir Mercury Bank (Jun S3)
5. Configurar Stripe Billing + Skool (Jun S4)

---

## Reporte Diario Automático

- **Cuándo:** 7:00 AM diario (launchd)
- **Qué hace:** Lee métricas de los 3 pipelines, genera brief
- **Dónde:** Notion Daily Brief + archivo local en _logs/

### Troubleshooting launchd
```bash
# Ver si está cargado
launchctl list | grep gzbr

# Recargar
launchctl unload ~/Library/LaunchAgents/com.gzbr.dailybrief.plist
launchctl load ~/Library/LaunchAgents/com.gzbr.dailybrief.plist

# Ver errores
cat /tmp/gzbr_dailybrief_err.log
```

---

## Notion Pages

| Página | ID |
|---|---|
| ARRANQUE (parent) | 352e54e2-80a7-81ec-82b1-f877a92ba7f3 |
| Fundraising Eventos | 353e54e2-80a7-816a-80a9-fa7d202d54b4 |
| Infraestructura USA | 353e54e2-80a7-81be-93ba-eabd6a4e012f |
| Producción Cola | 353e54e2-80a7-8131-897f-e0fbcf6caacb |
| Daily Brief JLV | 353e54e2-80a7-8198-8f50-e32a2824c774 |
| Caja Negra | 352e54e2-80a7-8197-8bfe-ee22d607019c |
| Hub V9.1 | 34de54e2-80a7-8106-8c7a-f3f7194f4a60 |

---

## Documentos V9.1 fuente
- GuitarZero_Plan_Negocios_V9_1 — Plan maestro
- GuitarZero_Modelo_Legal_Transicion_LLC_V9_1 — Plan B legal
- GZBR_Biblia_Produccion_Visual_V9_1 — Estándares visuales
- Protocolo-Grabacion-Clase-V9.1 — Cómo graban los ICAs
- GZBR_Estrategia_WhatsApp_Impulso_V9_1 — Conversión WA
- GZBR_Guerrilla_TJ_Bares_V9_1 — Estrategia eventos
