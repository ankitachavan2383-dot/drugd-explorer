"""Small reusable UI pieces."""
import streamlit as st


def page_header(title: str, subtitle: str):
    st.markdown(f"""
    <div class="header">
        <h1 style="color:black; margin:0;">{title}</h1>
        <p style="color:black; margin:0; opacity:0.8;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
