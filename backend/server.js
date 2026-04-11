const express = require('express');
const cors = require('cors');
const path = require('path'); // 1. Import path module

const chatRoute = require('./routes/chat');
const analyzeRoute = require('./routes/analyze');
const uploadRoute = require('./routes/upload');

const app = express();

app.use(cors());
app.use(express.json());

// API Routes
app.use('/api/chat', chatRoute);
app.use('/api/analyze', analyzeRoute);
app.use('/api/upload', uploadRoute);

// 2. Serve static files (CSS, JS, Images) from the frontend folder
// Based on your repo structure, frontend is one level up from server.js
app.use(express.static(path.join(__dirname, '../frontend')));

// 3. Serve the index.html for any other request (The Root Route)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend', 'index.html'));
});

// 4. Use dynamic port for deployment (defaults to 5000 for local dev)
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
