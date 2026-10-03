import numpy as np
import streamlit as st
from rdkit import Chem
from rdkit.Chem import Descriptors, Draw, Lipinski

from components.molecule_input import display_molecule_input
from components.ui import page_header
from core.state import get_current_molecule

PAGE_KEY = "optimization"

TOXIC_ALERTS = {
    "Nitroso": "[N](=O)",
    "Michael Acceptor": "C=CC=O",
    "Aniline": "c1ccc(cc1)N",
}

BIOISOSTERES = {
    "[C](=O)[O-]": ["SO₃H", "PO₃H₂", "Tetrazole"],   # carboxylate
    "c1ccccc1": ["Pyridyl", "Thiophene", "Imidazole"],  # phenyl
    "[OH]": ["NH₂", "F", "CONH₂"],                    # hydroxyl
    "[NH2]": ["[OH]", "CH₃"],                         # amine
}


def _has(mol, smarts):
    return mol.HasSubstructMatch(Chem.MolFromSmarts(smarts))


def render(data):
    page_header("⚗️ Compound Optimization", "Get suggestions for improving drug properties")
    display_molecule_input(data, PAGE_KEY)

    mol, _ = get_current_molecule()
    if not mol:
        st.warning("No molecule selected")
        return

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(Draw.MolToImage(mol, size=(300, 300)), use_container_width=True)

    try:
        props = {
            "MW": Descriptors.MolWt(mol), "LogP": Descriptors.MolLogP(mol),
            "HBD": Lipinski.NumHDonors(mol), "HBA": Lipinski.NumHAcceptors(mol),
        }
    except Exception as e:
        st.error(f"Error calculating properties for optimization: {e}")
        return

    lipinski = {
        "MW <500": props["MW"] < 500, "LogP <5": props["LogP"] < 5,
        "HBD ≤5": props["HBD"] <= 5, "HBA ≤10": props["HBA"] <= 10,
    }
    with col2:
        st.metric("Molecular Weight", f"{props['MW']:.1f}")
        st.metric("LogP", f"{props['LogP']:.2f}")
        st.metric("Lipinski Compliance", f"{sum(lipinski.values())}/4",
                  help="\n".join(f"{k}: {'✔' if v else '✖'}" for k, v in lipinski.items()))

    # Toxicophores
    toxic = []
    for name, smarts in TOXIC_ALERTS.items():
        try:
            if _has(mol, smarts):
                toxic.append(name)
        except Exception as e:
            st.warning(f"Could not check toxicophore {name}: {e}")
    if toxic:
        st.error(f"⚠️ Potential Toxicophores: {', '.join(toxic)}")
    else:
        st.success("✅ No common toxicophores detected")

    # Bioisosteres
    st.markdown("### 🔄 Bioisostere Suggestions")
    st.caption("Suggested replacements for common functional groups based on bioisosterism principles.")
    found = False
    for smarts, repl in BIOISOSTERES.items():
        try:
            if _has(mol, smarts):
                st.markdown(f"<div class='card'><b>{smarts}</b> group found. "
                            f"Consider replacing with: {', '.join(repl)}</div>", unsafe_allow_html=True)
                found = True
        except Exception as e:
            st.warning(f"Could not check for bioisostere {smarts}: {e}")
    if not found:
        st.info("No common bioisosteric groups found in the molecule.")

    # Tips
    st.markdown("### 🧠 Optimization Tips")
    st.caption("General strategies for improving drug-like properties.")
    st.markdown("""
    <div class="card"><ul>
        <li><b>Solubility</b>: Increase polarity (e.g., add OH, NH, COOH), reduce LogP, reduce MW.</li>
        <li><b>Permeability</b>: Reduce TPSA, reduce HBD, maintain LogP in optimal range (1-3).</li>
        <li><b>Metabolic Stability</b>: Replace metabolically labile groups (e.g., esters, amides, ethers) with more stable bioisosteres. Consider deuteration.</li>
        <li><b>Synthetic Ease</b>: Aim for simpler structures (fewer chiral centers, fewer complex rings), keep heavy atom count reasonable (&lt;~35).</li>
        <li><b>Toxicity</b>: Remove toxicophores, modify reactive functional groups.</li>
    </ul></div>
    """, unsafe_allow_html=True)
