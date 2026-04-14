from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import io
import json
import random
import numpy as np
from PIL import Image
import uvicorn

app = FastAPI(title="Sahayak AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== DATA ==========
CROPS = {
    "low": [
        {"name": "Jowar (Millet)", "name_kn": "ಜೋಳ", "roi": 4, "profit": 15000},
        {"name": "Ragi", "name_kn": "ರಾಗಿ", "roi": 4, "profit": 18000},
        {"name": "Tur Dal", "name_kn": "ತೂರ್ ದಾಳ್", "roi": 6, "profit": 22000},
    ],
    "moderate": [
        {"name": "Cotton", "name_kn": "ಹತ್ತಿ", "roi": 6, "profit": 35000},
        {"name": "Maize", "name_kn": "ಮೆಕ್ಕೆಜೋಳ", "roi": 3, "profit": 25000},
    ],
    "high": [
        {"name": "Sugarcane", "name_kn": "ಕಬ್ಬು", "roi": 12, "profit": 80000},
    ]
}

LIVESTOCK = {
    "low": [
        {"name": "Goat Rearing", "name_kn": "ಮೇಕೆ ಸಾಕಣೆ", "setup": 10000, "monthly": 3000},
        {"name": "Beekeeping", "name_kn": "ಜೇನು ಸಾಕಣೆ", "setup": 12000, "monthly": 4000},
    ],
    "moderate": [
        {"name": "Dairy", "name_kn": "ಹೈನುಗಾರಿಕೆ", "setup": 60000, "monthly": 8000},
    ]
}

SKILLS = {
    "bidri": {"name": "Bidri Work", "name_kn": "ಬಿದ್ರಿ ಕೆಲಸ", "setup": 5000, "monthly": 5000},
    "kasuti": {"name": "Kasuti Embroidery", "name_kn": "ಕಸೂತಿ", "setup": 1000, "monthly": 2500},
    "diya": {"name": "Diya Making", "name_kn": "ದೀಪ ಮಾಡುವುದು", "setup": 3000, "monthly": 7500},
    "pickle": {"name": "Pickle Making", "name_kn": "ಉಪ್ಪಿನಕಾಯಿ", "setup": 5000, "monthly": 10000}
}

SCHEMES = [
    {"name": "PMEGP", "name_kn": "ಪಿಎಂಇಜಿಪಿ", "subsidy": "35%"},
    {"name": "NABARD SHG", "name_kn": "ನಬಾರ್ಡ್", "subsidy": "Loans"},
    {"name": "KVIC Craft", "name_kn": "ಕೆವಿಐಸಿ", "subsidy": "40%"},
]

SOIL_TYPES = {
    "red": {"name": "Red Soil", "name_kn": "ಕೆಂಪು ಮಣ್ಣು", "water": "low"},
    "black": {"name": "Black Soil", "name_kn": "ಕಪ್ಪು ಮಣ್ಣು", "water": "high"},
    "laterite": {"name": "Laterite", "name_kn": "ಲ್ಯಾಟರೈಟ್", "water": "moderate"},
    "alluvial": {"name": "Alluvial", "name_kn": "ಮೆಕ್ಕಲು", "water": "moderate"},
}

class FarmerRequest(BaseModel):
    land_acres: float
    water: str
    budget: float
    skills: List[str] = []
    language: str = "english"

@app.get("/")
async def root():
    return {"message": "Sahayak AI is running!", "status": "ready"}

@app.post("/api/recommend")
async def get_recommendations(request: FarmerRequest):
    water = request.water
    lang = request.language
    
    crops = CROPS.get(water, CROPS["low"])[:3]
    for c in crops:
        c["display_name"] = c["name_kn"] if lang == "kannada" else c["name"]
    
    if water == "low":
        livestock = LIVESTOCK["low"][:2]
    else:
        livestock = LIVESTOCK["low"][:1] + LIVESTOCK["moderate"][:1]
    for l in livestock:
        l["display_name"] = l["name_kn"] if lang == "kannada" else l["name"]
    
    skills = []
    for sid in request.skills[:3]:
        if sid in SKILLS:
            s = SKILLS[sid].copy()
            s["display_name"] = s["name_kn"] if lang == "kannada" else s["name"]
            skills.append(s)
    if not skills:
        s = SKILLS["diya"].copy()
        s["display_name"] = s["name_kn"] if lang == "kannada" else s["name"]
        skills.append(s)
    
    schemes = SCHEMES[:3]
    for s in schemes:
        s["display_name"] = s["name_kn"] if lang == "kannada" else s["name"]
    
    total_setup = sum(l["setup"] for l in livestock) + sum(s["setup"] for s in skills)
    total_monthly = sum(l["monthly"] for l in livestock) + sum(s["monthly"] for s in skills)
    
    return {
        "success": True,
        "crops": crops,
        "livestock": livestock,
        "skills": skills,
        "schemes": schemes,
        "summary": {
            "total_setup": total_setup,
            "monthly_income": total_monthly,
            "stability": "40% → 95%"
        }
    }

@app.post("/api/soil/analyze")
async def analyze_soil(
    file: UploadFile = File(...),
    land_acres: float = Form(...),
    budget: float = Form(...),
    skills: str = Form("[]"),
    language: str = Form("english")
):
    import json
    skill_ids = json.loads(skills) if skills else []
    
    image_bytes = await file.read()
    img = Image.open(io.BytesIO(image_bytes))
    img = img.resize((50, 50))
    img_array = np.array(img)
    avg_color = np.mean(img_array, axis=(0, 1))
    
    if avg_color[0] > 100:
        soil_type = "red"
    elif avg_color[0] < 60:
        soil_type = "black"
    else:
        soil_type = "alluvial"
    
    soil = SOIL_TYPES[soil_type]
    water_key = "low" if soil["water"] == "low" else "moderate"
    
    crops = CROPS.get(water_key, CROPS["low"])[:3]
    for c in crops:
        c["display_name"] = c["name_kn"] if language == "kannada" else c["name"]
    
    livestock = LIVESTOCK[water_key][:2]
    for l in livestock:
        l["display_name"] = l["name_kn"] if language == "kannada" else l["name"]
    
    selected_skills = []
    for sid in skill_ids[:2]:
        if sid in SKILLS:
            selected_skills.append(SKILLS[sid])
    if not selected_skills:
        selected_skills.append(SKILLS["diya"])
    
    return {
        "success": True,
        "soil_analysis": {
            "type": soil["name_kn"] if language == "kannada" else soil["name"],
            "confidence": 85
        },
        "recommendations": {
            "crops": crops,
            "livestock": livestock,
            "skills": selected_skills
        }
    }

@app.get("/api/voice/respond")
async def voice_response(question: str, language: str = "english"):
    q_lower = question.lower()
    if "crop" in q_lower:
        response = "Jowar, Ragi, and Tur Dal are good for low water areas."
        response_kn = "ಜೋಳ, ರಾಗಿ, ತೂರ್ ದಾಳ್ ಕಡಿಮೆ ನೀರಿಗೆ ಒಳ್ಳೆಯದು."
    elif "bidri" in q_lower:
        response = "Bidri work costs ₹5,000, monthly income ₹5,000. Training at KVIC Bidar."
        response_kn = "ಬಿದ್ರಿ ಕೆಲಸಕ್ಕೆ ₹5,000 ವೆಚ್ಚ, ಮಾಸಿಕ ₹5,000 ಆದಾಯ."
    elif "subsidy" in q_lower:
        response = "PMEGP gives 35% subsidy. KVIC gives 40% for handicrafts."
        response_kn = "ಪಿಎಂಇಜಿಪಿ 35% ಸಬ್ಸಿಡಿ. ಕೆವಿಐಸಿ 40% ಸಬ್ಸಿಡಿ."
    else:
        response = "I can help with crops, Bidri work, and subsidies."
        response_kn = "ನಾನು ಬೆಳೆ, ಬಿದ್ರಿ, ಸಬ್ಸಿಡಿ ಬಗ್ಗೆ ಸಹಾಯ ಮಾಡಬಲ್ಲೆ."
    
    return {"response": response_kn if language == "kannada" else response}

if __name__ == "__main__":
    print("=" * 50)
    print("🌾 Sahayak AI Server Starting...")
    print("📍 http://localhost:8000")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000)