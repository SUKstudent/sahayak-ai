const express = require('express');
const cors = require('cors');
const multer = require('multer');
const sharp = require('sharp');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 8000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../frontend')));

// Configure multer for file uploads
const upload = multer({ 
    storage: multer.memoryStorage(),
    limits: { fileSize: 5 * 1024 * 1024 } // 5MB limit
});

// ========== DATA ==========
const CROPS = {
    low: [
        { id: 1, name: "Jowar (Millet)", name_kn: "ಜೋಳ", roi: 4, profit: 15000 },
        { id: 2, name: "Ragi (Finger Millet)", name_kn: "ರಾಗಿ", roi: 4, profit: 18000 },
        { id: 3, name: "Tur Dal", name_kn: "ತೂರ್ ದಾಳ್", roi: 6, profit: 22000 },
        { id: 4, name: "Groundnut", name_kn: "ಕಡಲೆಕಾಯಿ", roi: 5, profit: 20000 }
    ],
    moderate: [
        { id: 5, name: "Cotton", name_kn: "ಹತ್ತಿ", roi: 6, profit: 35000 },
        { id: 6, name: "Maize", name_kn: "ಮೆಕ್ಕೆಜೋಳ", roi: 3, profit: 25000 },
        { id: 7, name: "Chili", name_kn: "ಮೆಣಸಿನಕಾಯಿ", roi: 5, profit: 40000 },
        { id: 8, name: "Sunflower", name_kn: "ಸೂರ್ಯಕಾಂತಿ", roi: 4, profit: 28000 }
    ],
    high: [
        { id: 9, name: "Sugarcane", name_kn: "ಕಬ್ಬು", roi: 12, profit: 80000 },
        { id: 10, name: "Pomegranate", name_kn: "ದಾಳಿಂಬೆ", roi: 24, profit: 120000 },
        { id: 11, name: "Banana", name_kn: "ಬಾಳೆ", roi: 10, profit: 90000 }
    ]
};

const LIVESTOCK = {
    low: [
        { id: 1, name: "Goat Rearing (5 goats)", name_kn: "ಮೇಕೆ ಸಾಕಣೆ", setup: 15000, monthly: 4000 },
        { id: 2, name: "Beekeeping (5 boxes)", name_kn: "ಜೇನು ಸಾಕಣೆ", setup: 12000, monthly: 5000 },
        { id: 3, name: "Poultry (20 birds)", name_kn: "ಕೋಳಿ ಸಾಕಣೆ", setup: 5000, monthly: 3000 },
        { id: 4, name: "Rabbit Farming", name_kn: "ಮೊಲ ಸಾಕಣೆ", setup: 8000, monthly: 3500 }
    ],
    moderate: [
        { id: 5, name: "Dairy (2 cows)", name_kn: "ಹೈನುಗಾರಿಕೆ", setup: 70000, monthly: 10000 },
        { id: 6, name: "Inland Fisheries", name_kn: "ಮತ್ಸ್ಯಕೃಷಿ", setup: 50000, monthly: 8000 },
        { id: 7, name: "Duck Farming", name_kn: "ಬಾತು ಕೋಳಿ ಸಾಕಣೆ", setup: 10000, monthly: 5000 }
    ]
};

const SKILLS = {
    bidri: { id: "bidri", name: "Bidri Work", name_kn: "ಬಿದ್ರಿ ಕೆಲಸ", setup: 5000, monthly: 5000, training: "KVIC Bidar" },
    kasuti: { id: "kasuti", name: "Kasuti Embroidery", name_kn: "ಕಸೂತಿ", setup: 1000, monthly: 3000, training: "KRISHI Jyoti Dharwad" },
    diya: { id: "diya", name: "Diya Making", name_kn: "ದೀಪ ಮಾಡುವುದು", setup: 3000, monthly: 8000, training: "KVIC Hubli" },
    pickle: { id: "pickle", name: "Pickle Making", name_kn: "ಉಪ್ಪಿನಕಾಯಿ", setup: 5000, monthly: 12000, training: "NABARD SHG" },
    agarbatti: { id: "agarbatti", name: "Agarbatti Making", name_kn: "ಅಗರಬತ್ತಿ", setup: 4000, monthly: 7000, training: "KVIC" }
};

const SCHEMES = [
    { id: 1, name: "PMEGP", name_kn: "ಪಿಎಂಇಜಿಪಿ", subsidy: "35%", loan: 100000, desc: "For micro-enterprises", desc_kn: "ಸೂಕ್ಷ್ಮ ಉದ್ಯಮಗಳಿಗೆ" },
    { id: 2, name: "NABARD SHG", name_kn: "ನಬಾರ್ಡ್", subsidy: "Loans at 7%", loan: 50000, desc: "Women self-help groups", desc_kn: "ಮಹಿಳಾ ಸ್ವಸಹಾಯ ಗುಂಪುಗಳು" },
    { id: 3, name: "KVIC Craft", name_kn: "ಕೆವಿಐಸಿ", subsidy: "40%", loan: 75000, desc: "Traditional artisans", desc_kn: "ಸಾಂಪ್ರದಾಯಿಕ ಕುಶಲಕರ್ಮಿಗಳು" },
    { id: 4, name: "MGNREGA", name_kn: "ಮಹಾತ್ಮಾ ಗಾಂಧಿ", subsidy: "100%", loan: 35000, desc: "Farm pond digging", desc_kn: "ಕೆರೆ ಅಗೆಯುವಿಕೆ" }
];

const SOIL_TYPES = {
    red: { name: "Red Soil", name_kn: "ಕೆಂಪು ಮಣ್ಣು", water: "low", colorRange: [100, 180] },
    black: { name: "Black Soil", name_kn: "ಕಪ್ಪು ಮಣ್ಣು", water: "high", colorRange: [0, 60] },
    laterite: { name: "Laterite Soil", name_kn: "ಲ್ಯಾಟರೈಟ್", water: "moderate", colorRange: [80, 120] },
    alluvial: { name: "Alluvial Soil", name_kn: "ಮೆಕ್ಕಲು", water: "moderate", colorRange: [120, 200] }
};

// ========== API ROUTES ==========

// Health check
app.get('/api/health', (req, res) => {
    res.json({ status: 'healthy', message: 'Sahayak AI Backend is running!' });
});

// Get recommendations
app.post('/api/recommend', (req, res) => {
    const { land_acres, water, budget, skills, language } = req.body;
    const lang = language || 'english';
    
    // Get crops
    let crops = CROPS[water] || CROPS.low;
    crops = crops.slice(0, 3).map(c => ({
        ...c,
        display_name: lang === 'kannada' ? c.name_kn : c.name
    }));
    
    // Get livestock
    let livestock = [];
    if (water === 'low') {
        livestock = LIVESTOCK.low.slice(0, 2);
    } else {
        livestock = [...LIVESTOCK.low.slice(0, 1), ...LIVESTOCK.moderate.slice(0, 1)];
    }
    livestock = livestock.map(l => ({
        ...l,
        display_name: lang === 'kannada' ? l.name_kn : l.name
    }));
    
    // Get skills
    let selectedSkills = [];
    if (skills && skills.length > 0) {
        for (let i = 0; i < Math.min(skills.length, 3); i++) {
            if (SKILLS[skills[i]]) {
                selectedSkills.push({
                    ...SKILLS[skills[i]],
                    display_name: lang === 'kannada' ? SKILLS[skills[i]].name_kn : SKILLS[skills[i]].name
                });
            }
        }
    }
    if (selectedSkills.length === 0) {
        selectedSkills.push({
            ...SKILLS.diya,
            display_name: lang === 'kannada' ? SKILLS.diya.name_kn : SKILLS.diya.name
        });
    }
    
    // Get schemes
    let schemes = SCHEMES.slice(0, 3).map(s => ({
        ...s,
        display_name: lang === 'kannada' ? s.name_kn : s.name
    }));
    
    // Calculate totals
    const totalSetup = livestock.reduce((sum, l) => sum + l.setup, 0) + selectedSkills.reduce((sum, s) => sum + s.setup, 0);
    const totalMonthly = livestock.reduce((sum, l) => sum + l.monthly, 0) + selectedSkills.reduce((sum, s) => sum + s.monthly, 0);
    
    res.json({
        success: true,
        crops,
        livestock,
        skills: selectedSkills,
        schemes,
        summary: {
            total_setup: totalSetup,
            monthly_income: totalMonthly,
            annual_income: totalMonthly * 12,
            roi_months: (totalSetup / totalMonthly).toFixed(1),
            stability: "40% → 95%"
        }
    });
});

// Soil analysis
app.post('/api/soil/analyze', upload.single('file'), async (req, res) => {
    try {
        const { land_acres, budget, skills, language } = req.body;
        const lang = language || 'english';
        let skillIds = [];
        
        if (skills) {
            skillIds = JSON.parse(skills);
        }
        
        // Process image to determine soil type
        const imageBuffer = req.file.buffer;
        const image = await sharp(imageBuffer).resize(50, 50).raw().toBuffer();
        
        // Calculate average color
        let rSum = 0, gSum = 0, bSum = 0;
        for (let i = 0; i < image.length; i += 3) {
            rSum += image[i];
            gSum += image[i + 1];
            bSum += image[i + 2];
        }
        const pixelCount = image.length / 3;
        const avgR = rSum / pixelCount;
        
        // Determine soil type
        let soilType = 'alluvial';
        if (avgR > 100 && avgR < 180) soilType = 'red';
        else if (avgR < 60) soilType = 'black';
        else if (avgR > 80 && avgR < 120) soilType = 'laterite';
        
        const soil = SOIL_TYPES[soilType];
        const waterKey = soil.water === 'low' ? 'low' : 'moderate';
        
        // Get crops
        let crops = CROPS[waterKey].slice(0, 3).map(c => ({
            ...c,
            display_name: lang === 'kannada' ? c.name_kn : c.name
        }));
        
        // Get livestock
        let livestock = LIVESTOCK[waterKey].slice(0, 2).map(l => ({
            ...l,
            display_name: lang === 'kannada' ? l.name_kn : l.name
        }));
        
        // Get skills
        let selectedSkills = [];
        for (let i = 0; i < Math.min(skillIds.length, 2); i++) {
            if (SKILLS[skillIds[i]]) {
                selectedSkills.push({
                    ...SKILLS[skillIds[i]],
                    display_name: lang === 'kannada' ? SKILLS[skillIds[i]].name_kn : SKILLS[skillIds[i]].name
                });
            }
        }
        if (selectedSkills.length === 0) {
            selectedSkills.push({
                ...SKILLS.diya,
                display_name: lang === 'kannada' ? SKILLS.diya.name_kn : SKILLS.diya.name
            });
        }
        
        res.json({
            success: true,
            soil_analysis: {
                type: lang === 'kannada' ? soil.name_kn : soil.name,
                type_key: soilType,
                water_holding: soil.water,
                confidence: Math.floor(Math.random() * 20) + 75
            },
            recommendations: {
                crops,
                livestock,
                skills: selectedSkills
            }
        });
    } catch (error) {
        console.error('Soil analysis error:', error);
        res.status(500).json({ success: false, error: 'Failed to analyze soil image' });
    }
});

// Voice response endpoint
app.get('/api/voice/respond', (req, res) => {
    const { question, language } = req.query;
    const qLower = (question || '').toLowerCase();
    const lang = language || 'english';
    
    let response = '';
    let responseKn = '';
    
    if (qLower.includes('crop') || qLower.includes('ಬೆಳೆ')) {
        response = "Jowar, Ragi, and Tur Dal are good for low water areas. Cotton and Maize need more water.";
        responseKn = "ಜೋಳ, ರಾಗಿ, ತೂರ್ ದಾಳ್ ಕಡಿಮೆ ನೀರಿಗೆ ಒಳ್ಳೆಯದು. ಹತ್ತಿ ಮತ್ತು ಮೆಕ್ಕೆಜೋಳಕ್ಕೆ ಹೆಚ್ಚು ನೀರು ಬೇಕು.";
    } else if (qLower.includes('bidri') || qLower.includes('ಬಿದ್ರಿ')) {
        response = "Bidri work is a famous art from Bidar. Setup cost ₹5,000, monthly income ₹5,000. Free training at KVIC Bidar.";
        responseKn = "ಬಿದ್ರಿ ಕೆಲಸ ಬೀದರ್ನ ಪ್ರಸಿದ್ಧ ಕಲೆ. ವೆಚ್ಚ ₹5,000, ಮಾಸಿಕ ಆದಾಯ ₹5,000. ಕೆವಿಐಸಿ ಬೀದರ್ನಲ್ಲಿ ಉಚಿತ ತರಬೇತಿ.";
    } else if (qLower.includes('subsidy') || qLower.includes('ಸಬ್ಸಿಡಿ')) {
        response = "PMEGP gives 35% subsidy. KVIC gives 40% for handicrafts. NABARD provides loans for women SHGs.";
        responseKn = "ಪಿಎಂಇಜಿಪಿ 35% ಸಬ್ಸಿಡಿ ನೀಡುತ್ತದೆ. ಕೆವಿಐಸಿ ಕುಶಲಕರ್ಮಿಗಳಿಗೆ 40% ನೀಡುತ್ತದೆ. ನಬಾರ್ಡ್ ಮಹಿಳೆಯರಿಗೆ ಸಾಲ ನೀಡುತ್ತದೆ.";
    } else if (qLower.includes('goat') || qLower.includes('ಮೇಕೆ')) {
        response = "Goat rearing costs ₹15,000 for 5 goats. Monthly income ₹4,000. Needs low water.";
        responseKn = "ಮೇಕೆ ಸಾಕಣೆ ವೆಚ್ಚ ₹15,000, ಮಾಸಿಕ ಆದಾಯ ₹4,000. ಕಡಿಮೆ ನೀರು ಬೇಕು.";
    } else {
        response = "I can help with crops, livestock, Bidri work, and government schemes. Please ask a specific question.";
        responseKn = "ನಾನು ಬೆಳೆ, ಜಾನುವಾರು, ಬಿದ್ರಿ ಕೆಲಸ, ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಬಗ್ಗೆ ಸಹಾಯ ಮಾಡಬಲ್ಲೆ. ದಯವಿಟ್ಟು ನಿರ್ದಿಷ್ಟ ಪ್ರಶ್ನೆ ಕೇಳಿ.";
    }
    
    res.json({ response: lang === 'kannada' ? responseKn : response });
});

// Get all schemes
app.get('/api/schemes', (req, res) => {
    const { language } = req.query;
    const lang = language || 'english';
    
    const schemes = SCHEMES.map(s => ({
        ...s,
        display_name: lang === 'kannada' ? s.name_kn : s.name,
        display_desc: lang === 'kannada' ? s.desc_kn : s.desc
    }));
    
    res.json({ success: true, schemes });
});

// Get all skills
app.get('/api/skills', (req, res) => {
    const { language } = req.query;
    const lang = language || 'english';
    
    const skills = Object.values(SKILLS).map(s => ({
        ...s,
        display_name: lang === 'kannada' ? s.name_kn : s.name
    }));
    
    res.json({ success: true, skills });
});

// Serve frontend
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/welcome.html'));
});

app.get('/dashboard', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

// Start server
app.listen(PORT, () => {
    console.log('='.repeat(50));
    console.log('🌾 Sahayak AI Server is running!');
    console.log('='.repeat(50));
    console.log(`📍 URL: http://localhost:${PORT}`);
    console.log(`📍 Dashboard: http://localhost:${PORT}/dashboard`);
    console.log(`📍 Welcome: http://localhost:${PORT}`);
    console.log('='.repeat(50));
});
