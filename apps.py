import streamlit as st
import base64
from gtts import gTTS
import io
from pydantic import BaseModel

# ------------------ Backend logic ------------------
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
    """Convert text to audio and return base64"""
    tts = gTTS(text=text, lang=lang)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return base64.b64encode(audio_bytes.read()).decode()

def recommend(data: RequestData):
    crops, income, value = get_plan(data.choice, data.language)
    audio = speak(f"{crops}. {income}. {value}", data.language)
    return {
        "crops": crops,
        "income": income,
        "value_addition": value,
        "audio": audio
    }

def speak_instruction(text, lang):
    """Play instruction audio in Streamlit"""
    audio_bytes = base64.b64decode(speak(text, lang))
    st.audio(audio_bytes, format="audio/mp3")

# ------------------ Frontend (Streamlit) ------------------
st.set_page_config(page_title="🌾 Sahayak AI", layout="wide")

st.title("🌾 Sahayak AI - Climate Resilient Livelihood Planner")
st.subheader("Krishi Mitra – Assistant")

# --- Language Selection ---
lang_option = st.selectbox("Select Language / भाषा / ಭಾಷೆ", ["English", "Hindi", "Kannada"])
lang_map = {"English": "en", "Hindi": "hi", "Kannada": "kn"}
language = lang_map[lang_option]

# Play instruction
if st.button("🔊 Play Instructions"):
    speak_instruction({
        "en": "Select your farm type below. Then click on the recommended crop to hear advice.",
        "hi": "नीचे अपने फार्म का प्रकार चुनें। फिर सलाह सुनने के लिए अनुशंसित फसल पर क्लिक करें।",
        "kn": "ಕೆಳಗಿನ ನಿಮ್ಮ ಫಾರ್ಮ್ ಪ್ರಕಾರವನ್ನು ಆರಿಸಿ. ನಂತರ ಸಲಹೆಯನ್ನು ಕೇಳಲು ಶಿಫಾರಸು ಮಾಡಿದ ಬೆಳೆಯನ್ನು ಕ್ಲಿಕ್ ಮಾಡಿ."
    }[language], language)

st.markdown("### Select Farm Type")

col1, col2, col3 = st.columns(3)

choice = None
with col1:
    if st.button("🏜️ Dry Land", key="dry"):
        choice = "dry"
with col2:
    if st.button("🐄 Dairy", key="dairy"):
        choice = "dairy"
with col3:
    if st.button("🐟 Fish", key="fish"):
        choice = "fish"

if choice:
    try:
        data = recommend(RequestData(choice=choice, language=language))

        st.success("✅ Recommendation Ready")

        # Show results with big font for readability
        st.markdown(f"### 🌱 Crops: {data['crops']}")
        st.markdown(f"### 💰 Income: {data['income']}")
        st.markdown(f"### 🔄 Value Addition: {data['value_addition']}")

        # Play recommendation audio
        st.audio(base64.b64decode(data["audio"]), format="audio/mp3")

        # Optional: repeat instruction button
        if st.button("🔊 Play Advice Again"):
            st.audio(base64.b64decode(data["audio"]), format="audio/mp3")

    except Exception as e:
        st.error(f"⚠️ Failed to get recommendation: {e}")

# Footer
st.markdown("---")
st.markdown("🌾 Sahayak AI helps farmers get drought-resilient crops and secondary income options in multiple languages.")
