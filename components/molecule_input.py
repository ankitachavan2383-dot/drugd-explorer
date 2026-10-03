"""Shared 'select from database / enter SMILES' widget used by many pages."""
import streamlit as st
from rdkit import Chem
from rdkit.Chem import Descriptors, Draw


def display_molecule_input(data, page_key: str):
    """Render the molecule input section.

    Updates st.session_state.selected_mol / selected_smiles and returns the
    chosen input method. `page_key` keeps widget keys unique per page.
    """
    st.markdown("### 🔬 Molecule Input")
    input_method = st.radio(
        "Input Method:",
        ["Select from Database", "Enter SMILES"],
        key=f"input_method_{page_key}",
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        if input_method == "Select from Database":
            compound_name = st.selectbox(
                "Select compound:",
                options=data["generic_name"].unique(),
                index=0,
                key=f"db_select_{page_key}",
            )
            if st.session_state.get(f"last_selected_db_{page_key}") != compound_name:
                selected = data[data["generic_name"] == compound_name].iloc[0]
                st.session_state.selected_smiles = selected["smiles"]
                st.session_state.selected_mol = Chem.MolFromSmiles(selected["smiles"])
                st.session_state[f"last_selected_db_{page_key}"] = compound_name
                st.session_state.last_selected_name = compound_name

        else:  # Enter SMILES
            smiles_text = st.text_input("Enter SMILES:", key=f"smiles_input_{page_key}")
            if smiles_text:
                mol = Chem.MolFromSmiles(smiles_text)
                if mol:
                    st.success("✅ Valid SMILES")
                    st.image(Draw.MolToImage(mol, size=(200, 200)),
                             caption="Input Molecule", use_container_width=True)
                    st.session_state.selected_mol = mol
                    st.session_state.selected_smiles = smiles_text
                    st.session_state[f"last_selected_db_{page_key}"] = None
                else:
                    st.error("❌ Invalid SMILES")
                    st.session_state.selected_mol = None
                    st.session_state.selected_smiles = None

    with col2:
        mol = st.session_state.selected_mol
        if mol:
            st.markdown(f"""
            <div class="molecule-card">
                <h4 style="margin-top:0;">Selected Molecule</h4>
                <p><strong>SMILES:</strong> {st.session_state.selected_smiles}</p>
                <p><strong>MW:</strong> {Descriptors.MolWt(mol):.2f}</p>
                <p><strong>LogP:</strong> {Descriptors.MolLogP(mol):.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Select or enter a molecule to proceed.")

    st.markdown("---")
    return input_method
