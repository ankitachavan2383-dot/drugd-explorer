"""Structural-alert (PAINS / Brenk / NIH) processing for virtual screening."""
import pandas as pd
import streamlit as st
from rdkit import Chem
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams

_Cat = FilterCatalogParams.FilterCatalogs


def _catalog(kind):
    params = FilterCatalogParams()
    params.AddCatalog(kind)
    return FilterCatalog(params)


@st.cache_data(show_spinner=False)
def process_screening_molecules(df, smiles_col):
    """Parse SMILES and flag structural alerts.

    NOTE: parameter is `df` (not `_df`) so the cache is invalidated when the
    uploaded file changes.
    """
    pains_cat, brenk_cat = _catalog(_Cat.PAINS_A), _catalog(_Cat.BRENK)
    nih_cat, all_cat = _catalog(_Cat.NIH), _catalog(_Cat.ALL)

    mols, smiles, orig_idx, invalid_idx = [], [], [], []
    pains, brenk, nih, matches_txt = [], [], [], []

    for i, smi in enumerate(df[smiles_col]):
        try:
            mol = Chem.MolFromSmiles(str(smi)) if pd.notna(smi) else None
            if mol is None:
                invalid_idx.append(i)
                continue
            mols.append(mol)
            smiles.append(str(smi))
            orig_idx.append(i)
            pains.append(pains_cat.HasMatch(mol))
            brenk.append(brenk_cat.HasMatch(mol))
            nih.append(nih_cat.HasMatch(mol))
            found = all_cat.GetMatches(mol)
            matches_txt.append(
                "; ".join(f"{e.GetProp('FilterSet')}: {e.GetDescription()}" for e in found)
                if found else "None"
            )
        except Exception:
            invalid_idx.append(i)

    return mols, smiles, orig_idx, invalid_idx, pains, brenk, nih, matches_txt
