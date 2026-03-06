#!/usr/bin/env bash
set -euo pipefail

# K.3.1 dependency installer for Omni-BMO interactive transport drills.
# Targets Debian/Ubuntu/Raspberry Pi OS environments.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "[k3-deps] starting install in $ROOT"

if ! command -v apt-get >/dev/null 2>&1; then
  echo "[k3-deps] apt-get not found. Install dependencies manually for your distro."
  exit 1
fi

sudo apt-get update -y
sudo apt-get install -y \
  git curl ca-certificates \
  alsa-utils ffmpeg \
  python3 python3-venv python3-pip \
  build-essential cmake pkg-config libasound2-dev

# rpicam-still is usually present on Pi images; on non-Pi hosts this may be unavailable.
if ! command -v rpicam-still >/dev/null 2>&1; then
  echo "[k3-deps] rpicam-still not found. Attempting install..."
  sudo apt-get install -y libcamera-apps || true
fi

# Whisper.cpp binary
if [[ ! -x "$ROOT/whisper.cpp/build/bin/whisper-cli" ]]; then
  echo "[k3-deps] installing whisper.cpp"
  if [[ ! -d "$ROOT/whisper.cpp/.git" ]]; then
    rm -rf "$ROOT/whisper.cpp"
    git clone https://github.com/ggerganov/whisper.cpp.git "$ROOT/whisper.cpp"
  fi
  cmake -S "$ROOT/whisper.cpp" -B "$ROOT/whisper.cpp/build"
  cmake --build "$ROOT/whisper.cpp/build" -j "$(nproc)"
fi

# Whisper model (tiny.en default in this project)
mkdir -p "$ROOT/models"
if [[ ! -f "$ROOT/models/ggml-tiny.en.bin" ]]; then
  echo "[k3-deps] downloading whisper tiny.en model"
  curl -L -o "$ROOT/models/ggml-tiny.en.bin" \
    https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin
fi

# Piper binary
if [[ ! -x "$ROOT/piper/piper" ]]; then
  echo "[k3-deps] installing piper binary"
  mkdir -p "$ROOT/piper"
  arch="$(uname -m)"
  case "$arch" in
    x86_64) piper_url="https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz" ;;
    aarch64|arm64) piper_url="https://github.com/rhasspy/piper/releases/latest/download/piper_linux_aarch64.tar.gz" ;;
    armv7l|armv6l) piper_url="https://github.com/rhasspy/piper/releases/latest/download/piper_linux_armv7l.tar.gz" ;;
    *)
      echo "[k3-deps] unsupported arch for auto piper install: $arch"
      piper_url=""
      ;;
  esac

  if [[ -n "$piper_url" ]]; then
    tmp_tar="/tmp/piper-$$.tar.gz"
    curl -L -o "$tmp_tar" "$piper_url"
    tar -xzf "$tmp_tar" -C "$ROOT/piper" --strip-components=1
    rm -f "$tmp_tar"
  fi
fi

# Optional voice model placeholder
if [[ ! -f "$ROOT/piper/en_GB-semaine-medium.onnx" ]]; then
  echo "[k3-deps] NOTE: voice model missing at piper/en_GB-semaine-medium.onnx"
  echo "[k3-deps] Add your preferred Piper voice model + .json metadata file."
fi

echo "[k3-deps] completed"
echo "[k3-deps] next: ./scripts/bmo_omni_doctor.sh && ./scripts/run_validation_matrix.sh"
