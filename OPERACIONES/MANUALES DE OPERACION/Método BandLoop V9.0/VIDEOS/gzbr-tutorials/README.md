# 🎬 GZBR Tutorials - Remotion

Proyecto de video tutoriales para GZBR usando Remotion.

## 📦 Instalación

```bash
cd gzbr-tutorials
npm install
```

## 🚀 Comandos Principales

### 1. Modo Desarrollo (Remotion Studio)
```bash
npm start
```
- Abre interfaz visual en el navegador
- Preview en tiempo real
- Ajusta duración, fps, resolución
- Export directo desde UI

### 2. Render Local (CLI)

**Wonderwall Intro:**
```bash
npx remotion render src/index.ts WonderwallIntro out/wonderwall.mp4
```

**Seven Nation Army:**
```bash
npx remotion render src/index.ts SevenNationArmy out/seven-nation.mp4
```

**Ambos videos:**
```bash
npx remotion render src/index.ts WonderwallIntro out/wonderwall.mp4 && \
npx remotion render src/index.ts SevenNationArmy out/seven-nation.mp4
```

### 3. Ver Compositions Disponibles
```bash
npx remotion compositions src/index.ts
```

## 📁 Estructura del Proyecto

```
gzbr-tutorials/
├── src/
│   ├── compositions/          # Videos completos
│   │   ├── WonderwallIntro.tsx    # Ejercicio 1: Em7-G
│   │   └── SevenNationArmy.tsx    # Ejercicio 2: Riff bajo
│   ├── components/            # Componentes reutilizables
│   │   ├── GZBRBranding.tsx       # Intro/outro GZBR
│   │   ├── TabViewer.tsx          # Tabs animadas
│   │   └── ChordCircle.tsx        # Círculos de acordes
│   ├── assets/
│   │   ├── audio/                 # Backing tracks (añadir)
│   │   └── fonts/                 # DM Serif Display (añadir)
│   ├── Root.tsx                   # Registro de compositions
│   └── index.ts                   # Punto de entrada
├── out/                       # Videos renderizados
├── public/                    # Assets estáticos
└── package.json
```

## 🎨 Ejercicios Incluidos

### ✅ Ejercicio 1: Wonderwall - Intro
- **Duración:** 15 segundos
- **Acordes:** Em7 → G
- **Features:**
  - Intro GZBR branded (3s)
  - Círculos de acordes con glow
  - Tabs sincronizadas
  - Progress bar
  - Outro con CTA

### ✅ Ejercicio 2: Seven Nation Army - Riff
- **Duración:** 20 segundos
- **Instrumento:** Bajo (4 cuerdas)
- **Features:**
  - Fondo pulsante con intensidad
  - Notación de notas (E-E-G-E-D-C-B)
  - Tabs con velocity visual
  - Tempo indicator (120 BPM)
  - Outro GZBR

## 🎯 Personalización Rápida

### Cambiar colores GZBR:
Edita `src/components/GZBRBranding.tsx`:
```tsx
background: 'linear-gradient(135deg, #00d4ff 0%, #ff00ff 100%)'
```

### Agregar nuevo tutorial:
1. Crea `src/compositions/NuevoTutorial.tsx`
2. Copia estructura de WonderwallIntro.tsx
3. Modifica tabs y acordes
4. Registra en `src/Root.tsx`:
```tsx
<Composition
  id="NuevoTutorial"
  component={NuevoTutorial}
  durationInFrames={300}
  fps={30}
  width={1920}
  height={1080}
/>
```

### Agregar audio:
```tsx
import {Audio} from 'remotion';

<Audio src="/assets/audio/backing-track.mp3" />
```

## 📊 Configuración de Render

### Calidad Alta (producción):
```bash
npx remotion render src/index.ts WonderwallIntro out/wonderwall.mp4 \
  --codec h264 \
  --crf 18 \
  --pixel-format yuv420p
```

### Preview Rápido (draft):
```bash
npx remotion render src/index.ts WonderwallIntro out/preview.mp4 \
  --scale 0.5 \
  --crf 28
```

## 🔧 Tips Útiles

### Verificar duración de video:
```bash
ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 out/wonderwall.mp4
```

### Convertir para Instagram/TikTok (9:16):
Modifica composition:
```tsx
width={1080}
height={1920}
```

### Debug frame específico:
En Remotion Studio → Input frame number → Play

## 📱 Próximos Pasos

1. **Agregar audio:** Backing tracks en `/assets/audio`
2. **Fuentes custom:** DM Serif Display en `/assets/fonts`
3. **Más tutoriales:** Crear compositions para cada canción GZBR
4. **Templates:** Abstraer componentes para reutilización
5. **Cloud render:** Cuando escales a producción masiva

## 🆘 Troubleshooting

**Error: Module not found**
```bash
npm install
```

**Render muy lento**
- Reduce resolución: `width={1280} height={720}`
- Baja fps: `fps={24}`
- Usa preview mode: `--scale 0.5`

**Video sin audio**
- Verifica que Audio component tenga src correcto
- Formatos soportados: mp3, wav, aac

## 📚 Recursos

- [Remotion Docs](https://www.remotion.dev/docs)
- [API Reference](https://www.remotion.dev/docs/api)
- [Examples](https://www.remotion.dev/showcase)

---

**Made with 💙💜 for GZBR - GuitarZero to BandRock**
