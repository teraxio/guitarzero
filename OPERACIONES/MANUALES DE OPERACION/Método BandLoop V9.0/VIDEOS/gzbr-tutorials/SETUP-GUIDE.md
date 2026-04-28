# 🎯 GZBR Remotion - Setup Completo

## ✅ Lo Que Tienes Ahora

### Proyecto Base Configurado
```
✅ gzbr-tutorials/
   ✅ package.json con dependencias Remotion
   ✅ tsconfig.json (TypeScript configurado)
   ✅ remotion.config.ts
   ✅ Estructura de carpetas completa
```

### Componentes GZBR Listos
```
✅ GZBRBranding.tsx      → Intro/outro con gradiente cyan→magenta
✅ TabViewer.tsx         → Tabs animadas con glow
✅ ChordCircle.tsx       → Círculos de acordes iluminados
```

### 2 Ejercicios Prácticos Completos
```
✅ WonderwallIntro.tsx   → 15s | Em7-G | Guitarra
✅ SevenNationArmy.tsx   → 20s | Riff | Bajo
```

### Documentación
```
✅ README.md             → Guía completa
✅ COMMANDS.md           → Quick reference
✅ .gitignore            → Configurado para Remotion
```

---

## 🚀 Siguiente: Instalación en Tu Mac

### PASO 1: Copiar Proyecto
```bash
# Si estás en Claude Code, el proyecto ya está en /home/claude/gzbr-tutorials
# Cópialo a tu Mac:
cp -r /home/claude/gzbr-tutorials ~/Desktop/
cd ~/Desktop/gzbr-tutorials
```

### PASO 2: Instalar Dependencias
```bash
npm install
```
**Tiempo estimado:** 2-3 minutos
**Peso total:** ~300MB (node_modules)

### PASO 3: Verificar Instalación
```bash
npx remotion --version
# Debería mostrar: 4.x.x
```

### PASO 4: Abrir Remotion Studio
```bash
npm start
```
**Se abrirá:** http://localhost:3000
**Verás:** 2 compositions listas para preview

---

## 🎬 Primeros Ejercicios (Práctica)

### Ejercicio 1: Preview en Studio
1. `npm start`
2. Selecciona "WonderwallIntro"
3. Click ▶️ Play
4. Ajusta timeline, observa:
   - Intro GZBR (0-3s)
   - Círculos Em7/G iluminándose
   - Tabs sincronizadas
   - Progress bar
   - Outro (12-15s)

### Ejercicio 2: Primer Render
```bash
npx remotion render src/index.ts WonderwallIntro out/mi-primer-video.mp4
```
**Resultado:** `out/mi-primer-video.mp4` (1920x1080, ~2MB)
**Tiempo:** 30-60 segundos (depende de tu Mac)

**Abre el video y verifica:**
- ✅ Calidad 1080p
- ✅ Gradientes suaves
- ✅ Animaciones fluidas
- ✅ Audio (si agregaste backing track)

---

## 🎨 Personalización Básica

### Cambiar Texto del Intro
Edita `src/components/GZBRBranding.tsx`:
```tsx
// Línea 31
<div>{text}</div>
// Cambia a:
<div>Tutorial por José Luis</div>
```

### Cambiar Acordes de Wonderwall
Edita `src/compositions/WonderwallIntro.tsx`:
```tsx
// Línea 67-76: Reemplaza Em7/G por otros acordes
<ChordCircle chord="Cmaj7" ... />
<ChordCircle chord="D" ... />
```

### Cambiar Colores GZBR
Busca en cualquier archivo:
```tsx
background: 'linear-gradient(135deg, #00d4ff, #ff00ff)'
// Cambia a tus colores preferidos
```

---

## 📊 Escalando a Producción

### Cuando Domines los Ejercicios:

1. **Agregar Audio**
   - Pon backing tracks en `/assets/audio`
   - Importa: `<Audio src="/assets/audio/wonderwall.mp3" />`

2. **Más Tutoriales**
   - Copia template de WonderwallIntro.tsx
   - Modifica tabs/acordes
   - Registra en Root.tsx

3. **Optimizar Workflow**
   - Crea script para batch render:
     ```bash
     for song in Wonderwall SevenNationArmy NewSong; do
       npx remotion render src/index.ts $song out/$song.mp4
     done
     ```

4. **Cloud Render (Producción Masiva)**
   - Cuando tengas 20+ videos
   - Setup AWS Lambda
   - Docs: https://www.remotion.dev/docs/lambda

---

## 🆘 Troubleshooting Común

### "npm install" falla
```bash
# Actualizar npm
npm install -g npm@latest

# Limpiar cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Remotion Studio no abre
```bash
# Verificar puerto 3000 libre
lsof -ti:3000 | xargs kill -9

# Reintentar
npm start
```

### Render muy lento
```bash
# Draft mode (más rápido)
npx remotion render src/index.ts WonderwallIntro out/draft.mp4 --scale 0.5
```

### Video sale negro
- Verifica que composition ID coincida exactamente
- Revisa console en Remotion Studio para errores

---

## 📚 Recursos de Aprendizaje

### Remotion Docs (esenciales)
1. **Getting Started:** https://www.remotion.dev/docs
2. **API Reference:** https://www.remotion.dev/docs/api
3. **Animations:** https://www.remotion.dev/docs/animating
4. **Audio:** https://www.remotion.dev/docs/using-audio

### Templates de Inspiración
- https://www.remotion.dev/showcase
- Busca "music tutorial" en showcase

### Comunidad
- Discord: https://remotion.dev/discord
- GitHub Discussions: https://github.com/remotion-dev/remotion/discussions

---

## ✅ Checklist de Setup

Marca cuando completes:

- [ ] `npm install` exitoso
- [ ] `npm start` abre Remotion Studio
- [ ] Puedes ver preview de WonderwallIntro
- [ ] Puedes ver preview de SevenNationArmy
- [ ] Render exitoso de un video
- [ ] Video abre en VLC/QuickTime
- [ ] Entiendes cómo editar tabs
- [ ] Entiendes cómo cambiar acordes
- [ ] Leíste README.md completo
- [ ] Leíste COMMANDS.md

---

## 🎯 Meta: 2 Semanas

**Semana 1: Familiarización**
- Día 1-2: Setup + ejercicios básicos
- Día 3-4: Editar ejercicios existentes
- Día 5-7: Crear 2 tutoriales nuevos

**Semana 2: Producción**
- Día 8-10: 5 tutoriales completos
- Día 11-12: Agregar audio + efectos
- Día 13-14: Batch render + optimización

**Resultado esperado:** 10+ videos tutoriales GZBR listos para Skool/social media

---

## 💡 Consejo Final

**Empieza simple:**
1. No te compliques con audio todavía
2. Practica editando los ejercicios existentes
3. Cuando te sientas cómodo → agrega nuevas canciones
4. Cuando tengas 5+ videos → optimiza workflow

**Remotion es código = control total**
- Cada animación es programable
- Cada elemento es reutilizable
- Escala a 100+ videos sin esfuerzo extra

**¡Estás listo para crear contenido GZBR de clase mundial!** 🎸🎹🎤

---

**Made with 💙💜 for GZBR**
**Setup by Claude - April 2026**
