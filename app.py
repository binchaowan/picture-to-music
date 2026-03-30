{\rtf1\ansi\ansicpg950\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import numpy as np\
from PIL import Image\
import io\
import base64\
import time\
\
# \uc0\u31777 \u21934 \u38899 \u27138 \u29983 \u25104 \u20989 \u25976 \u65288 \u29983 \u25104 \u32004 30\u31186  WAV \u26684 \u24335 \u26032 \u21476 \u20856 \u39080 \u26684 \u38899 \u27138 \u65289 \
def generate_neoclassical_music(prompt: str, duration_sec: int = 30, sample_rate: int = 44100):\
    np.random.seed(42)  # \uc0\u22266 \u23450 \u31278 \u23376 \u65292 \u20196 \u21516 \u19968  prompt \u27599 \u27425 \u32893 \u33853 \u39006 \u20284 \
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), False)\
    \
    # \uc0\u26681 \u25818  prompt \u31777 \u21934 \u26144 \u23556 \u21443 \u25976 \u65288 \u20320 \u21487 \u20197 \u20877 \u25844 \u20805 \u65289 \
    mood = "calm" if any(word in prompt.lower() for word in ["calm", "peace", "soft", "serene"]) else "dramatic"\
    \
    # \uc0\u20027 \u26059 \u24459 \u38971 \u29575 \u65288 \u26032 \u21476 \u20856 \u39080 \u26684 \u65306 \u20302 \u27785 \u37628 \u29748  + \u39640 \u38899 \u24358 \u27138 \u24863 \u65289 \
    base_freq = 220 if mood == "calm" else 330  # A3 \uc0\u25110  E4 \u38468 \u36817 \
    \
    # \uc0\u29983 \u25104 \u22810 \u23652 \u32882 \u38899 \
    audio = np.zeros_like(t)\
    \
    # Layer 1: \uc0\u20302 \u27785 \u25345 \u32396 \u21644 \u24358 \u65288 \u20687 \u37628 \u29748 \u20302 \u38899 \u65289 \
    for f in [base_freq, base_freq * 1.5, base_freq * 2]:\
        audio += 0.3 * np.sin(2 * np.pi * f * t) * np.exp(-t / 8)  # \uc0\u36629 \u24494 \u34928 \u28187 \
    \
    # Layer 2: \uc0\u32233 \u24930 \u26059 \u24459 \u65288 \u26032 \u21476 \u20856 \u27969 \u26274 \u32218 \u26781 \u65289 \
    melody_freqs = [base_freq * 2, base_freq * 2.5, base_freq * 3, base_freq * 4]\
    for i, f in enumerate(melody_freqs):\
        phase = i * 0.5\
        audio += 0.2 * np.sin(2 * np.pi * f * t * (1 + 0.01 * np.sin(2 * np.pi * 0.2 * t)))  # \uc0\u36629 \u24494  vibrato\
    \
    # Layer 3: \uc0\u39640 \u38899 \u40670 \u32180 \u65288 \u20687 \u35918 \u29748 \u25110 \u36629 \u24358 \u27138 \u65289 \
    audio += 0.15 * np.sin(2 * np.pi * (base_freq * 8) * t) * (np.sin(2 * np.pi * 0.8 * t) > 0).astype(float)\
    \
    # \uc0\u27491 \u35215 \u21270  + \u36629 \u24494  reverb \u27169 \u25836 \
    audio = audio / np.max(np.abs(audio)) * 0.8\
    # \uc0\u31777 \u21934  fade in/out\
    fade = np.linspace(0, 1, int(sample_rate * 2))\
    audio[:len(fade)] *= fade\
    audio[-len(fade):] *= fade[::-1]\
    \
    # \uc0\u36681 \u25104  WAV bytes\
    audio_int16 = np.int16(audio * 32767)\
    wav_bytes = io.BytesIO()\
    # \uc0\u25163 \u21205 \u23531 \u31777 \u21934  WAV header\u65288 \u25110 \u29992  scipy.io.wavfile\u65292 \u20294 \u28858 \u31777 \u21270 \u29992  numpy to bytes\u65289 \
    from scipy.io.wavfile import write\
    write(wav_bytes, sample_rate, audio_int16)\
    wav_bytes.seek(0)\
    return wav_bytes\
\
# \uc0\u20998 \u26512 \u22294 \u29255 \u29305 \u33394 \u20006 \u29983 \u25104  prompt\
def analyze_image_and_create_prompt(image: Image.Image) -> str:\
    # \uc0\u36681  numpy array\
    img_array = np.array(image.convert("RGB"))\
    \
    # \uc0\u22522 \u26412 \u29305 \u33394 \u20998 \u26512 \
    avg_color = np.mean(img_array, axis=(0,1)).astype(int)  # \uc0\u24179 \u22343  RGB\
    brightness = np.mean(img_array) / 255.0\
    contrast = np.std(img_array) / 255.0\
    \
    # \uc0\u20027 \u33394 \u35519 \u21028 \u26039 \u65288 \u31777 \u21934 \u65289 \
    dominant = np.argmax(avg_color)\
    color_name = ["red", "green", "blue"][dominant]\
    \
    # \uc0\u27675 \u22285 \u25551 \u36848 \
    if brightness > 0.7:\
        mood = "bright, serene, uplifting"\
    elif brightness < 0.4:\
        mood = "dark, mysterious, melancholic"\
    else:\
        mood = "balanced, peaceful"\
    \
    if contrast > 0.25:\
        mood += ", dramatic with strong emotions"\
    \
    prompt = f"A beautiful neoclassical instrumental piano and strings piece inspired by a \{mood\} photograph with dominant \{color_name\} tones, soft flowing melodies, gentle arpeggios, emotional depth, around 30 seconds long, pure instrumental, no vocals."\
    \
    return prompt, \{\
        "avg_color": avg_color.tolist(),\
        "brightness": round(brightness, 2),\
        "contrast": round(contrast, 2),\
        "mood": mood\
    \}\
\
# Streamlit UI\
st.set_page_config(page_title="\uc0\u29031 \u29255 \u36681 \u26032 \u21476 \u20856 \u38899 \u27138 ", page_icon="\u55356 \u57273 ", layout="centered")\
\
st.title("\uc0\u55357 \u56568  \u29031 \u29255 \u36681 \u26032 \u21476 \u20856 \u32020 \u38899 \u27138 ")\
st.markdown("\uc0\u19978 \u20659 \u19968 \u24373 \u29031 \u29255 \u65292 \u25105 \u26371 \u20998 \u26512 \u20322 \u22021 \u38991 \u33394 \u12289 \u20142 \u24230 \u21516 \u27675 \u22285 \u65292 \u28982 \u24460 \u29983 \u25104 \u19968 \u27573 \u32004  **30 \u31186 ** \u26032 \u21476 \u20856 \u39080 \u26684 \u32020 \u38899 \u27138 \u65288 \u37628 \u29748  + \u24358 \u27138 \u28858 \u20027 \u65289 \u12290 ")\
\
uploaded_file = st.file_uploader("\uc0\u19978 \u20659 \u29031 \u29255 \u65288 JPG / PNG\u65289 ", type=["jpg", "jpeg", "png"])\
\
if uploaded_file is not None:\
    image = Image.open(uploaded_file)\
    st.image(image, caption="\uc0\u20320 \u19978 \u20659 \u22021 \u29031 \u29255 ", use_column_width=True)\
    \
    with st.spinner("\uc0\u20998 \u26512 \u29031 \u29255 \u29305 \u33394 \u20006 \u29983 \u25104 \u38899 \u27138 \u20013 ...\u65288 \u32004  10-20 \u31186 \u65289 "):\
        prompt, stats = analyze_image_and_create_prompt(image)\
        \
        st.subheader("\uc0\u29031 \u29255 \u20998 \u26512 \u32080 \u26524 ")\
        st.json(stats)\
        st.caption(f"\uc0\u29983 \u25104 \u25552 \u31034 \u35422 \u65288 \u20839 \u37096 \u20351 \u29992 \u65289 \u65306 \\n\{prompt\}")\
        \
        # \uc0\u29983 \u25104 \u38899 \u27138 \
        audio_bytes = generate_neoclassical_music(prompt, duration_sec=30)\
        \
        st.success("\uc0\u38899 \u27138 \u29983 \u25104 \u23436 \u25104 \u65281 ")\
        st.audio(audio_bytes, format="audio/wav")\
        \
        # \uc0\u19979 \u36617 \u25353 \u37397 \
        st.download_button(\
            label="\uc0\u19979 \u36617 \u38899 \u27138 \u65288 WAV \u26684 \u24335 \u65289 ",\
            data=audio_bytes,\
            file_name="neoclassical_from_photo.wav",\
            mime="audio/wav"\
        )\
        \
        st.info("\uc0\u21602 \u27573 \u38899 \u27138 \u20418 \u26681 \u25818 \u29031 \u29255 \u29305 \u33394  procedural \u29983 \u25104 \u65292 \u39080 \u26684 \u20670 \u21521 \u26032 \u21476 \u20856 \u65288 \u26580 \u21644 \u12289 \u24773 \u24863 \u35920 \u23500 \u65289 \u12290 \u24819 \u26356 \u30495 \u23526  AI \u38899 \u27138 \u65292 \u21487 \u20197 \u20043 \u24460 \u21152  Suno/Udio \u31561  API\u12290 ")\
\
st.markdown("---")\
st.caption("\uc0\u29992  Python + Streamlit \u38283 \u30332  \'95 \u32020 \u38899 \u27138 \u29983 \u25104  \'95 \u20219 \u20309 \u20154 \u37117 \u21487 \u20197  deploy \u21040 \u20114 \u32879 \u32178 ")}