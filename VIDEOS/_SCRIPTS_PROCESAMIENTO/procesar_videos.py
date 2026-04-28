#!/usr/bin/env python3
"""
================================================================
GZBR — Pipeline Automático de Procesamiento de Videos
================================================================
MacBook Air Apple M1 | 100% Local | Sin APIs externas

Hace automáticamente:
  1. Strip metadatos GPS (privacidad / redes sociales USA)
  2. Eliminación de silencios (VAD)
  3. Detección y corte de palabras de relleno (ums, eeeh, etc.)
  4. Corrección de color/brillo
  5. Transcripción + subtítulos SRT (Whisper local M1)
  6. Concat intro y outro GZBR
  7. Export optimizado para Skool (H.264 1080p)

Uso:
  python3 procesar_videos.py --ica ICA-03 --nivel PRINCIPIANTE
  python3 procesar_videos.py --todos
  python3 procesar_videos.py --archivo video.mp4
================================================================
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

# ─── Colores para terminal ───────────────────────────────────
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    OK   = Fore.GREEN  + "  ✓ " + Style.RESET_ALL
    ERR  = Fore.RED    + "  ✗ " + Style.RESET_ALL
    INFO = Fore.CYAN   + "  → " + Style.RESET_ALL
    WARN = Fore.YELLOW + "  ⚠ " + Style.RESET_ALL
except ImportError:
    OK = ERR = INFO = WARN = "  "

# ─── Rutas base ──────────────────────────────────────────────
DISK_BASE   = Path("/Volumes/Disk JLV/GuitarZerotoBandRock/VIDEOS")
SCRIPTS_DIR = DISK_BASE / "_SCRIPTS_PROCESAMIENTO"
SKOOL_DIR   = DISK_BASE / "_PROCESADOS_SKOOL"
INTRO_FILE  = SCRIPTS_DIR / "assets" / "intro_gzbr.mp4"
OUTRO_FILE  = SCRIPTS_DIR / "assets" / "outro_gzbr.mp4"

# ─── Palabras de relleno en español ──────────────────────────
FILLER_WORDS = {
    "es": ["eeh", "ehh", "mmm", "ummm", "este", "o sea", "o sea que",
           "bueno", "pues", "entonces", "verdad", "no", "digamos",
           "básicamente", "literalmente", "tipo que", "o algo así"],
    "en": ["um", "uh", "like", "you know", "basically", "literally",
           "kind of", "sort of", "right", "okay so"]
}

# ─── Configuración de exportación para Skool ─────────────────
SKOOL_CONFIG = {
    "video_codec":   "libx264",
    "audio_codec":   "aac",
    "video_bitrate": "4000k",
    "audio_bitrate": "192k",
    "resolution":    "1920:1080",   # 1080p máximo
    "fps":           "30",
    "preset":        "slow",        # mejor compresión en M1
    "crf":           "22",          # calidad (18=alta, 28=baja)
    "audio_sample":  "44100",
    "pixel_fmt":     "yuv420p",     # compatible con todos los browsers
}


# ================================================================
# UTILIDADES
# ================================================================

def run(cmd: list, capture=False) -> subprocess.CompletedProcess:
    """Ejecuta un comando de sistema."""
    result = subprocess.run(
        cmd,
        capture_output=capture,
        text=True
    )
    return result


def check_ffmpeg() -> bool:
    """Verifica que FFmpeg esté instalado."""
    result = run(["ffmpeg", "-version"], capture=True)
    return result.returncode == 0


def check_whisper() -> str:
    """Retorna qué versión de whisper está disponible."""
    try:
        import mlx_whisper
        return "mlx"
    except ImportError:
        pass
    try:
        import whisper
        return "openai"
    except ImportError:
        pass
    return "none"


def get_video_duration(video_path: Path) -> float:
    """Obtiene duración del video en segundos."""
    result = run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path)
    ], capture=True)
    try:
        return float(result.stdout.strip())
    except:
        return 0.0


def format_time(seconds: float) -> str:
    """Formatea segundos como HH:MM:SS,mmm para SRT."""
    ms  = int((seconds % 1) * 1000)
    s   = int(seconds) % 60
    m   = int(seconds) // 60 % 60
    h   = int(seconds) // 3600
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def log(msg: str, level: str = "info"):
    prefix = {"ok": OK, "err": ERR, "info": INFO, "warn": WARN}.get(level, INFO)
    print(f"{prefix}{msg}")


# ================================================================
# PASO 1 — STRIP METADATOS GPS
# ================================================================

def strip_metadata(input_path: Path, output_path: Path) -> bool:
    """
    Elimina todos los metadatos del video (GPS, device, location).
    Crítico para publicar en redes sociales USA sin revelar origen MX.
    """
    log(f"Eliminando metadatos GPS...", "info")
    result = run([
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-map_metadata", "-1",      # elimina TODOS los metadatos
        "-c:v", "copy",             # copia video sin re-encode (rápido)
        "-c:a", "copy",             # copia audio sin re-encode
        str(output_path)
    ], capture=True)
    if result.returncode == 0:
        log(f"Metadatos eliminados", "ok")
        return True
    else:
        log(f"Error strip metadata: {result.stderr[-200:]}", "err")
        return False


# ================================================================
# PASO 2 — ELIMINACIÓN DE SILENCIOS (VAD)
# ================================================================

def remove_silence(input_path: Path, output_path: Path,
                   silence_thresh_db: int = -40,
                   min_silence_sec: float = 0.8,
                   keep_padding_sec: float = 0.15) -> bool:
    """
    Elimina silencios del video usando filtro FFmpeg silenceremove.
    - silence_thresh_db: umbral de silencio en dB (-40 = moderado)
    - min_silence_sec:   duración mínima de silencio a eliminar (0.8s)
    - keep_padding_sec:  margen que deja antes/después de cada corte
    """
    log(f"Eliminando silencios (umbral {silence_thresh_db}dB, mín {min_silence_sec}s)...", "info")

    # Filtro silenceremove de FFmpeg — muy preciso en M1
    silence_filter = (
        f"silenceremove="
        f"start_periods=1:"
        f"start_duration=0.1:"
        f"start_threshold={silence_thresh_db}dB:"
        f"stop_periods=-1:"
        f"stop_duration={min_silence_sec}:"
        f"stop_threshold={silence_thresh_db}dB:"
        f"detection=peak"
    )

    result = run([
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-af", silence_filter,
        "-c:v", "copy",
        str(output_path)
    ], capture=True)

    if result.returncode == 0:
        orig_dur = get_video_duration(input_path)
        new_dur  = get_video_duration(output_path)
        saved    = orig_dur - new_dur
        log(f"Silencios eliminados — ahorró {saved:.1f}s ({orig_dur:.1f}s → {new_dur:.1f}s)", "ok")
        return True
    else:
        log(f"Error silence removal: {result.stderr[-200:]}", "err")
        # Si falla, continua con el archivo original
        shutil.copy(input_path, output_path)
        return False


# ================================================================
# PASO 3 — TRANSCRIPCIÓN + SUBTÍTULOS (Whisper local M1)
# ================================================================

def transcribe_and_subtitle(input_path: Path, output_srt: Path,
                             language: str = "es") -> list:
    """
    Transcribe el video con Whisper (corre en GPU Metal del M1).
    Retorna lista de segmentos con timestamps.
    Genera archivo SRT de subtítulos.
    """
    log(f"Transcribiendo con Whisper (GPU M1, idioma: {language})...", "info")

    whisper_type = check_whisper()

    if whisper_type == "none":
        log("Whisper no instalado — saltando subtítulos", "warn")
        return []

    segments = []

    try:
        if whisper_type == "mlx":
            import mlx_whisper
            result = mlx_whisper.transcribe(
                str(input_path),
                path_or_hf_repo="mlx-community/whisper-large-v3-mlx",
                language=language,
                word_timestamps=True,
            )
        else:
            import whisper
            model = whisper.load_model("large-v3")  # el más preciso
            result = model.transcribe(
                str(input_path),
                language=language,
                word_timestamps=True,
                verbose=False
            )

        segments = result.get("segments", [])

        # Generar SRT
        srt_content = ""
        for i, seg in enumerate(segments, 1):
            start = format_time(seg["start"])
            end   = format_time(seg["end"])
            text  = seg["text"].strip()
            srt_content += f"{i}\n{start} --> {end}\n{text}\n\n"

        output_srt.write_text(srt_content, encoding="utf-8")
        log(f"Subtítulos generados: {len(segments)} segmentos → {output_srt.name}", "ok")

    except Exception as e:
        log(f"Error Whisper: {e}", "err")

    return segments


# ================================================================
# PASO 4 — CORTE DE PALABRAS DE RELLENO
# ================================================================

def remove_filler_words(input_path: Path, output_path: Path,
                        segments: list, language: str = "es") -> bool:
    """
    Usa los timestamps de Whisper para identificar y cortar
    palabras de relleno del video.
    """
    if not segments:
        log("Sin segmentos Whisper — saltando filler removal", "warn")
        shutil.copy(input_path, output_path)
        return False

    log("Detectando palabras de relleno...", "info")

    fillers   = FILLER_WORDS.get(language, []) + FILLER_WORDS.get("es", [])
    cuts      = []  # lista de (start, end) a eliminar
    filler_count = 0

    for seg in segments:
        words = seg.get("words", [])
        for w in words:
            word_text = w.get("word", "").strip().lower()
            # Detecta palabras de relleno (solo si son cortas y aisladas)
            if any(filler in word_text for filler in fillers):
                # Solo corta si el segmento de relleno es < 2 segundos
                duration = w.get("end", 0) - w.get("start", 0)
                if 0 < duration < 2.0:
                    cuts.append((w["start"], w["end"]))
                    filler_count += 1

    if not cuts:
        log("No se encontraron palabras de relleno", "ok")
        shutil.copy(input_path, output_path)
        return True

    log(f"Cortando {filler_count} palabras de relleno...", "info")

    # Construye lista de segmentos a CONSERVAR (inverso de los cortes)
    total_dur   = get_video_duration(input_path)
    keep_segs   = []
    last_end    = 0.0

    # Combina cortes muy cercanos (< 0.1s entre ellos)
    merged = []
    for start, end in sorted(cuts):
        if merged and start - merged[-1][1] < 0.1:
            merged[-1] = (merged[-1][0], end)
        else:
            merged.append([start, end])

    for cut_start, cut_end in merged:
        if last_end < cut_start:
            keep_segs.append((last_end, cut_start))
        last_end = cut_end

    if last_end < total_dur:
        keep_segs.append((last_end, total_dur))

    if not keep_segs:
        shutil.copy(input_path, output_path)
        return False

    # Crea lista de archivos temporales para concat
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path  = Path(tmpdir)
        clip_list = tmp_path / "clips.txt"
        clip_files = []

        for idx, (seg_start, seg_end) in enumerate(keep_segs):
            duration = seg_end - seg_start
            if duration < 0.05:
                continue
            clip_out = tmp_path / f"clip_{idx:04d}.mp4"
            run([
                "ffmpeg", "-y",
                "-ss", str(seg_start),
                "-to", str(seg_end),
                "-i", str(input_path),
                "-c", "copy",
                str(clip_out)
            ], capture=True)
            if clip_out.exists():
                clip_files.append(clip_out)

        if not clip_files:
            shutil.copy(input_path, output_path)
            return False

        # Escribe archivo de concatenación
        with open(clip_list, "w") as f:
            for cf in clip_files:
                f.write(f"file '{cf}'\n")

        result = run([
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(clip_list),
            "-c", "copy",
            str(output_path)
        ], capture=True)

    if result.returncode == 0:
        log(f"Filler words eliminadas: {filler_count} cortes", "ok")
        return True
    else:
        log(f"Error filler removal — conservando original", "warn")
        shutil.copy(input_path, output_path)
        return False


# ================================================================
# PASO 5 — CORRECCIÓN DE COLOR Y BRILLO
# ================================================================

def color_correction(input_path: Path, output_path: Path) -> bool:
    """
    Aplica corrección automática de color para mejorar calidad visual.
    Optimizado para videos grabados con Samsung en interiores.
    """
    log("Aplicando corrección de color...", "info")

    # Filtros: normalize (auto-levels) + vibrance + sharpness suave
    color_filter = (
        "normalize=blackpt=black:whitept=white:smoothing=0,"  # auto-levels
        "eq=brightness=0.02:saturation=1.1:contrast=1.05,"   # leve boost
        "unsharp=3:3:0.5:3:3:0.0"                            # sharpness suave
    )

    result = run([
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-vf", color_filter,
        "-c:a", "copy",
        "-c:v", SKOOL_CONFIG["video_codec"],
        "-crf", SKOOL_CONFIG["crf"],
        "-preset", SKOOL_CONFIG["preset"],
        str(output_path)
    ], capture=True)

    if result.returncode == 0:
        log("Corrección de color aplicada", "ok")
        return True
    else:
        log(f"Error color correction — conservando original", "warn")
        shutil.copy(input_path, output_path)
        return False


# ================================================================
# PASO 6 — CONCAT INTRO Y OUTRO
# ================================================================

def add_intro_outro(input_path: Path, output_path: Path) -> bool:
    """
    Añade intro y outro de GZBR al video.
    Si no existen los archivos de intro/outro, salta este paso.
    """
    has_intro = INTRO_FILE.exists()
    has_outro = OUTRO_FILE.exists()

    if not has_intro and not has_outro:
        log("Sin intro/outro — coloca archivos en assets/ para activar", "warn")
        shutil.copy(input_path, output_path)
        return False

    log(f"Añadiendo {'intro' if has_intro else ''}{'/' if has_intro and has_outro else ''}{'outro' if has_outro else ''}...", "info")

    with tempfile.TemporaryDirectory() as tmpdir:
        concat_file = Path(tmpdir) / "concat.txt"
        parts = []

        if has_intro:
            parts.append(str(INTRO_FILE))
        parts.append(str(input_path))
        if has_outro:
            parts.append(str(OUTRO_FILE))

        with open(concat_file, "w") as f:
            for p in parts:
                f.write(f"file '{p}'\n")

        result = run([
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c", "copy",
            str(output_path)
        ], capture=True)

    if result.returncode == 0:
        log("Intro/outro añadidos", "ok")
        return True
    else:
        log("Error concat intro/outro — conservando sin intro/outro", "warn")
        shutil.copy(input_path, output_path)
        return False


# ================================================================
# PASO 7 — EXPORT FINAL OPTIMIZADO PARA SKOOL
# ================================================================

def export_for_skool(input_path: Path, output_path: Path,
                     srt_path: Path = None) -> bool:
    """
    Exporta el video final con:
    - Codec H.264 (máxima compatibilidad Skool/browsers)
    - Audio AAC estéreo
    - Resolución máx 1080p (escala si es necesario)
    - Subtítulos como pista separada (no quemados)
    - Nombre limpio sin espacios
    """
    log(f"Exportando para Skool (H.264 1080p)...", "info")

    # Scale a 1080p máximo (si es más grande lo baja, si es menor lo deja)
    scale_filter = (
        f"scale='if(gt(iw,1920),1920,iw)':"
        f"'if(gt(ih,1080),1080,ih)':"
        f"force_original_aspect_ratio=decrease,"
        f"pad=ceil(iw/2)*2:ceil(ih/2)*2"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_path),
    ]

    # Añadir subtítulos como pista (no quemados = usuario puede desactivarlos)
    if srt_path and srt_path.exists():
        cmd += ["-i", str(srt_path)]
        cmd += [
            "-map", "0:v",
            "-map", "0:a",
            "-map", "1:s",
            "-c:s", "mov_text",    # subtítulos en formato MP4
            "-metadata:s:s:0", "language=spa",
        ]
    else:
        cmd += ["-map", "0:v", "-map", "0:a"]

    cmd += [
        "-c:v",        SKOOL_CONFIG["video_codec"],
        "-crf",        SKOOL_CONFIG["crf"],
        "-preset",     SKOOL_CONFIG["preset"],
        "-b:v",        SKOOL_CONFIG["video_bitrate"],
        "-c:a",        SKOOL_CONFIG["audio_codec"],
        "-b:a",        SKOOL_CONFIG["audio_bitrate"],
        "-ar",         SKOOL_CONFIG["audio_sample"],
        "-vf",         scale_filter,
        "-r",          SKOOL_CONFIG["fps"],
        "-pix_fmt",    SKOOL_CONFIG["pixel_fmt"],
        "-movflags",   "+faststart",   # streaming progresivo en web
        "-map_metadata", "-1",         # strip final de metadatos
        str(output_path)
    ]

    result = run(cmd, capture=True)

    if result.returncode == 0:
        size_mb = output_path.stat().st_size / (1024 * 1024)
        dur     = get_video_duration(output_path)
        log(f"Export completo → {output_path.name} ({size_mb:.1f} MB, {dur:.0f}s)", "ok")
        return True
    else:
        log(f"Error export: {result.stderr[-300:]}", "err")
        return False


# ================================================================
# PIPELINE PRINCIPAL
# ================================================================

def procesar_video(input_path: Path, output_dir: Path,
                   language: str = "es") -> dict:
    """
    Ejecuta el pipeline completo para un video.
    Retorna dict con resultado y tiempos.
    """
    nombre_base = input_path.stem
    # Nombre limpio: sin espacios, sin caracteres especiales
    nombre_limpio = nombre_base.replace(" ", "_").replace("(", "").replace(")", "")
    ts = datetime.now().strftime("%Y%m%d_%H%M")

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*55}")
    print(f"  Procesando: {input_path.name}")
    print(f"  Destino:    {output_dir}")
    print(f"{'='*55}")

    inicio = datetime.now()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # Archivos intermedios
        f_meta    = tmp / "01_meta.mp4"
        f_silence = tmp / "02_silence.mp4"
        f_filler  = tmp / "03_filler.mp4"
        f_color   = tmp / "04_color.mp4"
        f_concat  = tmp / "05_concat.mp4"
        f_srt     = output_dir / f"{nombre_limpio}.srt"
        f_final   = output_dir / f"{nombre_limpio}_{ts}.mp4"

        resultados = {}

        # ── Paso 1: Strip metadatos
        resultados["metadata"] = strip_metadata(input_path, f_meta)
        fuente = f_meta if f_meta.exists() else input_path

        # ── Paso 2: Eliminar silencios
        resultados["silences"] = remove_silence(fuente, f_silence)
        fuente = f_silence if f_silence.exists() else fuente

        # ── Paso 3: Transcripción + subtítulos
        segments = transcribe_and_subtitle(fuente, f_srt, language=language)
        resultados["subtitles"] = len(segments) > 0

        # ── Paso 4: Eliminar filler words
        resultados["fillers"] = remove_filler_words(fuente, f_filler, segments, language)
        fuente = f_filler if f_filler.exists() else fuente

        # ── Paso 5: Corrección de color
        resultados["color"] = color_correction(fuente, f_color)
        fuente = f_color if f_color.exists() else fuente

        # ── Paso 6: Intro/Outro
        resultados["intro_outro"] = add_intro_outro(fuente, f_concat)
        fuente = f_concat if f_concat.exists() else fuente

        # ── Paso 7: Export para Skool
        resultados["export"] = export_for_skool(
            fuente, f_final,
            srt_path=f_srt if f_srt.exists() else None
        )

        # Copiar también al directorio _PROCESADOS_SKOOL
        if resultados["export"] and f_final.exists():
            skool_dest = SKOOL_DIR / f_final.name
            shutil.copy(f_final, skool_dest)
            log(f"Copiado a _PROCESADOS_SKOOL/", "ok")

    fin      = datetime.now()
    duracion = (fin - inicio).total_seconds()

    print(f"\n{'─'*55}")
    print(f"  RESULTADO: {input_path.name}")
    print(f"  Tiempo total: {duracion:.0f}s")
    for paso, ok in resultados.items():
        icono = "✓" if ok else "⚠"
        print(f"    {icono} {paso}")
    print(f"{'─'*55}\n")

    return resultados


def procesar_carpeta(raw_dir: Path, editados_dir: Path,
                     language: str = "es"):
    """Procesa todos los MP4 en una carpeta raw/."""
    videos = list(raw_dir.glob("*.mp4")) + list(raw_dir.glob("*.MP4")) + \
             list(raw_dir.glob("*.mov")) + list(raw_dir.glob("*.MOV"))

    if not videos:
        log(f"No hay videos en {raw_dir}", "warn")
        return

    log(f"Encontrados {len(videos)} videos en {raw_dir.parent.name}/{raw_dir.name}", "info")

    for i, video in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}]", end="")
        procesar_video(video, editados_dir, language=language)


# ================================================================
# INTERFAZ DE LÍNEA DE COMANDOS
# ================================================================

def main():
    parser = argparse.ArgumentParser(
        description="GZBR — Pipeline automático de videos para Skool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python3 procesar_videos.py --ica ICA-03 --nivel PRINCIPIANTE
  python3 procesar_videos.py --ica ICA-03 --nivel INTERMEDIO
  python3 procesar_videos.py --ica ICA-03          # procesa ambos niveles
  python3 procesar_videos.py --todos               # procesa TODO
  python3 procesar_videos.py --introduccion        # solo introducción
  python3 procesar_videos.py --archivo /ruta/video.mp4
        """
    )

    parser.add_argument("--ica",          type=str, help="ICA a procesar (ej: ICA-03)")
    parser.add_argument("--nivel",        type=str, choices=["PRINCIPIANTE", "INTERMEDIO"],
                        help="Nivel a procesar")
    parser.add_argument("--todos",        action="store_true", help="Procesa todos los ICAs")
    parser.add_argument("--introduccion", action="store_true", help="Procesa carpeta 00-INTRODUCCION")
    parser.add_argument("--archivo",      type=str, help="Ruta a un video específico")
    parser.add_argument("--idioma",       type=str, default="es",
                        choices=["es", "en"], help="Idioma para subtítulos (default: es)")
    parser.add_argument("--ayuda",        action="store_true", help="Muestra este mensaje")

    args = parser.parse_args()

    if args.ayuda or len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    # Verificaciones previas
    print("\n🎬 GZBR Video Pipeline\n")

    if not check_ffmpeg():
        print(ERR + "FFmpeg no instalado. Ejecuta: bash instalar_dependencias.sh")
        sys.exit(1)

    SKOOL_DIR.mkdir(parents=True, exist_ok=True)

    # ── Modo: archivo individual
    if args.archivo:
        video_path = Path(args.archivo)
        if not video_path.exists():
            log(f"Archivo no encontrado: {args.archivo}", "err")
            sys.exit(1)
        output_dir = video_path.parent.parent / "editados"
        procesar_video(video_path, output_dir, language=args.idioma)

    # ── Modo: introducción
    elif args.introduccion:
        raw = DISK_BASE / "00-INTRODUCCION" / "raw"
        out = DISK_BASE / "00-INTRODUCCION" / "editados"
        procesar_carpeta(raw, out, language=args.idioma)

    # ── Modo: ICA específico
    elif args.ica:
        ica_dir = DISK_BASE / args.ica.upper()
        if not ica_dir.exists():
            log(f"Carpeta no encontrada: {ica_dir}", "err")
            sys.exit(1)

        niveles = [args.nivel] if args.nivel else ["PRINCIPIANTE", "INTERMEDIO"]
        for nivel in niveles:
            raw = ica_dir / nivel / "raw"
            out = ica_dir / nivel / "editados"
            if raw.exists():
                procesar_carpeta(raw, out, language=args.idioma)
            else:
                log(f"Carpeta raw no existe: {raw}", "warn")

    # ── Modo: todos
    elif args.todos:
        # Introducción
        procesar_carpeta(
            DISK_BASE / "00-INTRODUCCION" / "raw",
            DISK_BASE / "00-INTRODUCCION" / "editados",
            language=args.idioma
        )
        # ICAs 1-11
        for n in range(1, 12):
            ica = f"ICA-{n:02d}"
            for nivel in ["PRINCIPIANTE", "INTERMEDIO"]:
                raw = DISK_BASE / ica / nivel / "raw"
                out = DISK_BASE / ica / nivel / "editados"
                if raw.exists():
                    procesar_carpeta(raw, out, language=args.idioma)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
