"""Dataset download + drug-likeness filtering."""
from io import StringIO

import pandas as pd
import requests
import streamlit as st
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski

SOURCES = [
    "https://www.cureffi.org/wp-content/uploads/2013/10/drugs.txt",
    # TODO: replace with a real backup URL
    "https://raw.githubusercontent.com/your-repo/backup/main/drugs.txt",
]


def _calculate_properties(mol):
    return {
        "mw": Descriptors.MolWt(mol),
        "logp": Descriptors.MolLogP(mol),
        "hbd": Lipinski.NumHDonors(mol),
        "hba": Lipinski.NumHAcceptors(mol),
        "rot_bonds": Lipinski.NumRotatableBonds(mol),
        "tpsa": Descriptors.TPSA(mol),
    }


def _fallback_dataframe():
    return pd.DataFrame({
        "generic_name": ["Aspirin", "Paracetamol"],
        "smiles": ["CC(=O)OC1=CC=CC=C1C(=O)O", "CC(=O)NC1=CC=C(C=C1)O"],
        "mw": [180.16, 151.16],
        "logp": [1.19, 0.49],
        "hbd": [1, 2],
        "hba": [3, 2],
        "rot_bonds": [2, 1],
        "tpsa": [63.6, 49.3],
    })


@st.cache_data(ttl=3600, show_spinner="Loading drug dataset...")
def download_dataset():
    for url in SOURCES:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            df = pd.read_csv(StringIO(response.text), sep="\t")
            df = df[["generic_name", "smiles"]].dropna()

            df["mol"] = df["smiles"].apply(Chem.MolFromSmiles)
            df = df[df["mol"].notna()].copy()

            props = df["mol"].apply(_calculate_properties).apply(pd.Series)
            df = pd.concat([df, props], axis=1)

            druglike = (
                df["mw"].between(150, 600)
                & df["logp"].between(-2, 5)
                & (df["hbd"] <= 5)
                & (df["hba"] <= 10)
                & (df["rot_bonds"] <= 10)
                & (df["tpsa"] <= 150)
            )
            return df[druglike].drop(columns="mol").reset_index(drop=True)
        except Exception as e:
            st.warning(f"Failed to load from {url}: {e}")

    st.error("All data sources failed. Using sample data.")
    return _fallback_dataframe()
