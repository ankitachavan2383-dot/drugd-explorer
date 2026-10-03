import streamlit as st
from components.ui import page_header


def render(data):
    page_header("🧪 Drug Candidate Exploration Hub",
                "Comprehensive cheminformatics platform for modern drug discovery")
    st.markdown("---")

    st.markdown("""
    ## 🌟 Platform Overview

    The **Drug Discovery Suite** is a state-of-the-art cheminformatics platform designed to accelerate small molecule drug discovery through:

    - **Interactive molecular analysis** with real-time visualization
    - **Comprehensive property calculation** with 200+ descriptors
    - **Advanced predictive modeling** for ADMET properties
    - **Target identification** through ChEMBL integration
    - **Virtual screening** capabilities for large compound libraries

    Built on RDKit and Streamlit, this platform combines robust computational chemistry with an intuitive interface.
    """)

    st.markdown("""
    ## 🚀 Key Capabilities

    ### Core Modules:

    | Module | Description | Key Features |
    |--------|-------------|--------------|
    | **Dashboard** | Overview of compound collections | Property distributions, chemical space visualization |
    | **Drug Explorer** | Browse and filter compound databases | Advanced filtering, scaffold analysis |
    | **Property Calculator** | Calculate molecular descriptors | Basic and advanced descriptors, 2D/3D visualization, Fingerprints |
    | **Similarity Search** | Find structurally similar compounds | Multiple fingerprints, batch processing |
    | **ADMET Prediction** | Predict drug-like properties | Drug likeness, Lipinski rules, toxicity alerts, BBB penetration |
    | **Virtual Screening** | Screen compound libraries | Customizable thresholds, structural alerts |
    | **Compound Optimization** | Improve drug properties | Bioisostere suggestions, property optimization |
    """)

    st.markdown("""
    ## 📖 User Guide

    ### Getting Started

    1. **Select a Molecule**:
       - Choose from the built-in database of drug-like compounds
       - Or enter a SMILES string directly
       - View basic properties in the Dashboard

    2. **Explore Features**:
       - Calculate descriptors in Molecular Property Calculator
       - Run similarity searches against the database
       - Predict ADMET properties
       - Perform virtual screening

    3. **Advanced Workflows**:
       - Upload your own compound libraries (CSV/TXT)
       - Analyze scaffold networks
       - Get optimization suggestions

    ### Best Practices

    - **For Property Calculation**:
      - Start with the Basic Properties tab for key descriptors
      - Use Advanced Descriptors for specialized calculations
      - Check the 2D/3D Viewer to validate structures

    - **For Similarity Searching**:
      - Morgan fingerprints (radius=2) work well for general similarity
      - MACCS keys are better for scaffold hopping
      - Adjust similarity threshold based on your needs (0.7-0.9 typical)

    - **For Virtual Screening**:
      - Check structural alerts first (PAINS, Brenk filters)
      - Start with moderate similarity thresholds (0.6-0.7)
      - Consider multiple fingerprint types for comprehensive results

    - **For Compound Optimization**:
      - Address Lipinski rule violations first
      - Consider bioisosteric replacements for problematic groups
      - Balance solubility and permeability properties
    """)
