import streamlit as st
from rdkit import Chem

from components.molecule_input import display_molecule_input
from components.ui import page_header
from core.chem_utils import admet_properties
from core.state import get_current_molecule

PAGE_KEY = "admet"

TOXIC_GROUPS = {
    "Sulfonyl halide": "[S;D1](=O)(=O)[Cl,Br,I,F]",
    "Anhydride": "C(=O)OC(=O)",
    "Azo": "N=N",
    "Carbamate": "[NH2]C(=O)O",
    "Sulfonate": "[S;D2]([#6])(=O)(=O)",
}


def _druglikeness(p):
    st.write("### Drug-likeness Rules")
    rules = {
        "Lipinski's Rule of 5": [
            ("MW < 500", p["mw"] < 500), ("LogP < 5", p["logp"] < 5),
            ("HBD ≤ 5", p["hbd"] <= 5), ("HBA ≤ 10", p["hba"] <= 10)],
        "Ghose Filter": [
            ("-0.4 < LogP < 5.6", -0.4 < p["logp"] < 5.6), ("160 < MW < 480", 160 < p["mw"] < 480),
            ("40 < Atoms < 70", 40 < p["heavy_atoms"] < 70), ("MR 40-130", 40 < p["mr"] < 130)],
        "Veber's Rule": [
            ("Rot. Bonds ≤ 10", p["rot_bonds"] <= 10), ("TPSA ≤ 140", p["tpsa"] <= 140)],
    }
    total = sum(len(c) for c in rules.values())
    passed_total = 0
    for name, conds in rules.items():
        passed = sum(1 for _, ok in conds if ok)
        passed_total += passed
        st.metric(f"{name} ({passed}/{len(conds)})",
                  "✅ Passed" if passed == len(conds) else "⚠️ Review",
                  help="\n".join(f"{n}: {'✔' if ok else '✖'}" for n, ok in conds))

    score = passed_total / total
    label = "Excellent" if score > 0.8 else "Good" if score > 0.6 else "Poor" if score > 0.3 else "Very Poor"
    st.progress(score, text=f"Overall Drug-likeness: {label}")


def _absorption(p):
    st.write("### Absorption Potential")
    bio = sum([p["mw"] < 500, -0.4 < p["logp"] < 5.6, p["tpsa"] < 140, p["rot_bonds"] <= 10])
    st.metric("Bioavailability Score", f"{bio}/4")

    # Simplified model
    logs = 0.16 - 0.63 * p["logp"] - 0.0062 * p["mw"] + 0.066 * p["tpsa"] - 0.74 * p["rot_bonds"]
    st.metric("Predicted LogS", f"{logs:.2f}", "Good" if logs > -4 else "Poor")


def _toxicity(mol, p):
    st.write("### Toxicity Assessment")
    found = []
    for name, smarts in TOXIC_GROUPS.items():
        try:
            if mol.HasSubstructMatch(Chem.MolFromSmarts(smarts)):
                found.append(name)
        except Exception as e:
            st.warning(f"Could not check toxicophore {name}: {e}")

    if found:
        st.error(f"Toxicophores detected: {', '.join(found)}")
    else:
        st.success("✅ No toxicophores detected")

    # Simplified model
    ld50 = 2.5 - 0.5 * p["logp"] - 0.01 * p["mw"] + 0.05 * p["tpsa"]
    st.metric("Estimated LD50", f"{ld50:.1f}", "Toxicity concern" if ld50 < 2 else "Normal range")


def _bbb(p):
    st.write("### Blood-Brain Barrier")
    score = sum([1 <= p["logp"] <= 3, p["mw"] <= 400, p["tpsa"] < 90,
                 p["hbd"] <= 3, p["charge"] == 0])
    st.metric("BBB Score", f"{score}/5",
              "High penetration" if score >= 4 else "Moderate" if score >= 2 else "Low")


def render(data):
    page_header("💊 ADMET Prediction",
                "Predict Absorption, Distribution, Metabolism, Excretion, and Toxicity properties")
    display_molecule_input(data, PAGE_KEY)

    mol, _ = get_current_molecule()
    if not mol:
        st.warning("No molecule selected")
        return

    try:
        props = admet_properties(mol)
    except Exception as e:
        st.error(f"Error calculating basic properties: {e}")
        return

    tab1, tab2, tab3, tab4 = st.tabs(["💊 Drug-likeness", "🚀 Absorption", "☠️ Toxicity", "🧠 BBB"])
    with tab1:
        _druglikeness(props)
    with tab2:
        _absorption(props)
    with tab3:
        _toxicity(mol, props)
    with tab4:
        _bbb(props)
