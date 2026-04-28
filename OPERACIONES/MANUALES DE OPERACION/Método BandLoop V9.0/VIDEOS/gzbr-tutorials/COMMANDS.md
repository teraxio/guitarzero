# ⚡ GZBR Remotion - Quick Commands

## 🎬 Workflow Básico

### 1. Desarrollo
```bash
npm start
# → Abre http://localhost:3000
# → Preview interactivo en navegador
```

### 2. Render Individual
```bash
# Wonderwall
npx remotion render src/index.ts WonderwallIntro out/wonderwall.mp4

# Seven Nation Army
npx remotion render src/index.ts SevenNationArmy out/seven-nation.mp4
```

### 3. Render Batch (ambos videos)
```bash
npx remotion render src/index.ts WonderwallIntro out/wonderwall.mp4 && \
npx remotion render src/index.ts SevenNationArmy out/seven-nation.mp4
```

## 📊 Calidades de Render

### Alta (YouTube/producción)
```bash
npx remotion render src/index.ts WonderwallIntro out/hq.mp4 \
  --codec h264 --crf 18 --pixel-format yuv420p
```

### Media (Instagram/Facebook)
```bash
npx remotion render src/index.ts WonderwallIntro out/med.mp4 \
  --codec h264 --crf 23
```

### Preview (draft rápido)
```bash
npx remotion render src/index.ts WonderwallIntro out/draft.mp4 \
  --scale 0.5 --crf 28
```

## 🔧 Utilities

### Ver compositions disponibles
```bash
npx remotion compositions src/index.ts
```

### Info de video renderizado
```bash
ffprobe -v error -show_entries format=duration,size,bit_rate \
  -show_entries stream=width,height,codec_name \
  out/wonderwall.mp4
```

### Thumbnail de frame específico
```bash
npx remotion still src/index.ts WonderwallIntro out/thumb.png --frame=90
```

## 📱 Formatos

### Instagram/TikTok (9:16)
Modifica composition → `width={1080} height={1920}`

### YouTube (16:9) - Default
`width={1920} height={1080}`

### Square (1:1)
`width={1080} height={1080}`

## 🎨 Templates Rápidos

### Nuevo tutorial de guitarra
```bash
cp src/compositions/WonderwallIntro.tsx src/compositions/NewSong.tsx
# Editar NewSong.tsx
# Agregar a Root.tsx
```

### Nuevo tutorial de bajo
```bash
cp src/compositions/SevenNationArmy.tsx src/compositions/NewBass.tsx
# Editar NewBass.tsx
# Agregar a Root.tsx
```

## 🚀 Actualizar Remotion
```bash
npx remotion upgrade
```

## 📦 Reinstalar dependencias
```bash
rm -rf node_modules package-lock.json
npm install
```

---

💡 **Tip:** Usa `npm start` durante desarrollo para preview instantáneo
🎯 **Tip:** Render con `--scale 0.5` para testear rápido antes de HQ
⚡ **Tip:** Usa CRF 18-23 para balance calidad/tamaño
