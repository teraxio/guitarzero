#!/bin/bash
# ============================================================
# GZBR — Instalador de Dependencias para Pipeline de Video
# MacBook Air Apple M1 — 2026-04-06
# ============================================================

echo "============================================"
echo "  GZBR Video Pipeline — Instalando todo"
echo "============================================"

# 1. Homebrew (si no está)
if ! command -v brew &> /dev/null; then
    echo "[1/6] Instalando Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
else
    echo "[1/6] Homebrew: ya instalado ✓"
fi

# 2. FFmpeg con soporte completo
echo "[2/6] Instalando FFmpeg (Apple Silicon nativo)..."
brew install ffmpeg
echo "FFmpeg: $(ffmpeg -version 2>&1 | head -1) ✓"

# 3. pip actualizado
echo "[3/6] Actualizando pip..."
python3 -m pip install --upgrade pip --quiet

# 4. Whisper (mlx-whisper = el más rápido en M1, usa GPU Metal)
echo "[4/6] Instalando mlx-whisper (GPU Metal para M1)..."
pip3 install mlx-whisper --quiet
# Fallback a openai-whisper si falla
pip3 install openai-whisper --quiet
echo "Whisper: OK ✓"

# 5. Librerías Python para el pipeline
echo "[5/6] Instalando librerías Python..."
pip3 install \
    ffmpeg-python \
    webrtcvad \
    numpy \
    tqdm \
    colorama \
    --quiet
echo "Librerías Python: OK ✓"

# 6. Verificar todo
echo ""
echo "[6/6] Verificando instalación..."
echo -n "  FFmpeg: "; ffmpeg -version 2>&1 | grep "ffmpeg version" | head -1
echo -n "  Python: "; python3 --version
echo -n "  ffmpeg-python: "; python3 -c "import ffmpeg; print('OK')" 2>/dev/null || echo "FALLO"
echo -n "  whisper: "; python3 -c "import whisper; print('OK')" 2>/dev/null || echo "FALLO (instalar manualmente)"
echo -n "  webrtcvad: "; python3 -c "import webrtcvad; print('OK')" 2>/dev/null || echo "FALLO"
echo -n "  numpy: "; python3 -c "import numpy; print('OK')" 2>/dev/null || echo "FALLO"

echo ""
echo "============================================"
echo "  Instalación completa. Ejecuta:"
echo "  python3 procesar_videos.py --ayuda"
echo "============================================"
