# =========================================================================
#  Be More Agent 🤖
#  A Local, Offline-First AI Agent for Raspberry Pi
#
#  Copyright (c) 2026 brenpoly
#  Licensed under the MIT License
#  Source: https://github.com/brenpoly/be-more-agent
#
#  DISCLAIMER:
#  This software is provided "as is", without warranty of any kind.
#  This project is a generic framework and includes no copyrighted assets.
# =========================================================================

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
import json
import os
import subprocess
import random
import re
import sys
import select
import traceback
import atexit
import datetime
import warnings
import wave
import struct
import urllib.request
import urllib.error

# Suppress harmless library warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="duckduckgo_search")

# Core dependencies
import sounddevice as sd
import numpy as np
import scipy.signal 

# --- AI ENGINES ---
import openwakeword
from openwakeword.model import Model
import ollama 

# --- WEB SEARCH (Using your working import) ---
from ddgs import DDGS 

# =========================================================================
# 1. CONFIGURATION & CONSTANTS
# =========================================================================

CONFIG_FILE = "config.json"
MEMORY_FILE = "memory.json"
BMO_IMAGE_FILE = "current_image.jpg"
WAKE_WORD_MODEL = "./wakeword.onnx"

# HARDWARE SETTINGS
INPUT_DEVICE_NAME = None 

DEFAULT_CONFIG = {
    "text_model": "gemma3:1b",
    "vision_model": "moondream",
    "voice_model": "piper/en_GB-semaine-medium.onnx",
    "chat_memory": True,
    "camera_rotation": 0,
    "system_prompt_extras": "",
    "llm_backend": "ollama",  # ollama|omni
    "omni_base_url": "http://127.0.0.1:8799/api/omni",
    "omni_token_env": "PRISMBOT_API_TOKEN",
    "omni_model": "omni-core:phase2",
    "omni_tool_route_mode": "hybrid",  # off|hybrid|direct
    "omni_stream_chunk_chars": 48,
    "omni_fallback_to_ollama": True,
    "omni_request_timeout_sec": 90,
    "omni_vision_mode": "hybrid",  # local|hybrid

    # Milestone G transport routing
    "transport_mode": "auto",  # online|mesh|reticulum_fallback|auto
    "mesh_health_check_url": "",
    "reticulum_bridge_endpoint": "",
    "transport_failover_timeout_sec": 2.0,

    # Milestone E latency / wake / barge-in tuning
    "wake_word_threshold": 0.45,
    "ptt_toggle_debounce_sec": 0.25,
    "adaptive_pre_record_sec": 0.20,
    "ptt_pre_record_sec": 0.15,
    "silence_threshold": 0.0055,
    "silence_duration_sec": 0.65,
    "max_record_time_sec": 8.0,
    "tts_tail_sec": 0.20,
    "thinking_sound_initial_delay_sec": 0.25
}

# LLM SETTINGS
OLLAMA_OPTIONS = {
    'keep_alive': '-1',     
    'num_thread': 4,
    'temperature': 0.7,     
    'top_k': 40,
    'top_p': 0.9
}

def load_config():
    config = DEFAULT_CONFIG.copy()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                user_config = json.load(f)
                config.update(user_config)
        except Exception as e:
            print(f"Config Error: {e}. Using defaults.")
    return config

CURRENT_CONFIG = load_config()
TEXT_MODEL = CURRENT_CONFIG["text_model"]
VISION_MODEL = CURRENT_CONFIG["vision_model"]
LLM_BACKEND = str(CURRENT_CONFIG.get("llm_backend", "ollama")).strip().lower()
OMNI_BASE_URL = str(CURRENT_CONFIG.get("omni_base_url", "http://127.0.0.1:8799/api/omni")).strip().rstrip('/')
OMNI_TOKEN_ENV = str(CURRENT_CONFIG.get("omni_token_env", "PRISMBOT_API_TOKEN")).strip()
OMNI_MODEL = str(CURRENT_CONFIG.get("omni_model", "omni-core:phase2")).strip()
OMNI_TOOL_ROUTE_MODE = str(CURRENT_CONFIG.get("omni_tool_route_mode", "hybrid")).strip().lower()  # off|hybrid|direct
OMNI_STREAM_CHUNK_CHARS = int(CURRENT_CONFIG.get("omni_stream_chunk_chars", 48))
OMNI_FALLBACK_TO_OLLAMA = bool(CURRENT_CONFIG.get("omni_fallback_to_ollama", True))
OMNI_REQUEST_TIMEOUT_SEC = int(CURRENT_CONFIG.get("omni_request_timeout_sec", 90))
OMNI_VISION_MODE = str(CURRENT_CONFIG.get("omni_vision_mode", "hybrid")).strip().lower()  # local|hybrid

# Transport selection (Milestone G)
TRANSPORT_MODE = str(CURRENT_CONFIG.get("transport_mode", "auto")).strip().lower()  # online|mesh|reticulum_fallback|auto
MESH_HEALTH_CHECK_URL = str(CURRENT_CONFIG.get("mesh_health_check_url", "")).strip()
RETICULUM_BRIDGE_ENDPOINT = str(CURRENT_CONFIG.get("reticulum_bridge_endpoint", "")).strip()
TRANSPORT_FAILOVER_TIMEOUT_SEC = float(CURRENT_CONFIG.get("transport_failover_timeout_sec", 2.0))

# Latency tuning knobs
WAKE_WORD_THRESHOLD = float(CURRENT_CONFIG.get("wake_word_threshold", 0.45))
PTT_TOGGLE_DEBOUNCE_SEC = float(CURRENT_CONFIG.get("ptt_toggle_debounce_sec", 0.25))
ADAPTIVE_PRE_RECORD_SEC = float(CURRENT_CONFIG.get("adaptive_pre_record_sec", 0.20))
PTT_PRE_RECORD_SEC = float(CURRENT_CONFIG.get("ptt_pre_record_sec", 0.15))
SILENCE_THRESHOLD = float(CURRENT_CONFIG.get("silence_threshold", 0.0055))
SILENCE_DURATION_SEC = float(CURRENT_CONFIG.get("silence_duration_sec", 0.65))
MAX_RECORD_TIME_SEC = float(CURRENT_CONFIG.get("max_record_time_sec", 8.0))
TTS_TAIL_SEC = float(CURRENT_CONFIG.get("tts_tail_sec", 0.20))
THINKING_SOUND_INITIAL_DELAY_SEC = float(CURRENT_CONFIG.get("thinking_sound_initial_delay_sec", 0.25))

class BotStates:
    IDLE = "idle"             
    LISTENING = "listening"   
    THINKING = "thinking"     
    SPEAKING = "speaking"     
    ERROR = "error"           
    CAPTURING = "capturing" 
    WARMUP = "warmup"       

# --- SYSTEM PROMPT ---
BASE_SYSTEM_PROMPT = """You are a helpful robot assistant running on a Raspberry Pi.
Personality: Cute, helpful, robot.
Style: Short sentences. Enthusiastic.

INSTRUCTIONS:
- If the user asks for a physical action (time, search, photo), output JSON.
- If the user just wants to chat, reply with NORMAL TEXT.

### EXAMPLES ###

User: What time is it?
You: {"action": "get_time", "value": "now"}

User: Hello!
You: Hi! I am ready to help!

User: Search for news about robots.
You: {"action": "search_web", "value": "robots news"}

User: What do you see right now?
You: {"action": "capture_image", "value": "environment"}

### END EXAMPLES ###
"""

SYSTEM_PROMPT = BASE_SYSTEM_PROMPT + "\n\n" + CURRENT_CONFIG.get("system_prompt_extras", "")

# Sound Directories
greeting_sounds_dir = "sounds/greeting_sounds"
ack_sounds_dir = "sounds/ack_sounds"
thinking_sounds_dir = "sounds/thinking_sounds"
error_sounds_dir = "sounds/error_sounds"

# =========================================================================
# 2. GUI CLASS
# =========================================================================

class BotGUI:
    BG_WIDTH, BG_HEIGHT = 800, 480 
    OVERLAY_WIDTH, OVERLAY_HEIGHT = 400, 300 

    def __init__(self, master):
        self.master = master
        master.title("Pi Assistant")
        master.attributes('-fullscreen', True) 
        master.bind('<Escape>', self.exit_fullscreen)
        
        # Inputs
        master.bind('<Return>', self.handle_ptt_toggle)
        master.bind('<space>', self.handle_speaking_interrupt)
        master.bind('<F6>', self.handle_transport_cycle_hotkey)
        master.bind('<F7>', self.handle_transport_doctor_hotkey)
        atexit.register(self.safe_exit)
        
        # State
        self.current_state = BotStates.WARMUP
        self.current_volume = 0 
        self.animations = {}
        self.current_frame_index = 0
        self.current_overlay_image = None

        self.current_transport_mode = "online"
        self.transport_last_reason = "init"
        
        self.permanent_memory = self.load_chat_history()
        self.session_memory = []
        self.thinking_sound_active = threading.Event()
        
        self.last_ptt_time = 0 
        self.ptt_event = threading.Event()       
        self.recording_active = threading.Event() 
        self.interrupted = threading.Event() 
        
        self.tts_queue = []          
        self.tts_queue_lock = threading.Lock() 
        self.tts_thread = None       
        self.tts_active = threading.Event()
        self.current_audio_process = None 
        
        # --- WAKE WORD INITIALIZATION ---
        print("[INIT] Loading Wake Word...", flush=True)
        self.oww_model = None
        if os.path.exists(WAKE_WORD_MODEL):
            try:
                self.oww_model = Model(wakeword_model_paths=[WAKE_WORD_MODEL])
                print("[INIT] Wake Word Loaded.", flush=True)
            except TypeError:
                try:
                    self.oww_model = Model(wakeword_models=[WAKE_WORD_MODEL])
                    print("[INIT] Wake Word Loaded (New API).", flush=True)
                except Exception as e:
                    print(f"[CRITICAL] Failed to load model: {e}")
            except Exception as e:
                print(f"[CRITICAL] Failed to load model: {e}")
        else:
            print(f"[CRITICAL] Model not found: {WAKE_WORD_MODEL}")

        # GUI Setup
        self.background_label = tk.Label(master)
        self.background_label.place(x=0, y=0, width=self.BG_WIDTH, height=self.BG_HEIGHT)
        self.background_label.bind('<Button-1>', self.toggle_hud_visibility) 
        
        self.overlay_label = tk.Label(master, bg='black')
        self.overlay_label.bind('<Button-1>', self.toggle_hud_visibility)
        
        self.response_text = tk.Text(master, height=6, width=60, wrap=tk.WORD, 
                                     state=tk.DISABLED, bg="#ffffff", fg="#000000", font=('Arial', 12)) 
        
        self.status_var = tk.StringVar(value="Initializing...")
        self.status_label = ttk.Label(master, textvariable=self.status_var, background="#2e2e2e", foreground="white")
        
        self.exit_button = ttk.Button(master, text="Exit & Save", command=self.safe_exit)

        self.load_animations()
        self.update_animation() 
        
        threading.Thread(target=self.safe_main_execution, daemon=True).start()

    # --- HELPERS ---

    def extract_json_from_text(self, text):
        try:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return None
        except: return None

    def safe_exit(self):
        print("\n--- SHUTDOWN SEQUENCE ---", flush=True)
        if self.current_audio_process:
            try:
                self.current_audio_process.terminate()
                self.current_audio_process.wait(timeout=1)
            except: pass

        self.recording_active.clear()
        self.thinking_sound_active.clear()
        self.tts_active.clear() 
        
        self.save_chat_history()
        
        try:
            if LLM_BACKEND != "omni":
                ollama.generate(model=TEXT_MODEL, prompt="", keep_alive=0)
        except: pass

        self.master.quit()
        sys.exit(0) 
        
    def exit_fullscreen(self, event=None):
        self.master.attributes('-fullscreen', False)
        self.safe_exit()

    def toggle_hud_visibility(self, event=None):
        try:
            if self.response_text.winfo_ismapped():
                self.response_text.place_forget()
                self.status_label.place_forget()
                self.exit_button.place_forget()
            else:
                self.response_text.place(relx=0.5, rely=0.82, anchor=tk.S)
                self.status_label.place(relx=0.5, rely=1.0, anchor=tk.S, relwidth=1)
                self.exit_button.place(x=10, y=10)
        except tk.TclError: pass

    def handle_ptt_toggle(self, event=None):
        current_time = time.time()
        if current_time - self.last_ptt_time < max(0.05, PTT_TOGGLE_DEBOUNCE_SEC): 
            return 
        self.last_ptt_time = current_time

        if self.recording_active.is_set():
            print("[PTT] Toggle OFF", flush=True)
            self.recording_active.clear() 
        else:
            if self.current_state == BotStates.IDLE or "Wait" in self.status_var.get():
                print("[PTT] Toggle ON", flush=True)
                self.recording_active.set() 
                self.ptt_event.set()

    def handle_speaking_interrupt(self, event=None):
        if self.current_state == BotStates.SPEAKING or self.current_state == BotStates.THINKING:
            self.interrupted.set()
            self.thinking_sound_active.clear()
            with self.tts_queue_lock:
                self.tts_queue.clear()
            if self.current_audio_process:
                try: self.current_audio_process.terminate()
                except: pass
            self.set_state(BotStates.IDLE, "Interrupted.")

    def _transport_doctor_summary(self):
        selected = self.select_transport_mode()
        mesh_ok = False
        if MESH_HEALTH_CHECK_URL:
            mesh_ok = self._http_ping(MESH_HEALTH_CHECK_URL, timeout_sec=TRANSPORT_FAILOVER_TIMEOUT_SEC)
        omni_ok = self._http_ping(f"{OMNI_BASE_URL}/health", timeout_sec=TRANSPORT_FAILOVER_TIMEOUT_SEC)
        return (
            f"transport={selected}; reason={self.transport_last_reason}; "
            f"omni_health={'ok' if omni_ok else 'down'}; "
            f"mesh_health={'ok' if mesh_ok else ('n/a' if not MESH_HEALTH_CHECK_URL else 'down')}; "
            f"reticulum={'set' if RETICULUM_BRIDGE_ENDPOINT else 'unset'}"
        )

    def handle_transport_cycle_hotkey(self, event=None):
        order = ['auto', 'online', 'mesh', 'reticulum_fallback']
        cur = str(getattr(self, 'transport_mode_override', '') or CURRENT_CONFIG.get('transport_mode', TRANSPORT_MODE)).strip().lower()
        if cur not in order:
            cur = 'auto'
        nxt = order[(order.index(cur) + 1) % len(order)]
        self.transport_mode_override = nxt
        self.current_transport_mode = self.select_transport_mode()
        msg = f"Transport mode -> {nxt} ({self.current_transport_mode})"
        print(f"[TRANSPORT] {msg}", flush=True)
        self.set_state(BotStates.IDLE, msg)

    def handle_transport_doctor_hotkey(self, event=None):
        summary = self._transport_doctor_summary()
        print(f"[TRANSPORT_DOCTOR] {summary}", flush=True)
        self.set_state(BotStates.IDLE, summary)

    def load_animations(self):
        base_path = "faces"
        states = ["idle", "listening", "thinking", "speaking", "error", "capturing", "warmup"] 
        for state in states:
            folder = os.path.join(base_path, state)
            self.animations[state] = []
            if os.path.exists(folder):
                files = sorted([f for f in os.listdir(folder) if f.lower().endswith('.png')])
                for f in files:
                    img = Image.open(os.path.join(folder, f)).resize((self.BG_WIDTH, self.BG_HEIGHT))
                    self.animations[state].append(ImageTk.PhotoImage(img))
            if not self.animations[state]:
                if state in self.animations.get("idle", []):
                     self.animations[state] = self.animations["idle"]
                else:
                    # Blue screen fallback
                    blank = Image.new('RGB', (self.BG_WIDTH, self.BG_HEIGHT), color='#0000FF')
                    self.animations[state].append(ImageTk.PhotoImage(blank))

    def update_animation(self):
        frames = self.animations.get(self.current_state, []) or self.animations.get(BotStates.IDLE, [])
        if not frames:
            self.master.after(500, self.update_animation)
            return

        if self.current_state == BotStates.SPEAKING:
            if len(frames) > 1:
                self.current_frame_index = random.randint(1, len(frames) - 1)
            else:
                self.current_frame_index = 0 
        else:
            self.current_frame_index = (self.current_frame_index + 1) % len(frames)

        self.background_label.config(image=frames[self.current_frame_index])
        
        speed = 50 if self.current_state == BotStates.SPEAKING else 500
        self.master.after(speed, self.update_animation)

    def _status_with_transport(self, msg):
        base = str(msg or "").strip()
        mode = str(getattr(self, 'current_transport_mode', 'online') or 'online')
        if not base:
            return f"net:{mode}"
        return f"{base} | net:{mode}"

    def set_state(self, state, msg="", cam_path=None):
        def _update():
            if msg: print(f"[STATE] {state.upper()}: {msg}", flush=True)
            if self.current_state != state:
                self.current_state = state
                self.current_frame_index = 0
            if msg: self.status_var.set(self._status_with_transport(msg))
            if cam_path and os.path.exists(cam_path) and state in [BotStates.THINKING, BotStates.SPEAKING]:
                try:
                    img = Image.open(cam_path).resize((self.OVERLAY_WIDTH, self.OVERLAY_HEIGHT))
                    self.current_overlay_image = ImageTk.PhotoImage(img)
                    self.overlay_label.config(image=self.current_overlay_image)
                    self.overlay_label.place(x=200, y=90)
                except: pass
            else:
                self.overlay_label.place_forget()
        self.master.after(0, _update)

    def append_to_text(self, text, newline=True):
        def _update():
            self.response_text.config(state=tk.NORMAL)
            if newline: 
                self.response_text.insert(tk.END, text + "\n")
            else: 
                self.response_text.insert(tk.END, text)
            
            self.response_text.see(tk.END)
            self.response_text.config(state=tk.DISABLED)
            
        self.master.after(0, _update)

    def _stream_to_text(self, chunk):
        def update_text_stream():
            self.response_text.config(state=tk.NORMAL)
            self.response_text.insert(tk.END, chunk)
            self.response_text.see(tk.END) 
            self.response_text.config(state=tk.DISABLED)
        self.master.after(0, update_text_stream)

    # =========================================================================
    # 3. ACTION ROUTER
    # =========================================================================
    
    def execute_action_and_get_result(self, action_data):
        raw_action = action_data.get("action", "").lower().strip()
        value = action_data.get("value") or action_data.get("query")
        
        VALID_TOOLS = {
            "get_time", "search_web", "capture_image"
        }
        
        ALIASES = {
            "google": "search_web", "browser": "search_web", "news": "search_web",         
            "search_news": "search_web", "look": "capture_image", "see": "capture_image", 
            "check_time": "get_time"
        }

        action = ALIASES.get(raw_action, raw_action)
        print(f"ACTION: {raw_action} -> {action}", flush=True)

        if action not in VALID_TOOLS:
            if value and isinstance(value, str) and len(value.split()) > 1:
                return f"CHAT_FALLBACK::{value}"
            return "INVALID_ACTION"

        if action == "get_time":
            now = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current time is {now}."
        
        elif action == "search_web":
            print(f"Searching web for: {value}...", flush=True)
            try:
                # 'us-en' region is often more stable for CLI queries
                with DDGS() as ddgs:
                    results = []
                    # 1. News search
                    try:
                        results = list(ddgs.news(value, region='us-en', max_results=1))
                        if results: 
                            print(f"[DEBUG] Found News: {results[0].get('title')}", flush=True)
                    except Exception as e: 
                        print(f"[DEBUG] News Search Error: {e}", flush=True)
                    
                    # 2. Text fallback
                    if not results:
                        print("[DEBUG] No news found, trying text search...", flush=True)
                        try: 
                            results = list(ddgs.text(value, region='us-en', max_results=1))
                            if results: 
                                print(f"[DEBUG] Found Text: {results[0].get('title')}", flush=True)
                        except Exception as e:
                             print(f"[DEBUG] Text Search Error: {e}", flush=True)

                    if results:
                        r = results[0]
                        # Safe get
                        title = r.get('title', 'No Title')
                        body = r.get('body', r.get('snippet', 'No Body'))
                        return f"SEARCH RESULTS for '{value}':\nTitle: {title}\nSnippet: {body[:300]}"
                    else: 
                        print(f"[DEBUG] Search returned 0 results.", flush=True)
                        return "SEARCH_EMPTY"
            except Exception as e:
                print(f"[DEBUG] Connection/Library Error: {e}", flush=True)
                return "SEARCH_ERROR"
        
        elif action == "capture_image":
             return "IMAGE_CAPTURE_TRIGGERED"

        return None

    def infer_direct_action(self, text):
        t = str(text or "").strip()
        low = t.lower()
        if not t:
            return None

        # Time intent
        if any(k in low for k in ["what time", "time is it", "current time", "tell me the time"]):
            return {"action": "get_time", "value": "now"}

        # Vision/camera intent
        if any(k in low for k in ["what do you see", "look around", "take a photo", "take a picture", "show me what you see"]):
            return {"action": "capture_image", "value": "environment"}

        # Search intent
        m = re.match(r"^(search|look up|google|find)\s+(.+)$", low)
        if m and m.group(2).strip():
            return {"action": "search_web", "value": m.group(2).strip()}
        if "search for" in low:
            q = low.split("search for", 1)[1].strip(" .?!")
            if q:
                return {"action": "search_web", "value": q}

        return None

    def respond_with_tool_result(self, tool_result, user_text, model_to_use, img_path=None):
        if tool_result and tool_result.startswith("CHAT_FALLBACK::"):
            chat_text = tool_result.split("::", 1)[1]
            self.thinking_sound_active.clear()
            self.set_state(BotStates.SPEAKING, "Speaking...", cam_path=img_path)
            self.append_to_text("BOT: ", newline=False)
            self.append_to_text(chat_text, newline=True)
            with self.tts_queue_lock:
                self.tts_queue.append(chat_text)
            self.session_memory.append({"role": "assistant", "content": chat_text})
            self.wait_for_tts()
            self.set_state(BotStates.IDLE, "Ready")
            return True

        if tool_result == "IMAGE_CAPTURE_TRIGGERED":
            new_img_path = self.capture_image()
            if new_img_path:
                self.chat_and_respond(user_text, img_path=new_img_path)
            return True

        if tool_result == "INVALID_ACTION":
            fallback_text = "I am not sure how to do that."
        elif tool_result == "SEARCH_EMPTY":
            fallback_text = "I searched, but I couldn't find any news about that."
        elif tool_result == "SEARCH_ERROR":
            fallback_text = "I cannot reach the internet right now."
        elif tool_result:
            summary_prompt = [
                {"role": "system", "content": "Summarize this result in one short sentence."},
                {"role": "user", "content": f"RESULT: {tool_result}\nUser Question: {user_text}"}
            ]
            self.set_state(BotStates.THINKING, "Reading...")
            self.thinking_sound_active.set()
            final_resp = self.llm_chat_once(model=model_to_use, messages=summary_prompt, img_path=img_path)
            final_text = final_resp['message']['content']

            self.thinking_sound_active.clear()
            self.set_state(BotStates.SPEAKING, "Speaking...", cam_path=img_path)
            self.append_to_text("BOT: ", newline=False)
            self.append_to_text(final_text, newline=True)
            with self.tts_queue_lock:
                self.tts_queue.append(final_text)
            self.session_memory.append({"role": "assistant", "content": final_text})
            self.wait_for_tts()
            self.set_state(BotStates.IDLE, "Ready")
            return True

        if 'fallback_text' in locals():
            self.thinking_sound_active.clear()
            self.set_state(BotStates.SPEAKING, "Speaking...", cam_path=img_path)
            self.append_to_text("BOT: ", newline=False)
            self.append_to_text(fallback_text, newline=True)
            with self.tts_queue_lock:
                self.tts_queue.append(fallback_text)
            self.wait_for_tts()
            self.set_state(BotStates.IDLE, "Ready")
            return True

        return False

    # =========================================================================
    # 4. CORE LOGIC
    # =========================================================================

    def safe_main_execution(self):
        try:
            self.warm_up_logic()
            self.tts_active.set()
            self.tts_thread = threading.Thread(target=self._tts_worker, daemon=True)
            self.tts_thread.start()
            
            while True:
                trigger_source = self.detect_wake_word_or_ptt()
                if self.interrupted.is_set():
                    self.interrupted.clear()
                    self.set_state(BotStates.IDLE, "Resetting...")
                    continue

                self.set_state(BotStates.LISTENING, "I'm listening!")
                
                audio_file = None
                if trigger_source == "PTT":
                    audio_file = self.record_voice_ptt()
                else:
                    audio_file = self.record_voice_adaptive()
                
                if not audio_file: 
                    self.set_state(BotStates.IDLE, "Heard nothing.")
                    continue
                
                user_text = self.transcribe_audio(audio_file)
                if not user_text:
                    self.set_state(BotStates.IDLE, "Transcription empty.")
                    continue
                
                self.append_to_text(f"YOU: {user_text}")
                self.interrupted.clear()
                self.chat_and_respond(user_text, img_path=None)
                    
        except Exception as e:
            traceback.print_exc()
            self.set_state(BotStates.ERROR, f"Fatal Error: {str(e)[:40]}")

    def warm_up_logic(self):
        self.set_state(BotStates.WARMUP, "Warming up brains...")
        try:
            if LLM_BACKEND != "omni":
                ollama.generate(model=TEXT_MODEL, prompt="", keep_alive=-1)
        except Exception as e:
            print(f"Failed to load {TEXT_MODEL}: {e}", flush=True)
        self.play_sound(self.get_random_sound(greeting_sounds_dir))
        print("Models loaded.", flush=True)

    def detect_wake_word_or_ptt(self):
        self.set_state(BotStates.IDLE, "Waiting...")
        self.ptt_event.clear()
        
        if self.oww_model: self.oww_model.reset()

        if self.oww_model is None:
            self.ptt_event.wait()
            self.ptt_event.clear()
            return "PTT"

        CHUNK_SIZE = 1280
        OWW_SAMPLE_RATE = 16000
        
        try:
            device_info = sd.query_devices(kind='input')
            native_rate = int(device_info['default_samplerate'])
        except: native_rate = 48000
            
        use_resampling = (native_rate != OWW_SAMPLE_RATE)
        input_rate = native_rate if use_resampling else OWW_SAMPLE_RATE
        input_chunk_size = int(CHUNK_SIZE * (input_rate / OWW_SAMPLE_RATE)) if use_resampling else CHUNK_SIZE

        try:
            with sd.InputStream(samplerate=input_rate, channels=1, dtype='int16', 
                                blocksize=input_chunk_size, device=INPUT_DEVICE_NAME) as stream:
                while True:
                    if self.ptt_event.is_set():
                        self.ptt_event.clear()
                        return "PTT"
                    
                    rlist, _, _ = select.select([sys.stdin], [], [], 0.001)
                    if rlist: 
                        sys.stdin.readline()
                        return "CLI" 

                    data, _ = stream.read(input_chunk_size)
                    audio_data = np.frombuffer(data, dtype=np.int16)

                    if use_resampling:
                         audio_data = scipy.signal.resample(audio_data, CHUNK_SIZE).astype(np.int16)

                    prediction = self.oww_model.predict(audio_data)
                    for mdl in self.oww_model.prediction_buffer.keys():
                        if list(self.oww_model.prediction_buffer[mdl])[-1] > WAKE_WORD_THRESHOLD:
                            self.oww_model.reset() 
                            return "WAKE"
        except Exception as e:
            print(f"Wake Word Stream Error: {e}")
            self.ptt_event.wait()
            return "PTT"

    def record_voice_adaptive(self, filename="input.wav"):
        print("Recording (Adaptive)...", flush=True)
        time.sleep(max(0.0, ADAPTIVE_PRE_RECORD_SEC)) 
        try:
            device_info = sd.query_devices(kind='input')
            samplerate = int(device_info['default_samplerate'])
        except: samplerate = 44100 

        silence_threshold = max(0.0001, SILENCE_THRESHOLD)
        silence_duration = max(0.2, SILENCE_DURATION_SEC)
        max_record_time = max(2.0, MAX_RECORD_TIME_SEC)
        buffer = []
        silent_chunks = 0
        chunk_duration = 0.05 
        chunk_size = int(samplerate * chunk_duration)
        
        num_silent_chunks = int(silence_duration / chunk_duration)
        max_chunks = int(max_record_time / chunk_duration)
        recorded_chunks = 0
        silence_started = False

        def callback(indata, frames, time_info, status):
            nonlocal silent_chunks, recorded_chunks, silence_started
            volume_norm = np.linalg.norm(indata) / np.sqrt(len(indata))
            buffer.append(indata.copy())  
            recorded_chunks += 1
            if recorded_chunks < 5: return 
            if volume_norm < silence_threshold:
                silent_chunks += 1
                if silent_chunks >= num_silent_chunks: silence_started = True
            else: silent_chunks = 0

        try:
            with sd.InputStream(samplerate=samplerate, channels=1, callback=callback, 
                                device=INPUT_DEVICE_NAME, blocksize=chunk_size): 
                while not silence_started and recorded_chunks < max_chunks:
                    sd.sleep(int(chunk_duration * 1000))
        except Exception as e: return None 
        
        return self.save_audio_buffer(buffer, filename, samplerate)

    def record_voice_ptt(self, filename="input.wav"):
        print("Recording (PTT)...", flush=True)
        time.sleep(max(0.0, PTT_PRE_RECORD_SEC))
        try:
            device_info = sd.query_devices(kind='input')
            samplerate = int(device_info['default_samplerate'])
        except: samplerate = 44100 

        buffer = []
        def callback(indata, frames, time_info, status): buffer.append(indata.copy())
        
        try:
            with sd.InputStream(samplerate=samplerate, channels=1, callback=callback, device=INPUT_DEVICE_NAME):
                while self.recording_active.is_set(): sd.sleep(50)
        except Exception as e: return None
            
        return self.save_audio_buffer(buffer, filename, samplerate)

    def save_audio_buffer(self, buffer, filename, samplerate=16000):
        if not buffer: return None
        audio_data = np.concatenate(buffer, axis=0).flatten()
        audio_data = np.nan_to_num(audio_data, nan=0.0, posinf=0.0, neginf=0.0)
        audio_data = (audio_data * 32767).astype(np.int16)
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(audio_data.tobytes())
        self.play_sound(self.get_random_sound(ack_sounds_dir))
        return filename

    def transcribe_audio(self, filename):
        print("Transcribing...", flush=True)
        try:
            result = subprocess.run(
                ["./whisper.cpp/build/bin/whisper-cli", "-m", "./whisper.cpp/models/ggml-base.en.bin", "-l", "en", "-t", "4", "-f", filename],
                capture_output=True, text=True
            )
            transcription_lines = result.stdout.strip().split('\n')
            if transcription_lines and transcription_lines[-1].strip():
                last_line = transcription_lines[-1].strip()
                if ']' in last_line: transcription = last_line.split("]")[1].strip()
                else: transcription = last_line
            else: transcription = ""
            print(f"Heard: '{transcription}'", flush=True)
            return transcription.strip()
        except Exception as e:
            print(f"Transcription Error: {e}")
            return ""

    def capture_image(self):
        self.set_state(BotStates.CAPTURING, "Watching...")
        try:
            subprocess.run(["rpicam-still", "-t", "500", "-n", "--width", "640", "--height", "480", "-o", BMO_IMAGE_FILE], check=True)
            rotation = CURRENT_CONFIG.get("camera_rotation", 0)
            if rotation != 0:
                img = Image.open(BMO_IMAGE_FILE)
                img = img.rotate(rotation, expand=True) 
                img.save(BMO_IMAGE_FILE)
            return BMO_IMAGE_FILE
        except Exception as e:
            print(f"Camera Error: {e}")
            return None

    def _omni_headers(self):
        headers = {"content-type": "application/json"}
        token = os.getenv(OMNI_TOKEN_ENV, "").strip()
        if token:
            headers["authorization"] = f"Bearer {token}"
        return headers

    def _http_ping(self, url, timeout_sec=2.0):
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=max(0.5, float(timeout_sec))) as r:
                return 200 <= int(getattr(r, "status", 200)) < 500
        except Exception:
            return False

    def select_transport_mode(self):
        mode = str(getattr(self, 'transport_mode_override', '') or CURRENT_CONFIG.get('transport_mode', TRANSPORT_MODE)).strip().lower()
        reason = "configured"

        if mode in {"online", "mesh", "reticulum_fallback"}:
            self.current_transport_mode = mode
            self.transport_last_reason = reason
            return mode

        # auto mode
        omni_health = f"{OMNI_BASE_URL}/health"
        omni_ok = self._http_ping(omni_health, timeout_sec=TRANSPORT_FAILOVER_TIMEOUT_SEC)

        mesh_ok = False
        if MESH_HEALTH_CHECK_URL:
            mesh_ok = self._http_ping(MESH_HEALTH_CHECK_URL, timeout_sec=TRANSPORT_FAILOVER_TIMEOUT_SEC)

        if mesh_ok:
            mode = "mesh"
            reason = "mesh-health-ok"
        elif omni_ok:
            mode = "online"
            reason = "omni-health-ok"
        elif RETICULUM_BRIDGE_ENDPOINT:
            mode = "reticulum_fallback"
            reason = "omni-health-failed"
        else:
            mode = "online"
            reason = "fallback-online-no-reticulum"

        self.current_transport_mode = mode
        self.transport_last_reason = reason
        return mode

    def reticulum_fallback_chat(self, user_text, messages):
        # Milestone G stub: replace with real Reticulum bridge call in later milestone.
        print(f"[RETICULUM_STUB] endpoint={RETICULUM_BRIDGE_ENDPOINT or 'unset'} user={user_text[:80]!r}", flush=True)
        return {
            "message": {
                "content": "Reticulum fallback is configured as a placeholder right now. Omni network path is unavailable; local fallback should engage automatically."
            }
        }

    def _omni_chat_once(self, model, messages):
        payload = {
            "messages": messages,
            "model": model or OMNI_MODEL or TEXT_MODEL,
        }
        req = urllib.request.Request(
            f"{OMNI_BASE_URL}/chat/completions",
            method="POST",
            data=json.dumps(payload).encode("utf-8"),
            headers=self._omni_headers(),
        )
        with urllib.request.urlopen(req, timeout=max(15, OMNI_REQUEST_TIMEOUT_SEC)) as r:
            data = json.loads(r.read().decode("utf-8", "ignore"))

        choices = data.get("choices") or []
        content = ""
        if choices:
            content = str(((choices[0] or {}).get("message") or {}).get("content") or "")
        if not content:
            content = str(data.get("output") or "")
        return {"message": {"content": content}}

    def _chunk_text_for_stream(self, content):
        chunks = []
        for part in re.split(r"(?<=[\.!\?])\s+", str(content or "")):
            part = part.strip()
            if not part:
                continue
            if len(part) <= max(20, OMNI_STREAM_CHUNK_CHARS):
                chunks.append({"message": {"content": part + (" " if not part.endswith((".", "!", "?")) else "")}})
                continue
            for i in range(0, len(part), max(20, OMNI_STREAM_CHUNK_CHARS)):
                sub = part[i:i + max(20, OMNI_STREAM_CHUNK_CHARS)]
                if sub:
                    chunks.append({"message": {"content": sub}})
        return chunks or [{"message": {"content": str(content or "")}}]

    def _local_vision_caption(self, user_text, img_path):
        try:
            vision_messages = [{
                "role": "user",
                "content": f"User asked: {user_text}\nDescribe this image in 2 short factual sentences for another assistant.",
                "images": [img_path],
            }]
            resp = ollama.chat(model=VISION_MODEL, messages=vision_messages, stream=False, options=OLLAMA_OPTIONS)
            return str((resp.get("message") or {}).get("content") or "").strip()
        except Exception as e:
            print(f"Vision caption fallback failed: {e}")
            return ""

    def _build_omni_messages(self, messages, img_path=None):
        if not img_path or OMNI_VISION_MODE != "hybrid":
            return messages
        user_text = ""
        if isinstance(messages, list) and messages:
            user_text = str((messages[-1] or {}).get("content") or "")
        caption = self._local_vision_caption(user_text, img_path)
        if not caption:
            return messages
        combined = f"{user_text}\n\nVisual context from camera: {caption}".strip()
        return [{"role": "user", "content": combined}]

    def llm_chat_stream(self, model, messages, img_path=None):
        if LLM_BACKEND != "omni":
            self.current_transport_mode = "online"
            return ollama.chat(model=model, messages=messages, stream=True, options=OLLAMA_OPTIONS)

        selected_mode = self.select_transport_mode()
        if selected_mode == "reticulum_fallback":
            last_user = str((messages[-1] or {}).get("content") or "") if isinstance(messages, list) and messages else ""
            one = self.reticulum_fallback_chat(last_user, messages)
            return self._chunk_text_for_stream(str((one.get("message") or {}).get("content") or ""))

        try:
            omni_messages = self._build_omni_messages(messages, img_path=img_path)
            one = self._omni_chat_once(model if not img_path else OMNI_MODEL, omni_messages)
            content = str((one.get("message") or {}).get("content") or "")
            if not content:
                return []
            return self._chunk_text_for_stream(content)
        except Exception as e:
            print(f"Omni stream error: {e}")
            if OMNI_FALLBACK_TO_OLLAMA:
                self.current_transport_mode = "reticulum_fallback"
                self.transport_last_reason = "omni-error->ollama"
                fallback_model = VISION_MODEL if img_path else TEXT_MODEL
                return ollama.chat(model=fallback_model, messages=messages, stream=True, options=OLLAMA_OPTIONS)
            raise

    def llm_chat_once(self, model, messages, img_path=None):
        if LLM_BACKEND != "omni":
            self.current_transport_mode = "online"
            return ollama.chat(model=model, messages=messages, stream=False, options=OLLAMA_OPTIONS)

        selected_mode = self.select_transport_mode()
        if selected_mode == "reticulum_fallback":
            last_user = str((messages[-1] or {}).get("content") or "") if isinstance(messages, list) and messages else ""
            return self.reticulum_fallback_chat(last_user, messages)

        try:
            omni_messages = self._build_omni_messages(messages, img_path=img_path)
            return self._omni_chat_once(model if not img_path else OMNI_MODEL, omni_messages)
        except Exception as e:
            print(f"Omni once error: {e}")
            if OMNI_FALLBACK_TO_OLLAMA:
                self.current_transport_mode = "reticulum_fallback"
                self.transport_last_reason = "omni-error->ollama"
                fallback_model = VISION_MODEL if img_path else TEXT_MODEL
                return ollama.chat(model=fallback_model, messages=messages, stream=False, options=OLLAMA_OPTIONS)
            raise

    def handle_transport_command(self, text):
        t = str(text or '').strip().lower()
        if not t:
            return None

        if t in {'/transport', 'transport', 'net', '/net'}:
            return self._transport_doctor_summary()

        m = re.match(r'^(?:/)?(?:transport|net)\s+(auto|online|mesh|reticulum_fallback|reticulum)$', t)
        if m:
            mode = m.group(1)
            if mode == 'reticulum':
                mode = 'reticulum_fallback'
            self.transport_mode_override = mode
            self.current_transport_mode = self.select_transport_mode()
            return f"Transport override set to {mode} (active: {self.current_transport_mode})."

        if t in {'/doctor', '/net-doctor', '/transport-doctor'}:
            return self._transport_doctor_summary()

        return None

    # =========================================================================
    # 5. CHAT & RESPOND
    # =========================================================================

    def chat_and_respond(self, text, img_path=None):
        if "forget everything" in text.lower() or "reset memory" in text.lower():
            self.session_memory = []
            self.permanent_memory = [{"role": "system", "content": SYSTEM_PROMPT}]
            self.save_chat_history()
            with self.tts_queue_lock: 
                self.tts_queue.append("Okay. Memory wiped.")
            self.set_state(BotStates.IDLE, "Memory Wiped")
            return

        if LLM_BACKEND == "omni":
            model_to_use = OMNI_MODEL
        else:
            model_to_use = VISION_MODEL if img_path else TEXT_MODEL
        self.set_state(BotStates.THINKING, "Thinking...", cam_path=img_path)
        
        messages = []
        if img_path:
            messages = [{"role": "user", "content": text, "images": [img_path]}]
        else:
            user_msg = {"role": "user", "content": text}
            messages = self.permanent_memory + self.session_memory + [user_msg]

        # Milestone H: manual transport commands / diagnostics in UI loop.
        if not img_path:
            transport_reply = self.handle_transport_command(text)
            if transport_reply:
                self.thinking_sound_active.clear()
                self.set_state(BotStates.SPEAKING, "Speaking...", cam_path=img_path)
                self.append_to_text("BOT: ", newline=False)
                self.append_to_text(transport_reply, newline=True)
                with self.tts_queue_lock:
                    self.tts_queue.append(transport_reply)
                self.session_memory.append({"role": "assistant", "content": transport_reply})
                self.wait_for_tts()
                self.set_state(BotStates.IDLE, "Ready")
                return

        # Milestone B: optional direct tool routing for Omni to reduce action-JSON dependence.
        if LLM_BACKEND == "omni" and not img_path and OMNI_TOOL_ROUTE_MODE in {"hybrid", "direct"}:
            direct_action = self.infer_direct_action(text)
            if direct_action:
                self.set_state(BotStates.THINKING, "Running action...", cam_path=img_path)
                tool_result = self.execute_action_and_get_result(direct_action)
                if self.respond_with_tool_result(tool_result, text, model_to_use, img_path=img_path):
                    return

        self.thinking_sound_active.set()
        threading.Thread(target=self._run_thinking_sound_loop, daemon=True).start()
        
        full_response_buffer = ""
        sentence_buffer = "" 
        
        try:
            stream = self.llm_chat_stream(model=model_to_use, messages=messages, img_path=img_path)
            
            is_action_mode = False
            
            for chunk in stream:
                if self.interrupted.is_set(): break 
                content = chunk['message']['content']
                full_response_buffer += content
                
                if '{"' in content or "action:" in content.lower():
                    is_action_mode = True
                    self.thinking_sound_active.clear()
                    continue 

                if is_action_mode: continue

                self.thinking_sound_active.clear()
                if self.current_state != BotStates.SPEAKING:
                    self.set_state(BotStates.SPEAKING, "Speaking...", cam_path=img_path)
                    self.append_to_text("BOT: ", newline=False)

                self._stream_to_text(content)
                
                sentence_buffer += content
                if any(punct in content for punct in ".!?\n"):
                    clean_sentence = sentence_buffer.strip()
                    if clean_sentence and re.search(r'[a-zA-Z0-9]', clean_sentence):
                        with self.tts_queue_lock: self.tts_queue.append(clean_sentence)
                    sentence_buffer = ""

            if is_action_mode:
                action_data = self.extract_json_from_text(full_response_buffer)
                if action_data:
                    tool_result = self.execute_action_and_get_result(action_data)
                    if self.respond_with_tool_result(tool_result, text, model_to_use, img_path=img_path):
                        return
            else:
                self.append_to_text("")
                self.session_memory.append({"role": "assistant", "content": full_response_buffer}) 
            
            self.wait_for_tts()
            self.set_state(BotStates.IDLE, "Ready")
                
        except Exception as e:
            print(f"LLM Error: {e}")
            self.set_state(BotStates.ERROR, "Brain Freeze!")

    def wait_for_tts(self):
        while self.tts_queue or self.tts_active.is_set():
            if self.interrupted.is_set(): break
            time.sleep(0.1)

    def _tts_worker(self):
        while True:
            text = None
            with self.tts_queue_lock:
                if self.tts_queue: 
                    text = self.tts_queue.pop(0)
                    self.tts_active.set() 
            if text: 
                self.speak(text)
                self.tts_active.clear() 
            else: time.sleep(0.05)

    def speak(self, text):
        clean = re.sub(r"[^\w\s,.!?:-]", "", text)
        if not clean.strip(): return
        
        print(f"[PIPER SPEAKING] '{clean}'", flush=True)
        voice_model = CURRENT_CONFIG.get("voice_model", "piper/en_GB-semaine-medium.onnx")
        
        try:
            self.current_audio_process = subprocess.Popen(
                ["./piper/piper", "--model", voice_model, "--output-raw"], 
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL
            )
            
            self.current_audio_process.stdin.write(clean.encode() + b'\n')
            self.current_audio_process.stdin.close() 

            try:
                device_info = sd.query_devices(kind='output')
                native_rate = int(device_info['default_samplerate'])
            except:
                native_rate = 48000 

            PIPER_RATE = 22050
            use_native_rate = False
            
            try:
                sd.check_output_settings(device=None, samplerate=PIPER_RATE)
            except:
                use_native_rate = True

            with sd.RawOutputStream(samplerate=native_rate if use_native_rate else PIPER_RATE, 
                                    channels=1, dtype='int16', 
                                    device=None, latency='low', blocksize=2048) as stream:
                while True:
                    if self.interrupted.is_set(): break
                    data = self.current_audio_process.stdout.read(4096)
                    if not data: break 
                    
                    audio_chunk = np.frombuffer(data, dtype=np.int16)
                    if len(audio_chunk) > 0:
                        self.current_volume = np.max(np.abs(audio_chunk))
                        if use_native_rate:
                            num_samples = int(len(audio_chunk) * (native_rate / PIPER_RATE))
                            audio_chunk = scipy.signal.resample(audio_chunk, num_samples).astype(np.int16)
                        stream.write(audio_chunk.tobytes())
                    else:
                        self.current_volume = 0
                time.sleep(max(0.0, TTS_TAIL_SEC)) 
                    
        except Exception as e:
            print(f"Audio Error: {e}")
        finally:
            self.current_volume = 0 
            if self.current_audio_process:
                if self.current_audio_process.stdout: self.current_audio_process.stdout.close()
                if self.current_audio_process.poll() is None: self.current_audio_process.terminate()
                self.current_audio_process = None

    def _run_thinking_sound_loop(self):
        time.sleep(max(0.0, THINKING_SOUND_INITIAL_DELAY_SEC))
        while self.thinking_sound_active.is_set():
            sound = self.get_random_sound(thinking_sounds_dir)
            if sound: self.play_sound(sound)
            for _ in range(50):
                if not self.thinking_sound_active.is_set(): return
                time.sleep(0.1)

    def get_random_sound(self, directory):
        if os.path.exists(directory):
            files = [f for f in os.listdir(directory) if f.endswith(".wav")]
            return os.path.join(directory, random.choice(files)) if files else None
        return None

    def play_sound(self, file_path):
        if not file_path or not os.path.exists(file_path): return
        try:
            with wave.open(file_path, 'rb') as wf:
                file_sr = wf.getframerate()
                data = wf.readframes(wf.getnframes())
                audio = np.frombuffer(data, dtype=np.int16)

            try:
                device_info = sd.query_devices(kind='output')
                native_rate = int(device_info['default_samplerate'])
            except:
                native_rate = 48000 

            playback_rate = file_sr
            try:
                sd.check_output_settings(device=None, samplerate=file_sr)
            except:
                playback_rate = native_rate
                num_samples = int(len(audio) * (native_rate / file_sr))
                audio = scipy.signal.resample(audio, num_samples).astype(np.int16)

            sd.play(audio, playback_rate)
            sd.wait() 
        except: pass

    def load_chat_history(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f: return json.load(f)
            except: pass
        return [{"role": "system", "content": SYSTEM_PROMPT}]

    def save_chat_history(self):
        full = self.permanent_memory + self.session_memory
        conv = full[1:]
        if len(conv) > 10: conv = conv[-10:]
        with open(MEMORY_FILE, "w") as f: 
            json.dump([full[0]] + conv, f, indent=4)

if __name__ == "__main__":
    print("--- SYSTEM STARTING ---", flush=True)
    root = tk.Tk()
    app = BotGUI(root)
    root.mainloop()
