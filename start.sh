#!/bin/bash

# Start backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Start frontend
streamlit run app/frontend.py --server.port=8080 --server.address=0.0.0.0
