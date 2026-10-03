"""Drug Candidate Exploration Hub — entry point.

Run with:  streamlit run app.py
"""
import streamlit as st

# set_page_config must be the first Streamlit call
st.set_page_config(
    layout="wide",
    page_title="Drug Candidate Exploration Hub",
    page_icon="🧪",
    initial_sidebar_state="expanded",
)

from config.styles import MAIN_CSS
from core.data_loader import download_dataset
from core.state import init_session_state
from modules import (about, admet, dashboard, explorer, home, optimization,
                     property_calculator, scaffold, similarity, virtual_screening)

# Sidebar label -> page module (each exposes render(data))
PAGES = {
    "ℹ️ Home page": home,
    "🏠 Dashboard Overview": dashboard,
    "🔍 Drug Explorer": explorer,
    "🧮 Molecular Property Calculator": property_calculator,
    "📊 Advanced Similarity Search": similarity,
    "💊 ADMET Prediction": admet,
    "🧩 Scaffold Analysis": scaffold,
    "🖥️ Virtual Screening": virtual_screening,
    "⚗️ Compound Optimization": optimization,
    "ℹ️ About": about,
}

st.markdown(MAIN_CSS, unsafe_allow_html=True)
init_session_state()

with st.sidebar:
    selection = st.radio("Select Module:", list(PAGES.keys()), label_visibility="collapsed")
    st.markdown("<hr style='border-top: 2px dashed #E0B0C0;'>", unsafe_allow_html=True)

data = download_dataset()
PAGES[selection].render(data)

if st.button("Clear All Cache", help="Reset all cached data", key="clear_cache_button"):
    st.cache_data.clear()
    st.success("Cache cleared successfully!")
