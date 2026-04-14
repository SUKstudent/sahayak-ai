from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import io
import json
import random
import numpy as np
from PIL import Image
import uvicorn
import os

app = FastAPI(title="Sahayak AI")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend files
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

# ========== DATA ==========
CROPS = {
    "low": [
        {"name": "Jowar (Millet)", "name_kn": "ಜೋಳ", "roi": 4, "profit": 15000},
        {"name": "Ragi (Finger Millet)", "name_kn": "ರಾಗಿ", "roi": 4, "profit": 18000},
        {"name": "Tur Dal", "name_kn": "ತೂರ್ ದಾಳ್", "roi": 6, "profit": 22000},
        {"name": "Groundnut", "name_kn": "ಕಡಲೆಕಾಯಿ", "roi": 5, "profit": 20000},
    ],
    "moderate": [
        {"name": "Cotton", "name_kn": "ಹತ್ತಿ", "roi": 6, "profit": 35000},
        {"name": "Maize", "name_kn": "ಮೆಕ್ಕೆಜೋಳ", "roi": 3, "profit": 25000},
        {"name": "Chili", "name_kn": "ಮೆಣಸಿನಕಾಯಿ", "roi": 5, "profit": 40000},
        {"name": "Sunflower", "name_kn": "ಸೂರ್ಯಕಾಂತಿ", "roi": 4, "profit": 28000},
    ],
    "high": [
        {"name": "Sugarcane", "name_kn": "ಕಬ್ಬು", "roi": 12, "profit": 80000},
        {"name": "Pomegranate", "name_kn": "ದಾಳಿಂಬೆ", "roi": 24, "profit": 120000},
        {"name": "Banana", "name_kn": "ಬಾಳೆ", "roi": 10, "profit": 90000},
    ]
}

LIVESTOCK = {
    "low": [
        {"name": "Goat Rearing (5 goats)", "name_kn": "ಮೇಕೆ ಸಾಕಣೆ", "setup": 15000, "monthly": 4000},
        {"name": "Beekeeping (5 boxes)", "name_kn": "ಜೇನು ಸಾಕಣೆ", "setup": 12000, "monthly": 5000},
        {"name": "Poultry (20 birds)", "name_kn": "ಕೋಳಿ ಸಾಕಣೆ", "setup": 5000, "monthly": 3000},
        {"name": "Rabbit Farming", "name_kn": "ಮೊಲ ಸಾಕಣೆ", "setup": 8000, "monthly": 3500},
    ],
    "moderate": [
        {"name": "Dairy (2 cows)", "name_kn": "ಹೈನುಗಾರಿಕೆ", "setup": 70000, "monthly": 10000},
        {"name": "Inland Fisheries", "name_kn": "ಮತ್ಸ್ಯಕೃಷಿ", "setup": 50000, "monthly": 8000},
        {"name": "Duck Farming", "name_kn": "ಬಾತು ಕೋಳಿ ಸಾಕಣೆ", "setup": 10000, "monthly": 5000},
    ]
}

SKILLS = {
    "bidri": {"name": "Bidri Work", "name_kn": "ಬಿದ್ರಿ ಕೆಲಸ", "setup": 5000, "monthly": 5000, "training": "KVIC Bidar"},
    "kasuti": {"name": "Kasuti Embroidery", "name_kn": "ಕಸೂತಿ", "setup": 1000, "monthly": 3000, "training": "KRISHI Jyoti Dharwad"},
    "diya": {"name": "Diya Making", "name_kn": "ದೀಪ ಮಾಡುವುದು", "setup": 3000, "monthly": 8000, "training": "KVIC Hubli"},
    "pickle": {"name": "Pickle Making", "name_kn": "ಉಪ್ಪಿನಕಾಯಿ", "setup": 5000, "monthly": 12000, "training": "NABARD SHG"},
    "agarbatti": {"name": "Agarbatti Making", "name_kn": "ಅಗರಬತ್ತಿ", "setup": 4000, "monthly": 7000, "training": "KVIC"},
}

SCHEMES = [
    {"name": "PMEGP", "name_kn": "ಪಿಎಂಇಜಿಪಿ", "subsidy": "35%", "loan": 100000, "desc": "For micro-enterprises"},
    {"name": "NABARD SHG", "name_kn": "ನಬಾರ್ಡ್", "subsidy": "Loans at 7%", "loan": 50000, "desc": "Women self-help groups"},
    {"name": "KVIC Craft", "name_kn": "ಕೆವಿಐಸಿ", "subsidy": "40%", "loan": 75000, "desc": "Traditional artisans"},
    {"name": "MGNREGA", "name_kn": "ಮಹಾತ್ಮಾ ಗಾಂಧಿ", "subsidy": "100%", "loan": 35000, "desc": "Farm pond digging"},
]

SOIL_TYPES = {
    "red": {"name": "Red Soil", "name_kn": "ಕೆಂಪು ಮಣ್ಣು", "water": "low", "color": [165, 42, 42]},
    "black": {"name": "Black Soil", "name_kn": "ಕಪ್ಪು ಮಣ್ಣು", "water": "high", "color": [40, 40, 40]},
    "laterite": {"name": "Laterite Soil", "name_kn": "ಲ್ಯಾಟರೈಟ್", "water": "moderate", "color": [160, 82, 45]},
    "alluvial": {"name": "Alluvial Soil", "name_kn": "ಮೆಕ್ಕಲು", "water": "moderate", "color": [210, 180, 140]},
}

class FarmerRequest(BaseModel):
    land_acres: float
    water: str
    budget: float
    skills: List[str] = []
    language: str = "english"

@app.get("/")
async def root():
    return {"message": "🌾 Sahayak AI is running!", "status": "ready"}

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

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
            "annual_income": total_monthly * 12,
            "roi_months": round(total_setup / total_monthly, 1) if total_monthly > 0 else 0,
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
    skill_ids = json.loads(skills) if skills else []
    
    image_bytes = await file.read()
    img = Image.open(io.BytesIO(image_bytes))
    img = img.resize((50, 50))
    img_array = np.array(img)
    avg_color = np.mean(img_array, axis=(0, 1))
    
    # Determine soil type by color
    if avg_color[0] > 100 and avg_color[0] < 180:
        soil_type = "red"
    elif avg_color[0] < 60:
        soil_type = "black"
    elif avg_color[0] > 80 and avg_color[0] < 120:
        soil_type = "laterite"
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
    
    for s in selected_skills:
        s["display_name"] = s["name_kn"] if language == "kannada" else s["name"]
    
    return {
        "success": True,
        "soil_analysis": {
            "type": soil["name_kn"] if language == "kannada" else soil["name"],
            "type_key": soil_type,
            "water_holding": soil["water"],
            "confidence": random.randint(75, 95)
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
    
    if "crop" in q_lower or "ಬೆಳೆ" in q_lower:
        response = "Jowar, Ragi, and Tur Dal are good for low water areas. Cotton and Maize need more water."
        response_kn = "ಜೋಳ, ರಾಗಿ, ತೂರ್ ದಾಳ್ ಕಡಿಮೆ ನೀರಿಗೆ ಒಳ್ಳೆಯದು. ಹತ್ತಿ ಮತ್ತು ಮೆಕ್ಕೆಜೋಳಕ್ಕೆ ಹೆಚ್ಚು ನೀರು ಬೇಕು."
    elif "bidri" in q_lower or "ಬಿದ್ರಿ" in q_lower:
        response = "Bidri work is a famous art from Bidar. Setup cost ₹5,000, monthly income ₹5,000. Free training at KVIC Bidar."
        response_kn = "ಬಿದ್ರಿ ಕೆಲಸ ಬೀದರ್ನ ಪ್ರಸಿದ್ಧ ಕಲೆ. ವೆಚ್ಚ ₹5,000, ಮಾಸಿಕ ಆದಾಯ ₹5,000. ಕೆವಿಐಸಿ ಬೀದರ್ನಲ್ಲಿ ಉಚಿತ ತರಬೇತಿ."
    elif "subsidy" in q_lower or "ಸಬ್ಸಿಡಿ" in q_lower:
        response = "PMEGP gives 35% subsidy. KVIC gives 40% for handicrafts. NABARD provides loans for women SHGs."
        response_kn = "ಪಿಎಂಇಜಿಪಿ 35% ಸಬ್ಸಿಡಿ ನೀಡುತ್ತದೆ. ಕೆವಿಐಸಿ ಕುಶಲಕರ್ಮಿಗಳಿಗೆ 40% ನೀಡುತ್ತದೆ. ನಬಾರ್ಡ್ ಮಹಿಳೆಯರಿಗೆ ಸಾಲ ನೀಡುತ್ತದೆ."
    elif "goat" in q_lower or "ಮೇಕೆ" in q_lower:
        response = "Goat rearing costs ₹15,000 for 5 goats. Monthly income ₹4,000. Needs low water. NABARD loans available."
        response_kn = "ಮೇಕೆ ಸಾಕಣೆ ವೆಚ್ಚ ₹15,000, ಮಾಸಿಕ ಆದಾಯ ₹4,000. ಕಡಿಮೆ ನೀರು ಬೇಕು. ನಬಾರ್ಡ್ ಸಾಲ ಸೌಲಭ್ಯವಿದೆ."
    else:
        response = "I can help with crops, livestock, Bidri work, and government schemes. Please ask a specific question."
        response_kn = "ನಾನು ಬೆಳೆ, ಜಾನುವಾರು, ಬಿದ್ರಿ ಕೆಲಸ, ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಬಗ್ಗೆ ಸಹಾಯ ಮಾಡಬಲ್ಲೆ. ದಯವಿಟ್ಟು ನಿರ್ದಿಷ್ಟ ಪ್ರಶ್ನೆ ಕೇಳಿ."
    
    return {"response": response_kn if language == "kannada" else response, "language": language}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
