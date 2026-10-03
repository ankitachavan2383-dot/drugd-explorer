import traceback

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, Draw, Lipinski

from components.molecule_input import display_molecule_input
from components.ui import page_header
from core.chem_utils import FP_TYPES, fp_to_array, get_fingerprint
from core.state import get_current_molecule

PAGE_KEY = "calculator"

_CSS = """
<style>
    .property-card { background-color: #f8f9fa; padding: 20px; border-radius: 10px;
                     box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .property-card .title { font-size: 18px; font-weight: bold; }
    .property-card .value { font-size: 22px; color: #007bff; }
    .property-card .unit  { font-size: 16px; color: #6c757d; }
</style>
"""


# ---------- Tab 1 ----------
def _basic_properties(mol):
    st.write("### Molecular Properties")
    props = [
        ("Molecular Weight", f"{Descriptors.MolWt(mol):.2f}", "g/mol", "⚖️"),
        ("Exact Mass", f"{Descriptors.ExactMolWt(mol):.4f}", "", "🧮"),
        ("LogP", f"{Descriptors.MolLogP(mol):.2f}", "", "📈"),
        ("TPSA", f"{Descriptors.TPSA(mol):.2f}", "Å²", "📐"),
        ("H-Bond Donors", Lipinski.NumHDonors(mol), "", "💧"),
        ("H-Bond Acceptors", Lipinski.NumHAcceptors(mol), "", "💦"),
        ("Rotatable Bonds", Lipinski.NumRotatableBonds(mol), "", "🔄"),
        ("Ring Count", Lipinski.RingCount(mol), "", "⭕"),
        ("Aromatic Rings", Lipinski.NumAromaticRings(mol), "", "🔴"),
        ("Fraction CSP3", f"{Lipinski.FractionCSP3(mol):.2f}", "", "🔶"),
        ("Formal Charge", Chem.GetFormalCharge(mol), "", "⚡"),
    ]
    for name, value, unit, icon in props:
        st.markdown(f"""
        <div class="property-card">
            <div class="title">{icon} {name}</div>
            <div class="value">{value} {unit}</div>
        </div>
        """, unsafe_allow_html=True)


# ---------- Tab 2 ----------
def _advanced_descriptors(mol):
    st.write("### Advanced Descriptors")
    try:
        from mordred import Calculator, descriptors  # heavy import, load lazily

        if not hasattr(np, "float"):
            np.float = float  # compat shim for old mordred

        try:
            values = Calculator(descriptors)(mol)
            desc_df = pd.DataFrame.from_dict(
                {str(k): str(v) for k, v in values.items() if v is not None},
                orient="index", columns=["Value"])
        except Exception as e:
            st.error(f"Error during descriptor calculation: {e}")
            desc_df = pd.DataFrame(columns=["Value"])

        desc_class = st.selectbox(
            "Filter by:", ["All", "Topological", "Geometrical", "Electronic", "Constitutional"],
            key=f"desc_filter_{PAGE_KEY}")
        if desc_class != "All":
            desc_df = desc_df[desc_df.index.str.lower().str.startswith(desc_class[:3].lower(), na=False)]
        st.dataframe(desc_df, use_container_width=True, height=400)
    except Exception as e:
        st.error(f"Descriptor calculation setup failed: {e}")


# ---------- Tab 3 ----------
def _viewer_3d(mol):
    st.write("### 2D and 3D Molecular Viewer")
    st.write("Visualize the 2D structure and an estimated 3D conformation.")
    col1, col2 = st.columns(2)

    with col1:
        st.write("#### 2D Structure")
        try:
            st.image(Draw.MolToImage(mol, size=(400, 300)), use_container_width=True,
                     caption="2D Depiction")
        except Exception as e:
            st.warning(f"Could not generate 2D image: {e}")

    with col2:
        st.write("#### 3D Structure (Estimated)")
        st.caption("Note: 3D conformation is an estimate using UFF optimization "
                   "and may not represent the lowest energy state.")
        try:
            mol_3d = Chem.AddHs(mol)
            if AllChem.EmbedMolecule(mol_3d, AllChem.ETKDG()) == -1:
                st.warning("Could not generate 3D coordinates with ETKDG. Trying random coordinates.")
                if AllChem.EmbedMolecule(mol_3d, useRandomCoords=True) == -1:
                    st.error("Could not generate 3D coordinates for this molecule.")
                    return
            AllChem.UFFOptimizeMolecule(mol_3d)
            molblock = Chem.MolToMolBlock(mol_3d)

            components.html(f"""
                <div id='viewer_3d' style='height:350px;width:100%'></div>
                <script src='https://3Dmol.csb.pitt.edu/build/3Dmol-min.js'></script>
                <script>
                let viewer = $3Dmol.createViewer("viewer_3d", {{backgroundColor:"white"}});
                viewer.addModel(`{molblock}`, "mol");
                viewer.setStyle({{}}, {{stick:{{}}}});
                viewer.zoomTo();
                viewer.render();
                </script>
            """, height=370)

            name = st.session_state.get("last_selected_name", "molecule")
            st.download_button("📥 Download 3D Structure (MolBlock)", data=molblock,
                               file_name=f"{name}_3d.mol", mime="chemical/x-mdl-molfile",
                               key="download_3d_molblock")
        except Exception as e:
            st.error(f"3D visualization failed: {e}")
            st.write(traceback.format_exc())


# ---------- Tab 4 ----------
def _fp_params(fp_type, key_suffix=""):
    radius, n_bits = 2, 1024
    if fp_type == "Morgan":
        radius = st.slider("Radius", 1, 5, 2, key=f"radius{key_suffix}")
        n_bits = st.slider("Number of bits", 64, 4096, 1024, step=64, key=f"bits{key_suffix}")
    return radius, n_bits


def _fingerprints_single(mol):
    st.success(f"Analyzing: {Chem.MolToSmiles(mol)}")
    col1, col2 = st.columns(2)
    with col1:
        fp_type = st.selectbox("Fingerprint type", FP_TYPES, key="fp_type_single")
    with col2:
        radius, n_bits = _fp_params(fp_type, "_single")

    fp = get_fingerprint(mol, fp_type, radius, n_bits)
    arr = fp_to_array(fp)

    st.write("### 🔍 Fingerprint Results")
    st.write(f"**Type:** {fp_type} | **Bits:** {len(arr)} | **Set bits:** {int(arr.sum())}")

    fig, ax = plt.subplots(figsize=(10, 1.5))
    ax.imshow(arr.reshape(1, -1), cmap="viridis", aspect="auto")
    ax.set_yticks([])
    ax.set_xlabel("Bit Position")
    st.pyplot(fig)

    st.download_button("📥 Download Fingerprint (CSV)",
                       data=pd.DataFrame(arr).to_csv(index=False, header=False).encode("utf-8"),
                       file_name=f"fingerprint_{fp_type}.csv", mime="text/csv")


def _fingerprints_batch():
    st.info("Upload a CSV/TSV file containing SMILES strings")
    uploaded = st.file_uploader("Choose a file", type=["csv", "tsv"], key="batch_uploader")
    if not uploaded:
        return
    st.success(f"Processing {uploaded.name}")

    try:
        df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_csv(uploaded, sep="\t")
        smiles_col = st.selectbox("Select SMILES column", df.columns, key="smiles_col")
        fp_type = st.selectbox("Fingerprint type", FP_TYPES, key="fp_type_batch")
        radius, n_bits = _fp_params(fp_type, "_batch")

        with st.spinner("Generating fingerprints..."):
            rows, arrays = [], []
            for idx, smi in df[smiles_col].items():
                m = Chem.MolFromSmiles(str(smi))
                fp = get_fingerprint(m, fp_type, radius, n_bits)
                if fp is not None:
                    rows.append(idx)
                    arrays.append(fp_to_array(fp))

            if not rows:
                st.error("No valid molecules found in the file!")
                return
            st.success(f"Generated fingerprints for {len(rows)} molecules")

            fp_df = pd.DataFrame(np.vstack(arrays),
                                 columns=[f"Bit_{i}" for i in range(len(arrays[0]))], index=rows)
            output_df = pd.concat([df.loc[rows], fp_df], axis=1)  # aligned on valid rows only

            st.write("### Results Preview")
            st.dataframe(output_df.head(3))
            st.download_button("📥 Download Full Results (CSV)",
                               data=output_df.to_csv(index=False).encode("utf-8"),
                               file_name=f"batch_fingerprints_{fp_type}.csv", mime="text/csv")
    except Exception as e:
        st.error(f"Error processing file: {e}")


def _fingerprints_tab(mol):
    st.write("## 🧬 Molecular Fingerprint Generator")
    mode = st.radio("Select input type:", ["Single Molecule", "Batch Processing (CSV/TSV)"],
                    horizontal=True, key=f"fp_analysis_type_{PAGE_KEY}")
    if mode == "Single Molecule":
        _fingerprints_single(mol)
    else:
        _fingerprints_batch()


def render(data):
    st.markdown(_CSS, unsafe_allow_html=True)
    page_header("🧮 Molecular Property Calculator", "Calculate various physicochemical descriptors")
    display_molecule_input(data, PAGE_KEY)

    mol, _ = get_current_molecule()
    if not mol:
        st.warning("No molecule selected")
        return

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 Basic Properties", "📊 Advanced Descriptors", "🖼️ 2D/3D Viewer", "🔢 Fingerprints"])
    with tab1:
        _basic_properties(mol)
    with tab2:
        _advanced_descriptors(mol)
    with tab3:
        _viewer_3d(mol)
    with tab4:
        _fingerprints_tab(mol)
