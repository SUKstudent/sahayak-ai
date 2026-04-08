from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
import io
import base64
import uvicorn

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
    plans = {
        "kn": {
            "dry": ("ರಾಗಿ, ಜೋಳ, ಜೋವಾರ", "ಆಡು, ಕೋಳಿ", "ತುಪ್ಪ, ಎಣ್ಣೆ"),
            "dairy": ("ಚಾರೆ ಬೆಳೆಗಳು", "ಹಾಲು, ಪನ್ನೀರ್", "ತುಪ್ಪ, ಬೆಣ್ಣೆ"),
            "fish": ("ನೀರಿನ ಸಸ್ಯಗಳು", "ಮೀನುಗಾರಿಕೆ", "ಮೀನು ಉತ್ಪನ್ನಗಳು")
        },
        "hi": {
            "dry": ("रागी, ज्वार, बाजरा", "बकरी, मुर्गी", "घी, तेल"),
            "dairy": ("चारे की फसलें", "दूध, पनीर", "घी, मक्खन"),
            "fish": ("जल पौधे", "मछली पालन", "मछली उत्पाद")
        },
        "en": {
            "dry": ("Ragi, Jowar, Bajra", "Goat, Poultry", "Ghee, Oil"),
            "dairy": ("Fodder Crops", "Milk, Paneer", "Ghee, Butter"),
            "fish": ("Water Plants", "Fish Farming", "Fish Products")
        }
    }
    return plans.get(lang, plans["en"]).get(choice, ("", "", ""))

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
    return {"crops": crops, "income": income, "value_addition": value, "audio": audio}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
