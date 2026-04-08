import streamlit as st
import requests
import base64
import threading
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
import io
import uvicorn

# --------------- Backend (FastAPI) -------------------

app = FastAPI(title="Sahayak AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    choice: str
    language: str

def get_plan(choice, lang):
    if lang == "kn":
        if choice == "dry":
            return "ರಾಗಿ, ಜೋಳ, ಜೋವಾರ", "ಆಡು, ಕೋಳಿ", "ತುಪ್ಪ, ಎಣ್ಣೆ"
        elif choice == "dairy":
            return "ಚಾರೆ ಬೆಳೆಗಳು", "ಹಾಲು, ಪನ್ನೀರ್", "ತುಪ್ಪ, ಬೆಣ್ಣೆ"
        elif choice == "fish":
            return "ನೀರಿನ ಸಸ್ಯಗಳು", "ಮೀನುಗಾರಿಕೆ", "ಮೀನು ಉತ್ಪನ್ನಗಳು"
    elif lang == "hi":
        if choice == "dry":
            return "रागी, ज्वार, बाजरा", "बकरी, मुर्गी", "घी, तेल"
        elif choice == "dairy":
            return "चारे की फसलें", "दूध, पनीर", "घी, मक्खन"
        elif choice == "fish":
            return "जल पौधे", "मछली पालन", "मछली उत्पाद"
    else:  # English
        if choice == "dry":
            return "Ragi, Jowar, Bajra", "Goat, Poultry", "Ghee, Oil"
        elif choice == "dairy":
            return "Fodder Crops", "Milk, Paneer", "Ghee, Butter"
        elif choice == "fish":
            return "Water Plants", "Fish Farming", "Fish Products"
    return "", "", ""

def speak(text, lang):
    tts = gTTS(text=text, lang=lang)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return base64.b64encode(audio_bytes.read()).decode()

@app.post("/recommend")
def recommend(data: RequestData):
    crops, income, value = get_plan(data.choice, data.language)
    audio = speak(f"{crops}. {income}. {value}", data.language)
    return {
        "crops": crops,
        "income": income,
        "value_addition": value,
        "audio": audio
    }

# Run FastAPI in a separate thread inside Streamlit app
def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")

api_thread = threading.Thread(target=run_api, daemon=True)
api_thread.start()

# --------------- Frontend (Streamlit) -------------------

st.set_page_config(page_title="🌾 Sahayak AI", layout="wide")

st.title("🌾 Sahayak AI - Climate Resilient Livelihood Planner")
st.subheader("Krishi Mitra – Assistant")

lang_option = st.selectbox("Select Language / भाषा / ಭಾಷೆ", ["English", "Hindi", "Kannada"])
lang_map = {"English": "en", "Hindi": "hi", "Kannada": "kn"}
language = lang_map[lang_option]

st.markdown("### Select Farm Type")

col1, col2, col3 = st.columns(3)

choice = None
with col1:
    if st.button("🏜️ Dry Land"):
        choice = "dry"
with col2:
    if st.button("🐄 Dairy"):
        choice = "dairy"
with col3:
    if st.button("🐟 Fish"):
        choice = "fish"

if choice:
    try:
        response = requests.post(
            "http://localhost:8000/recommend",
            json={"choice": choice, "language": language},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        st.success("✅ Recommendation Ready")

        st.write(f"### 🌱 Crops: {data['crops']}")
        st.write(f"### 💰 Income: {data['income']}")
        st.write(f"### 🔄 Value Addition: {data['value_addition']}")

        audio_bytes = base64.b64decode(data["audio"])
        st.audio(audio_bytes, format="audio/mp3")

    except Exception as e:
        st.error(f"⚠️ Failed to get recommendation: {e}")
