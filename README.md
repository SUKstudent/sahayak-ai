# 🌾 Sahayak AI - Climate-Resilient Livelihood Planner

A full-stack web application that helps farmers in drought-prone North Karnataka diversify their income sources by providing personalized crop, livestock, and family skill recommendations based on land, water, budget, and location.

## 🚀 Project Overview

This application allows farmers to input their land details, water availability, budget, and family skills. The system uses location intelligence (district selection or GPS) to provide region-specific crop recommendations. Farmers can also upload soil photos for AI-based soil analysis. The platform includes government schemes, family skill monetization options, and saves reports locally.

## 📊 Input Features

Farmers submit the following information through the web interface:

- 📍 **Location** - District selection (13 districts of North Karnataka) or auto-detect via GPS
- 🌍 **Land Size** - Area in acres
- 💧 **Water Availability** - Low / Moderate / High
- 💰 **Budget** - Available investment amount (₹)
- 👨‍👩‍👧‍👦 **Family Skills** - Bidri Work, Kasuti Embroidery, Diya Making, Pickle Making, Agarbatti Making
- 📸 **Soil Photo** - Upload image for AI-based soil analysis

## 🎯 Output

- 🌽 **Crop Recommendations** - Based on water availability and location
- 🐐 **Livestock Options** - Goat rearing, beekeeping, poultry, dairy, fisheries
- 👩‍🎨 **Family Skills to Monetize** - Setup cost, monthly income, training center
- 🏦 **Government Schemes** - Subsidy percentage, loan amount, eligibility, documents, deadlines, apply links
- 📈 **Income Summary** - Total setup cost, monthly income, ROI, stability improvement (40% → 95%)
- 📍 **Location Intelligence** - Soil type and water availability based on district

## 🗺️ Districts Covered

| District | Soil Type | Water Availability |
|----------|-----------|-------------------|
| Bagalkot | Red Soil | Low |
| Vijayapura | Red Soil | Low |
| Gadag | Red Soil | Low |
| Koppal | Red Soil | Low |
| Belagavi | Black Soil | Moderate |
| Dharwad | Black Soil | Moderate |
| Haveri | Black Soil | Moderate |
| Raichur | Alluvial Soil | Moderate |
| Yadgir | Alluvial Soil | Moderate |
| Kalaburagi | Alluvial Soil | Moderate |
| Uttara Kannada | Laterite Soil | High |
| Shivamogga | Laterite Soil | High |
| Chikkamagaluru | Laterite Soil | High |

## 👨‍👩‍👧‍👦 Family Skills Included

| Skill | Setup Cost | Monthly Income | Training Center | Water Required |
|-------|------------|----------------|-----------------|----------------|
| Bidri Work | ₹5,000 | ₹5,000 | KVIC Bidar | Zero |
| Kasuti Embroidery | ₹1,000 | ₹3,000 | KRISHI Jyoti Dharwad | Zero |
| Diya Making | ₹3,000 | ₹8,000 | KVIC Hubli | Zero |
| Pickle Making | ₹5,000 | ₹12,000 | NABARD SHG | Low |
| Agarbatti Making | ₹4,000 | ₹7,000 | KVIC | Zero |

## 🏦 Government Schemes Included

| Scheme | Subsidy | Max Loan | Interest | Deadline |
|--------|---------|----------|----------|----------|
| PMEGP | 35% | ₹1,00,000 | 2% | March 31, 2025 |
| NABARD SHG | Loans at 7% | ₹50,000 | 7% | Rolling |
| KVIC Craft | 40% | ₹75,000 | 4% | Dec 31, 2025 |
| MGNREGA | 100% | ₹35,000 | 0% | Rolling |
| RKVY | 50% | ₹2,00,000 | 3% | June 30, 2025 |

## 📊 Impact Metrics

| Metric | Before | After |
|--------|--------|-------|
| Income Stability | 40% | **95%** |
| Income Sources | 1-2 | **4-6** |
| Women's Income | 0-10% | **40-60%** |
| Zero-income days/year | 150-200 | **30-50** |
| Water Dependency | 90% | **<40%** |

## 🛠 Technologies Used

- **Backend:** Node.js, Express
- **Frontend:** HTML5, CSS3, JavaScript
- **Image Processing:** Sharp
- **File Upload:** Multer
- **Location Services:** Geolocation API, OpenStreetMap Nominatim
- **Version Control:** Git

## 📁 Project Structure

sahayak-ai/

├── backend/

│ ├── server.js # Express server with API routes

│ └── package.json # Dependencies

├── frontend/

│ ├── welcome.html # Landing page

│ └── index.html # Main dashboard

└── README.md # Documentation

## 📱 How to Use

### 1)For Farmers

a.Select your district or use GPS location

b.Enter land size, water availability, and budget

c.Select family skills (if any)

d.Click "Get Recommendations"

e.View personalized crop, livestock, and skill recommendations

f.Check government schemes for funding options

### 2)For Soil Analysis

a.Click "Soil Analysis" tab

b.Upload a photo of your soil

c.Enter land size and budget

d.Click "Analyze Soil"

e.AI predicts soil type and recommends suitable crops

----

## 🗣️Language Support

1)Click "English" or "ಕನ್ನಡ" buttons to switch languages

2)All content, labels, and recommendations update automatically

----

🔮 Future Scope

🔲 Real-time weather API integration (IMD)

🔲 Live market price updates (APMC)

🔲 Offline-first PWA

🔲 SMS interface for feature phones

🔲 AI crop disease detection from photos

🔲 Farmer-to-farmer network & marketplace

🔲 Integration with government portals for direct application
