import streamlit as st
from rdkit import Chem, DataStructs
from rdkit.Chem import Draw, Lipinski, rdFingerprintGenerator
from rdkit.Chem.Scaffolds import MurckoScaffold

from components.molecule_input import display_molecule_input
from components.ui import page_header
from core.state import get_current_molecule

PAGE_KEY = "scaffold"


@st.cache_data(ttl=3600, show_spinner=False)
def generate_scaffolds(_data):
    """Return (scaffold_smiles list, scaffold_mol list) aligned with _data rows."""
    smiles_out, mols_out = [], []
    for smi in _data["smiles"]:
        try:
            m = Chem.MolFromSmiles(str(smi))
            s = MurckoScaffold.GetScaffoldForMol(m) if m else None
            smiles_out.append(Chem.MolToSmiles(s) if s else None)
            mols_out.append(s)
        except Exception:
            smiles_out.append(None)
            mols_out.append(None)
    return smiles_out, mols_out


def render(data):
    page_header("🧩 Scaffold Analysis", "Decompose and analyze molecular scaffolds")
    display_molecule_input(data, PAGE_KEY)

    mol, _ = get_current_molecule()
    if not mol:
        st.warning("No molecule selected")
        return

    try:
        scaffold_mol = MurckoScaffold.GetScaffoldForMol(mol)
    except Exception as e:
        st.error(f"Could not generate scaffold for the selected molecule: {e}")
        return
    if not scaffold_mol:
        st.warning("Could not generate a valid scaffold for the selected molecule.")
        return
    scaffold_smiles = Chem.MolToSmiles(scaffold_mol)

    st.write("### 🏗️ Query Scaffold")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(Draw.MolToImage(scaffold_mol, size=(300, 300)), use_container_width=True)
    with col2:
        st.write("**SMILES**")
        st.code(scaffold_smiles or "(empty scaffold)")
        st.metric("Ring Count", Lipinski.RingCount(scaffold_mol))
        st.metric("Aromatic Rings", Lipinski.NumAromaticRings(scaffold_mol))

    st.write("### 🔍 Similar Scaffolds in Database")
    with st.spinner("Analyzing database scaffolds..."):
        scaf_smiles, scaf_mols = generate_scaffolds(data)
        df = data.copy()
        df["scaffold_smiles"], df["scaffold_mol"] = scaf_smiles, scaf_mols
        df = df[df["scaffold_mol"].notna()].reset_index(drop=True)
        if df.empty:
            st.warning("No valid scaffolds found in database")
            return

        try:
            fpgen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=1024)
            qfp = fpgen.GetFingerprint(scaffold_mol)
            df["similarity"] = df["scaffold_mol"].apply(
                lambda s: DataStructs.TanimotoSimilarity(qfp, fpgen.GetFingerprint(s)))

            for _, row in df.nlargest(5, "similarity").iterrows():
                with st.expander(f"✨ {row['generic_name']} (Similarity: {row['similarity']:.2f})"):
                    c1, c2 = st.columns([1, 3])
                    with c1:
                        st.image(Draw.MolToImage(row["scaffold_mol"], size=(200, 200)))
                    with c2:
                        st.write(f"**Original Compound:** {row['generic_name']}")
                        st.code(f"Scaffold SMILES: {row['scaffold_smiles']}")
                        st.code(f"Full SMILES: {row['smiles']}")
        except Exception as e:
            st.error(f"Error calculating scaffold similarities: {e}")
