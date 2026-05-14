#!/bin/bash

# Define colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🤖 Pi Local Assistant Setup Script${NC}"

# 1. Install System Dependencies (The "Hidden" Requirements)
echo -e "${YELLOW}[1/7] Installing System Tools (apt)...${NC}"
sudo apt update
sudo apt install -y python3-tk libasound2-dev libportaudio2 libatlas-base-dev cmake build-essential espeak-ng git wget curl

# 2. Create Folders
echo -e "${YELLOW}[2/7] Creating Folders...${NC}"
mkdir -p piper
mkdir -p tts
mkdir -p sounds/greeting_sounds
mkdir -p sounds/thinking_sounds
mkdir -p sounds/ack_sounds
mkdir -p sounds/error_sounds
mkdir -p faces/idle
mkdir -p faces/listening
mkdir -p faces/thinking
mkdir -p faces/speaking
mkdir -p faces/error
mkdir -p faces/warmup

# 3. Download Piper (Architecture Check)
echo -e "${YELLOW}[3/7] Setting up Piper TTS...${NC}"
ARCH=$(uname -m)
if [ "$ARCH" == "aarch64" ]; then
    # Using the specific 2023.11.14-2 release known to work on Pi.
    if [ ! -x "piper/piper" ] && [ ! -x "piper/piper.real" ]; then
        wget -O piper.tar.gz https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_aarch64.tar.gz
        tar -xvf piper.tar.gz -C piper --strip-components=1
        rm piper.tar.gz
    else
        echo -e "${GREEN}[ok] Piper binary already present.${NC}"
    fi
else
    echo -e "${RED}⚠️  Not on Raspberry Pi (aarch64). Skipping Piper binary download.${NC}"
fi

# 4. Download Voice Model
echo -e "${YELLOW}[4/7] Downloading Voice Model...${NC}"
cd piper
wget -nc -O en_GB-semaine-medium.onnx https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/semaine/medium/en_GB-semaine-medium.onnx
wget -nc -O en_GB-semaine-medium.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/semaine/medium/en_GB-semaine-medium.onnx.json
cd ..

# 5. Install Python Libraries
echo -e "${YELLOW}[5/7] Installing Python Libraries...${NC}"
# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 6. Install Buddy voice wrapper over Piper
echo -e "${YELLOW}[6/7] Installing Buddy Piper voice profile...${NC}"
python3 tts/buddy_piper_filter.py --install-wrapper || true

# 7. Pull AI Models
echo -e "${YELLOW}[7/7] Checking AI Models...${NC}"
if command -v ollama &> /dev/null; then
    ollama pull gemma3:1b
    ollama pull moondream
else
    echo -e "${RED}❌ Ollama not found. Please install it manually.${NC}"
fi

# OpenWakeWord Model
if [ ! -f "wakeword.onnx" ]; then
    echo -e "${YELLOW}Downloading default 'Hey Jarvis' wake word...${NC}"
    curl -L -o wakeword.onnx https://github.com/dscripka/openWakeWord/raw/main/openwakeword/resources/models/hey_jarvis_v0.1.onnx
fi

echo -e "${GREEN}✨ Setup Complete! Run 'source venv/bin/activate' then 'python agent.py'${NC}"
