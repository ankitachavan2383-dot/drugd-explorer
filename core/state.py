"""Session-state helpers."""
import streamlit as st

_DEFAULTS = {
    "selected_mol": None,
    "selected_smiles": None,
    "generate_viz": False,
}


def init_session_state():
    for key, value in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_current_molecule():
    """Return (mol, smiles) currently selected by the user."""
    return st.session_state.selected_mol, st.session_state.selected_smiles
