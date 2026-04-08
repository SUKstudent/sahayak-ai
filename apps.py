import streamlit as st
from gtts import gTTS
import io

# Optional voice input
try:
    import speech_recognition as sr
    VOICE_ENABLED = True
except ImportError:
    VOICE_ENABLED = False

# ---------------- Session ----------------
if "page" not in st.session_state:
    st.session_state.page = "language"
if "language" not in st.session_state:
    st.session_state.language = "en"
if "choice" not in st.session_state:
    st.session_state.choice = None

# ---------------- Helper Functions ----------------
def go_to_page(page_name):
    st.session_state.page = page_name
    st.experimental_rerun()

def generate_audio(text, lang):
    tts = gTTS(text=text, lang=lang)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

def speak(text):
    audio = generate_audio(text, st.session_state.language)
    st.audio(audio, format="audio/mp3")

def get_recommendation(choice, lang):
    data = {
        "en": {
            "dry": ("Ragi, Jowar, Bajra", "Goat, Poultry", "Ghee, Oil"),
            "dairy": ("Fodder Crops", "Milk, Paneer", "Ghee, Butter"),
            "fish": ("Water Plants", "Fish Farming", "Fish Products")
        },
        "hi": {
            "dry": ("रागी, ज्वार, बाजरा", "बकरी, मुर्गी", "घी, तेल"),
            "dairy": ("चारे की फसलें", "दूध, पनीर", "घी, मक्खन"),
            "fish": ("जल पौधे", "मछली पालन", "मछली उत्पाद")
        },
        "kn": {
            "dry": ("ರಾಗಿ, ಜೋಳ, ಜೋವಾರ", "ಆಡು, ಕೋಳಿ", "ತುಪ್ಪ, ಎಣ್ಣೆ"),
            "dairy": ("ಚಾರೆ ಬೆಳೆಗಳು", "ಹಾಲು, ಪನ್ನೀರ್", "ತುಪ್ಪ, ಬೆಣ್ಣೆ"),
            "fish": ("ನೀರಿನ ಸಸ್ಯಗಳು", "ಮೀನುಗಾರಿಕೆ", "ಮೀನು ಉತ್ಪನ್ನಗಳು")
        }
    }
    return data[lang][choice]

# ---------------- UI ----------------
# 1️⃣ Language Selection
if st.session_state.page == "language":
    st.title("🌾 Sahayak AI")
    st.subheader("Select Language")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🇬🇧"):
            st.session_state.language = "en"
            go_to_page("welcome")
    with col2:
        if st.button("🇮🇳"):
            st.session_state.language = "hi"
            go_to_page("welcome")
    with col3:
        if st.button("🏴"):
            st.session_state.language = "kn"
            go_to_page("welcome")

# 2️⃣ Welcome Page
elif st.session_state.page == "welcome":
    lang = st.session_state.language
    titles = {"en": "🌾 Welcome", "hi": "🌾 स्वागत है", "kn": "🌾 ಸುಸ್ವಾಗತ"}
    descriptions = {
        "en": "Your assistant for resilient crops & extra income",
        "hi": "आपका सहायक – फसल और अतिरिक्त आय",
        "kn": "ನಿಮ್ಮ ಸಹಾಯಕ – ಬೆಳೆ ಮತ್ತು ಹೆಚ್ಚುವರಿ ಆದಾಯ"
    }
    st.image("https://i.imgur.com/6Iej2c3.png", use_column_width=True)  # placeholder farm image
    st.title(titles[lang])
    speak(descriptions[lang])
    if st.button("➡️"):
        go_to_page("farm_type")

# 3️⃣ Farm Type Selection
elif st.session_state.page == "farm_type":
    lang = st.session_state.language
    st.subheader("Select Farm Type")
    speak({"en": "Choose your farm type: Dry Land, Dairy, or Fish",
           "hi": "अपना फ़ार्म प्रकार चुनें: ड्रा लैंड, डेयरी, या मछली",
           "kn": "ನಿಮ್ಮ ಫಾರ್ಮ್ ಪ್ರಕಾರ ಆಯ್ಕೆಮಾಡಿ: ಡ್ರೈ ಲ್ಯಾಂಡ್, ಡೇರಿ, ಅಥವಾ ಮೀನು"}[lang])
    
    # Voice Input
    if VOICE_ENABLED:
        st.write("🎤 Speak your farm type (Dry Land, Dairy, Fish)")
        audio_file = st.file_uploader("Upload voice (wav/mp3)", type=["wav","mp3"])
        if audio_file:
            r = sr.Recognizer()
            with sr.AudioFile(audio_file) as source:
                audio_data = r.record(source)
                try:
                    text = r.recognize_google(audio_data, language={"en":"en-US","hi":"hi-IN","kn":"kn-IN"}[lang])
                    st.write(f"You said: {text}")
                    if any(word in text.lower() for word in ["dry","रागी","ರಾಗಿ"]):
                        st.session_state.choice = "dry"
                    elif any(word in text.lower() for word in ["dairy","दूध","ಹಾಲು"]):
                        st.session_state.choice = "dairy"
                    elif any(word in text.lower() for word in ["fish","मछली","ಮೀನು"]):
                        st.session_state.choice = "fish"
                    if st.session_state.choice:
                        go_to_page("recommendation")
                except:
                    st.error("Could not recognize speech. Please use icons below.")
    
    # Icon Buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏜️"):
            st.session_state.choice = "dry"
            go_to_page("recommendation")
    with col2:
        if st.button("🐄"):
            st.session_state.choice = "dairy"
            go_to_page("recommendation")
    with col3:
        if st.button("🐟"):
            st.session_state.choice = "fish"
            go_to_page("recommendation")

# 4️⃣ Recommendation Page
elif st.session_state.page == "recommendation":
    lang = st.session_state.language
    if not st.session_state.choice:
        go_to_page("farm_type")
    
    crops, income, value = get_recommendation(st.session_state.choice, lang)
    
    st.subheader("🌱 Crops")
    st.image("https://i.imgur.com/1RZfJwI.png", caption=crops, use_column_width=True)
    st.subheader("💰 Livestock / Income")
    st.image("https://i.imgur.com/3QzQ0kj.png", caption=income, use_column_width=True)
    st.subheader("🔄 Value Addition")
    st.image("https://i.imgur.com/xZl4a4G.png", caption=value, use_column_width=True)
    
    speak(f"Crops: {crops}. Income: {income}. Value Addition: {value}")
    
    if st.button("🏠"):
        go_to_page("welcome")
