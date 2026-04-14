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
    limits: { fileSize: 5 * 1024 * 1024 }
});

// ========== DATA ==========
const CROPS = {
    low: [
        { id: 1, name: "Jowar (Millet)", name_kn: "ಜೋಳ", roi: 4, profit: 15000 },
        { id: 2, name: "Ragi (Finger Millet)", name_kn: "ರಾಗಿ", roi: 4, profit: 18000 },
        { id: 3, name: "Tur Dal (Togari Bele)", name_kn: "ತೊಗರಿಬೇಳೆ", roi: 6, profit: 22000 },
        { id: 4, name: "Groundnut", name_kn: "ಕಡಲೆಕಾಯಿ", roi: 5, profit: 20000 }
    ],
    moderate: [
        { id: 5, name: "Cotton", name_kn: "ಹತ್ತಿ", roi: 6, profit: 35000 },
        { id: 6, name: "Maize", name_kn: "ಮೆಕ್ಕೆಜೋಳ", roi: 3, profit: 25000 },
        { id: 7, name: "Chili", name_kn: "ಮೆಣಸಿನಕಾಯಿ", roi: 5, profit: 40000 }
    ],
    high: [
        { id: 8, name: "Sugarcane", name_kn: "ಕಬ್ಬು", roi: 12, profit: 80000 },
        { id: 9, name: "Pomegranate", name_kn: "ದಾಳಿಂಬೆ", roi: 24, profit: 120000 }
    ]
};

const LIVESTOCK = {
    low: [
        { id: 1, name: "Goat Rearing (5 goats)", name_kn: "ಮೇಕೆ ಸಾಕಣೆ", setup: 15000, monthly: 4000 },
        { id: 2, name: "Beekeeping (5 boxes)", name_kn: "ಜೇನು ಸಾಕಣೆ", setup: 12000, monthly: 5000 },
        { id: 3, name: "Poultry (20 birds)", name_kn: "ಕೋಳಿ ಸಾಕಣೆ", setup: 5000, monthly: 3000 }
    ],
    moderate: [
        { id: 4, name: "Dairy (2 cows)", name_kn: "ಹೈನುಗಾರಿಕೆ", setup: 70000, monthly: 10000 },
        { id: 5, name: "Inland Fisheries", name_kn: "ಮತ್ಸ್ಯಕೃಷಿ", setup: 50000, monthly: 8000 }
    ]
};

const SKILLS = {
    bidri: { id: "bidri", name: "Bidri Work", name_kn: "ಬಿದ್ರಿ ಕೆಲಸ", setup: 5000, monthly: 5000, training: "KVIC Bidar" },
    kasuti: { id: "kasuti", name: "Kasuti Embroidery", name_kn: "ಕಸೂತಿ", setup: 1000, monthly: 3000, training: "KRISHI Jyoti Dharwad" },
    diya: { id: "diya", name: "Diya Making", name_kn: "ದೀಪ ಮಾಡುವುದು", setup: 3000, monthly: 8000, training: "KVIC Hubli" },
    pickle: { id: "pickle", name: "Pickle Making", name_kn: "ಉಪ್ಪಿನಕಾಯಿ", setup: 5000, monthly: 12000, training: "NABARD SHG" }
};

const SCHEMES = [
    { 
        id: 1, name: "PMEGP", name_kn: "ಪಿಎಂಇಜಿಪಿ", 
        full_name: "Prime Minister's Employment Generation Programme",
        full_name_kn: "ಪ್ರಧಾನಮಂತ್ರಿ ಉದ್ಯೋಗ ಸೃಷ್ಟಿ ಯೋಜನೆ",
        subsidy: "35%", loan: 100000, interest: "2%",
        eligibility: "Any farmer above 18 years, 8th pass education",
        eligibility_kn: "18 ವರ್ಷ ಮೇಲ್ಪಟ್ಟ ಯಾವುದೇ ರೈತ, 8ನೇ ತರಗತಿ ಪಾಸ್",
        documents: "Aadhaar, Land papers, Bank account",
        documents_kn: "ಆಧಾರ್, ಜಮೀನು ದಾಖಲೆಗಳು, ಬ್ಯಾಂಕ್ ಖಾತೆ",
        application_link: "https://pmegp.in", deadline: "March 31, 2025",
        contact: "District Industries Centre",
        contact_kn: "ಜಿಲ್ಲಾ ಕೈಗಾರಿಕಾ ಕೇಂದ್ರ"
    },
    { 
        id: 2, name: "NABARD SHG", name_kn: "ನಬಾರ್ಡ್",
        full_name: "NABARD Self Help Group Bank Linkage",
        full_name_kn: "ನಬಾರ್ಡ್ ಸ್ವಸಹಾಯ ಗುಂಪು ಬ್ಯಾಂಕ್ ಸಂಪರ್ಕ",
        subsidy: "Loans at 7%", loan: 50000, interest: "7%",
        eligibility: "Women Self Help Groups with minimum 10 members",
        eligibility_kn: "ಕನಿಷ್ಠ 10 ಸದಸ್ಯರಿರುವ ಮಹಿಳಾ ಸ್ವಸಹಾಯ ಗುಂಪುಗಳು",
        documents: "SHG registration, Minutes book, Bank passbook",
        documents_kn: "ಸ್ವಸಹಾಯ ಗುಂಪು ನೋಂದಣಿ, ನಿಮಿಷಗಳ ಪುಸ್ತಕ, ಬ್ಯಾಂಕ್ ಪಾಸ್ಬುಕ್",
        application_link: "https://nabard.org", deadline: "Rolling",
        contact: "NABARD Regional Office or nearest bank",
        contact_kn: "ನಬಾರ್ಡ್ ಪ್ರಾದೇಶಿಕ ಕಚೇರಿ ಅಥವಾ ಹತ್ತಿರದ ಬ್ಯಾಂಕ್"
    },
    { 
        id: 3, name: "KVIC Craft", name_kn: "ಕೆವಿಐಸಿ",
        full_name: "KVIC Artisan Subsidy Scheme",
        full_name_kn: "ಕೆವಿಐಸಿ ಕುಶಲಕರ್ಮಿ ಸಬ್ಸಿಡಿ ಯೋಜನೆ",
        subsidy: "40%", loan: 75000, interest: "4%",
        eligibility: "Traditional artisans (Bidri, Pottery, Weaving, etc.)",
        eligibility_kn: "ಸಾಂಪ್ರದಾಯಿಕ ಕುಶಲಕರ್ಮಿಗಳು (ಬಿದ್ರಿ, ಕುಂಬಾರಿಕೆ, ನೇಯ್ಗೆ, ಇತ್ಯಾದಿ)",
        documents: "Aadhaar, Skill certificate, Bank account",
        documents_kn: "ಆಧಾರ್, ಕೌಶಲ್ಯ ಪ್ರಮಾಣಪತ್ರ, ಬ್ಯಾಂಕ್ ಖಾತೆ",
        application_link: "https://kvic.gov.in", deadline: "December 31, 2025",
        contact: "KVIC Office in your district",
        contact_kn: "ನಿಮ್ಮ ಜಿಲ್ಲೆಯ ಕೆವಿಐಸಿ ಕಚೇರಿ"
    },
    { 
        id: 4, name: "MGNREGA", name_kn: "ಮಹಾತ್ಮಾ ಗಾಂಧಿ",
        full_name: "Mahatma Gandhi National Rural Employment Guarantee Act",
        full_name_kn: "ಮಹಾತ್ಮಾ ಗಾಂಧಿ ರಾಷ್ಟ್ರೀಯ ಗ್ರಾಮೀಣ ಉದ್ಯೋಗ ಖಾತರಿ ಕಾಯ್ದೆ",
        subsidy: "100%", loan: 35000, interest: "0%",
        eligibility: "Any rural household, 100 days work guarantee",
        eligibility_kn: "ಯಾವುದೇ ಗ್ರಾಮೀಣ ಕುಟುಂಬ, 100 ದಿನಗಳ ಕೆಲಸದ ಖಾತರಿ",
        documents: "Job card, Bank account, Aadhaar",
        documents_kn: "ಜಾಬ್ ಕಾರ್ಡ್, ಬ್ಯಾಂಕ್ ಖಾತೆ, ಆಧಾರ್",
        application_link: "https://nrega.nic.in", deadline: "Rolling",
        contact: "Gram Panchayat Office",
        contact_kn: "ಗ್ರಾಮ ಪಂಚಾಯತ್ ಕಚೇರಿ"
    }
];

const SOIL_TYPES = {
    red: { name: "Red Soil", name_kn: "ಕೆಂಪು ಮಣ್ಣು", water: "low" },
    black: { name: "Black Soil", name_kn: "ಕಪ್ಪು ಮಣ್ಣು", water: "high" },
    laterite: { name: "Laterite Soil", name_kn: "ಲ್ಯಾಟರೈಟ್", water: "moderate" },
    alluvial: { name: "Alluvial Soil", name_kn: "ಮೆಕ್ಕಲು", water: "moderate" }
};

// ========== API ROUTES ==========
app.get('/api/health', (req, res) => {
    res.json({ status: 'healthy', message: 'Sahayak AI Backend is running!' });
});

app.post('/api/recommend', (req, res) => {
    const { land_acres, water, budget, skills, language } = req.body;
    const lang = language || 'english';
    
    let crops = CROPS[water] || CROPS.low;
    crops = crops.slice(0, 3).map(c => ({
        ...c,
        display_name: lang === 'kannada' ? c.name_kn : c.name
    }));
    
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
    
    let schemes = SCHEMES.slice(0, 3).map(s => ({
        ...s,
        display_name: lang === 'kannada' ? s.name_kn : s.name
    }));
    
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

app.post('/api/soil/analyze', upload.single('file'), async (req, res) => {
    try {
        const { land_acres, budget, skills, language } = req.body;
        const lang = language || 'english';
        let skillIds = skills ? JSON.parse(skills) : [];
        
        const imageBuffer = req.file.buffer;
        const image = await sharp(imageBuffer).resize(50, 50).raw().toBuffer();
        
        let rSum = 0;
        for (let i = 0; i < image.length; i += 3) {
            rSum += image[i];
        }
        const avgR = rSum / (image.length / 3);
        
        let soilType = 'alluvial';
        if (avgR > 100 && avgR < 180) soilType = 'red';
        else if (avgR < 60) soilType = 'black';
        else if (avgR > 80 && avgR < 120) soilType = 'laterite';
        
        const soil = SOIL_TYPES[soilType];
        const waterKey = soil.water === 'low' ? 'low' : 'moderate';
        
        let crops = CROPS[waterKey].slice(0, 3).map(c => ({
            ...c,
            display_name: lang === 'kannada' ? c.name_kn : c.name
        }));
        
        let livestock = LIVESTOCK[waterKey].slice(0, 2).map(l => ({
            ...l,
            display_name: lang === 'kannada' ? l.name_kn : l.name
        }));
        
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
            recommendations: { crops, livestock, skills: selectedSkills }
        });
    } catch (error) {
        res.status(500).json({ success: false, error: 'Failed to analyze soil image' });
    }
});

app.get('/api/schemes', (req, res) => {
    const { language } = req.query;
    const lang = language || 'english';
    const schemes = SCHEMES.map(s => ({
        ...s,
        display_name: lang === 'kannada' ? s.name_kn : s.name,
        display_full_name: lang === 'kannada' ? s.full_name_kn : s.full_name,
        display_eligibility: lang === 'kannada' ? s.eligibility_kn : s.eligibility,
        display_documents: lang === 'kannada' ? s.documents_kn : s.documents,
        display_contact: lang === 'kannada' ? s.contact_kn : s.contact
    }));
    res.json({ success: true, schemes });
});

app.get('/api/skills', (req, res) => {
    const { language } = req.query;
    const lang = language || 'english';
    const skills = Object.values(SKILLS).map(s => ({
        ...s,
        display_name: lang === 'kannada' ? s.name_kn : s.name
    }));
    res.json({ success: true, skills });
});

app.get('/api/voice/respond', (req, res) => {
    const { question, language } = req.query;
    const qLower = (question || '').toLowerCase();
    const lang = language || 'english';
    
    let response = '';
    if (qLower.includes('crop') || qLower.includes('ಬೆಳೆ')) {
        response = lang === 'kannada' ? "ಕಡಿಮೆ ನೀರಿಗೆ ಜೋಳ, ರಾಗಿ, ತೊಗರಿಬೇಳೆ ಒಳ್ಳೆಯದು." : "For low water, Jowar, Ragi, and Tur Dal are good.";
    } else if (qLower.includes('bidri') || qLower.includes('ಬಿದ್ರಿ')) {
        response = lang === 'kannada' ? "ಬಿದ್ರಿ ಕೆಲಸಕ್ಕೆ ₹5,000 ವೆಚ್ಚ, ಮಾಸಿಕ ₹5,000 ಆದಾಯ. ಕೆವಿಐಸಿ ಬೀದರ್ನಲ್ಲಿ ತರಬೇತಿ." : "Bidri work costs ₹5,000, monthly income ₹5,000. Training at KVIC Bidar.";
    } else if (qLower.includes('subsidy') || qLower.includes('ಸಬ್ಸಿಡಿ')) {
        response = lang === 'kannada' ? "PMEGP 35% ಸಬ್ಸಿಡಿ, KVIC 40% ಸಬ್ಸಿಡಿ, NABARD ಸಾಲ ಸೌಲಭ್ಯವಿದೆ." : "PMEGP 35% subsidy, KVIC 40% subsidy, NABARD loans available.";
    } else if (qLower.includes('goat') || qLower.includes('ಮೇಕೆ')) {
        response = lang === 'kannada' ? "ಮೇಕೆ ಸಾಕಣೆ ವೆಚ್ಚ ₹15,000, ಮಾಸಿಕ ಆದಾಯ ₹4,000." : "Goat rearing costs ₹15,000, monthly income ₹4,000.";
    } else {
        response = lang === 'kannada' ? "ದಯವಿಟ್ಟು ಬೆಳೆ, ಬಿದ್ರಿ, ಅಥವಾ ಸಬ್ಸಿಡಿ ಬಗ್ಗೆ ಕೇಳಿ." : "Please ask about crops, Bidri, or subsidies.";
    }
    res.json({ response });
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/welcome.html'));
});

app.get('/dashboard', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

app.listen(PORT, () => {
    console.log('='.repeat(50));
    console.log('🌾 Sahayak AI Server is running!');
    console.log('='.repeat(50));
    console.log(`📍 URL: http://localhost:${PORT}`);
    console.log(`📍 Dashboard: http://localhost:${PORT}/dashboard`);
    console.log('='.repeat(50));
});
