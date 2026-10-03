import pandas as pd
import streamlit as st
from rdkit import Chem, DataStructs
from rdkit.Chem import Draw

from components.molecule_input import display_molecule_input
from components.ui import page_header
from core.chem_utils import get_database_fps, get_fingerprint

PAGE_KEY = "similarity"
TOP_N = 5


def _read_upload(uploaded):
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
        col = "SMILES" if "SMILES" in df.columns else df.columns[0]
        return df[col].astype(str).tolist()
    df = pd.read_csv(uploaded, header=None, names=["SMILES"])
    return df["SMILES"].astype(str).tolist()


def _batch_search(data, fp_type):
    st.markdown("### 📁 Upload Compounds & Find Similarities in Database")
    uploaded = st.file_uploader("Upload compound file", type=["csv", "txt"], key="sim_upload")
    if uploaded is None:
        return

    try:
        queries = []
        for smi in _read_upload(uploaded):
            m = Chem.MolFromSmiles(smi)
            if m:
                queries.append((smi, m))
            else:
                st.warning(f"Invalid SMILES skipped: {smi}")
        if not queries:
            st.warning("No valid molecules found.")
            return

        db_fps, db_mols, db_names = get_database_fps(data, fp_type)

        for smi, qmol in queries:
            qfp = get_fingerprint(qmol, fp_type)
            hits = [(DataStructs.TanimotoSimilarity(qfp, fp), db_names[i], db_mols[i])
                    for i, fp in enumerate(db_fps)]
            hits.sort(key=lambda x: x[0], reverse=True)
            hits = hits[:TOP_N]

            st.markdown(f"### Input Molecule: {smi}")
            st.dataframe(pd.DataFrame([{
                "Name": name, "SMILES": Chem.MolToSmiles(m), "Similarity": f"{sim:.3f}"}
                for sim, name, m in hits]))

            for col, (sim, name, m) in zip(st.columns(len(hits)), hits):
                with col:
                    st.image(Draw.MolToImage(m, size=(200, 200)), caption=f"{name}\nSim: {sim:.3f}")
    except Exception as e:
        st.error(f"Error processing file: {e}")


def _compare_two():
    st.markdown("### 🔍 Compare Two Molecules")
    col1, col2 = st.columns(2)
    with col1:
        smi1 = st.text_input("SMILES 1")
    with col2:
        smi2 = st.text_input("SMILES 2")

    if st.button("Compare SMILES") and smi1 and smi2:
        m1, m2 = Chem.MolFromSmiles(smi1), Chem.MolFromSmiles(smi2)
        if not (m1 and m2):
            st.error("Invalid SMILES entered.")
            return
        score = DataStructs.TanimotoSimilarity(get_fingerprint(m1, "Morgan"),
                                               get_fingerprint(m2, "Morgan"))
        left, right = st.columns(2)
        with left:
            st.image(Draw.MolToImage(m1, size=(300, 300)), caption="Molecule 1")
        with right:
            st.image(Draw.MolToImage(m2, size=(300, 300)), caption="Molecule 2")
        st.markdown(f"### **Similarity score: {score:.3f}**")


def render(data):
    page_header("📊 Advanced Similarity Search", "Find similar compounds using molecular fingerprints")
    display_molecule_input(data, PAGE_KEY)

    st.markdown("### 🧪 Fingerprint Settings")
    fp_type = st.radio("Select fingerprint type:", ["Morgan", "MACCS"], horizontal=True,
                       help="Morgan: Circular fingerprints | MACCS: Predefined keys",
                       key="sim_fp_type")

    _batch_search(data, fp_type)
    _compare_two()
