from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
import io
import base64

app = FastAPI(title="Sahayak AI - North Karnataka")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    farm_type: str
    farm_size: float
    water_availability: str

# 🌾 North Karnataka crops
main_crops = {
    "dry": ["ರಾಗಿ (Ragi)", "ಜೋಳ (Jowar)", "ಸಜ್ಜೆ (Bajra)"],
    "dairy": ["ಮೇವು ಬೆಳೆಗಳು (Fodder Crops)"],
    "fish": ["ನೀರಿನ ಸಸ್ಯಗಳು (Water Plants)"]
}

# 💰 Local income options
secondary_options = {
    "dry": [
        ("ಮೇಡ ಸಾಕಣೆ (Goat Rearing)", 15000, 40000),
        ("ಜೋಳ ಹಿಟ್ಟು ಉತ್ಪಾದನೆ (Millet Flour)", 5000, 15000),
        ("ಸೇಂದ್ರೀಯ ಗೊಬ್ಬರ ಮಾರಾಟ (Compost)", 3000, 10000)
    ],
    "dairy": [
        ("ತುಪ್ಪ ತಯಾರಿ (Ghee Production)", 15000, 40000),
        ("ಪನೀರ್ ತಯಾರಿ (Paneer)", 10000, 30000),
        ("ಕೊಳಿ ಸಾಕಣೆ (Poultry)", 10000, 25000)
    ],
    "fish": [
        ("ಮೀನು ಪ್ರಕ್ರಿಯೆ (Fish Processing)", 15000, 40000),
        ("ನೀರು ಸಸ್ಯ ಕೃಷಿ (Water Plants)", 5000, 15000)
    ]
}

def speak(text):
    tts = gTTS(text=text, lang="kn")
    audio = io.BytesIO()
    tts.write_to_fp(audio)
    audio.seek(0)
    return base64.b64encode(audio.read()).decode()

@app.get("/")
def root():
    return {"message": "Sahayak AI North Karnataka Running 🚀"}

@app.post("/recommend")
def recommend(data: RequestData):

    crops = main_crops.get(data.farm_type, [])

    options = secondary_options.get(data.farm_type, [])[:2]

    sec_list = []
    sec_text = []

    for name, low, high in options:
        income = f"₹{low} - ₹{high}"
        sec_list.append(f"{name} ({income})")
        sec_text.append(f"{name} {income}")

    main_income = "₹30,000 - ₹70,000"

    # Kannada audio
    audio_text = f"ಮುಖ್ಯ ಬೆಳೆಗಳು {', '.join(crops)}. ಅಂದಾಜು ಆದಾಯ {main_income}. ಹೆಚ್ಚುವರಿ ಆದಾಯ ಮಾರ್ಗಗಳು {', '.join(sec_text)}"

    audio = speak(audio_text)

    schemes = [
        "ಪ್ರಧಾನಮಂತ್ರಿ ಫಸಲ್ ಬಿಮಾ ಯೋಜನೆ",
        "ಮತ್ಸ್ಯ ಸಂಪದ ಯೋಜನೆ",
        "ರಾಷ್ಟ್ರೀಯ ಪಶುಸಂಗೋಪನಾ ಮಿಷನ್"
    ]

    return {
        "main_crops": crops,
        "main_income": main_income,
        "secondary_income": sec_list,
        "schemes": schemes,
        "audio": audio
    }