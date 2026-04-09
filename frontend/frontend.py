import streamlit as st
import requests
import base64
from gtts import gTTS
import io

st.set_page_config(page_title="🌾 ಸಹಾಯಕ AI", layout="wide")

API_URL = "https://your-backend-url/recommend"

def speak(text):
    tts = gTTS(text=text, lang="kn")
    audio = io.BytesIO()
    tts.write_to_fp(audio)
    audio.seek(0)
    st.audio(audio.read(), format="audio/mp3")

def play_audio(b64):
    st.audio(base64.b64decode(b64), format="audio/mp3")

st.markdown("<h1 style='text-align:center;'>🌾 ಸಹಾಯಕ AI</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>ಉತ್ತರ ಕರ್ನಾಟಕ ರೈತರಿಗಾಗಿ</h4>", unsafe_allow_html=True)

if "step" not in st.session_state:
    st.session_state.step = 1

# STEP 1
if st.session_state.step == 1:
    speak("ನಿಮ್ಮ ಕೃಷಿ ಪ್ರಕಾರವನ್ನು ಆಯ್ಕೆಮಾಡಿ")

    col1, col2, col3 = st.columns(3)

    if col1.button("🏜️ ಒಣಭೂಮಿ"):
        st.session_state.farm = "dry"
        st.session_state.step = 2

    if col2.button("🐄 ಹಾಲುಗಾರಿಕೆ"):
        st.session_state.farm = "dairy"
        st.session_state.step = 2

    if col3.button("🐟 ಮೀನುಗಾರಿಕೆ"):
        st.session_state.farm = "fish"
        st.session_state.step = 2

# STEP 2
elif st.session_state.step == 2:
    speak("ನೀರಿನ ಲಭ್ಯತೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ")

    col1, col2, col3 = st.columns(3)

    if col1.button("🔴 ಕಡಿಮೆ"):
        st.session_state.water = "low"
        st.session_state.step = 3

    if col2.button("🟡 ಮಧ್ಯಮ"):
        st.session_state.water = "medium"
        st.session_state.step = 3

    if col3.button("🟢 ಹೆಚ್ಚು"):
        st.session_state.water = "high"
        st.session_state.step = 3

# STEP 3
elif st.session_state.step == 3:
    speak("ನಿಮ್ಮ ಕೃಷಿ ಯೋಜನೆ ತಯಾರಾಗುತ್ತಿದೆ")

    res = requests.post(API_URL, json={
        "farm_type": st.session_state.farm,
        "farm_size": 1.0,
        "water_availability": st.session_state.water
    }).json()

    speak("ಯೋಜನೆ ಸಿದ್ಧವಾಗಿದೆ")

    st.success("✅")

    st.markdown("### 🌱 ಮುಖ್ಯ ಬೆಳೆಗಳು")
    st.write(", ".join(res["main_crops"]))
    st.write(res["main_income"])

    st.markdown("### 💰 ಹೆಚ್ಚುವರಿ ಆದಾಯ")
    for i in res["secondary_income"]:
        st.write(i)

    st.markdown("### 🏛️ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು")
    for s in res["schemes"]:
        st.write(s)

    play_audio(res["audio"])

    if st.button("🔁 ಪುನರಾರಂಭ"):
        st.session_state.step = 1