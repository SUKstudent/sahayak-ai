import streamlit as st
import requests
import base64

# Page Config for a "Real App" feel
st.set_page_config(page_title="Sahayak AI", page_icon="🌾", layout="centered")

# Custom CSS for better UI
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #2e7d32; color: white; }
    .card { padding: 20px; border-radius: 15px; background-color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌾 Sahayak AI")
st.markdown("---")

# Sidebar for Settings
with st.sidebar:
    st.header("⚙️ Settings")
    lang_choice = st.selectbox("Select Language / ಭಾಷೆ / भाषा", 
                             options=["en", "kn", "hi"], 
                             format_func=lambda x: {"en":"English", "kn":"ಕನ್ನಡ", "hi":"हिन्दी"}[x])
    st.session_state.language = lang_choice
    st.info("Sahayak AI helps farmers choose the best crops and livestock based on land type.")

# Main Interface
st.subheader("What type of farm are you planning?")
col1, col2, col3 = st.columns(3)

choice = None
with col1:
    if st.button("🏜️ Dry Land"): choice = "dry"
with col2:
    if st.button("🐄 Dairy"): choice = "dairy"
with col3:
    if st.button("🐟 Fish Farm"): choice = "fish"

# Execution Logic
if choice:
    with st.spinner('Generating your plan...'):
        try:
            res = requests.post("http://localhost:8000/recommend", 
                               json={"choice": choice, "language": st.session_state.language})
            data = res.json()

            # Results Display in "Card" Style
            st.markdown(f"""
            <div class="card">
                <h3>📋 Your Farming Plan</h3>
                <p><b>🌱 Recommended Crops:</b> {data['crops']}</p>
                <p><b>💰 Income Source:</b> {data['income']}</p>
                <p><b>🔄 Value Addition:</b> {data['value_addition']}</p>
            </div>
            """, unsafe_allow_html=True)

            # Audio Player
            st.write("🔊 **Listen to Recommendation:**")
            audio_bytes = base64.b64decode(data["audio"])
            st.audio(audio_bytes, format="audio/mp3")
            
        except:
            st.error("Could not connect to Backend. Please ensure backend.py is running.")
