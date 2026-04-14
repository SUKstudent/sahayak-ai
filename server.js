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

// Serve static files from frontend folder
app.use(express.static(path.join(__dirname, 'frontend')));

// Configure multer for file uploads
const upload = multer({ 
    storage: multer.memoryStorage(),
    limits: { fileSize: 5 * 1024 * 1024 }
});

// ========== DATA (Keep your existing data here) ==========
// ... (your CROPS, LIVESTOCK, SKILLS, SCHEMES, SOIL_TYPES)

// ========== API ROUTES ==========
// ... (your existing API routes)

// ========== SERVE FRONTEND - FIXED PATHS ==========
// Welcome page at root URL
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend', 'welcome.html'));
});

// Dashboard page
app.get('/dashboard', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend', 'index.html'));
});

// Start server
app.listen(PORT, () => {
    console.log('='.repeat(50));
    console.log('🌾 Sahayak AI Server is running!');
    console.log('='.repeat(50));
    console.log(`📍 URL: http://localhost:${PORT}`);
    console.log(`📍 Dashboard: http://localhost:${PORT}/dashboard`);
    console.log('='.repeat(50));
});
