import traceback

import pandas as pd
import streamlit as st
from rdkit import DataStructs
from rdkit import Chem

from components.ui import page_header
from core.chem_utils import FP_TYPES, get_fingerprint
from core.screening_utils import process_screening_molecules

SAMPLE_SMILES = ("smiles,name\nCCO,Ethanol\nCCN,Ethylamine\nC1=CC=CC=C1,Benzene\n"
                 "INVALID_SMILES,BadOne\nCC(=O)OC1=CC=CC=C1C(=O)O,Aspirin")


def _load_upload(uploaded):
    """Return a DataFrame with a 'smiles' column, or None on error."""
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
        if "smiles" not in df.columns:
            st.error("❌ CSV file must contain a column named 'smiles'.")
            return None
        return df
    return pd.DataFrame({"smiles": [line.decode("utf-8").strip() for line in uploaded]})


def _show_alerts(screen_df, smiles, orig_idx, pains, brenk, nih, matches):
    rows = []
    for i, smi in enumerate(smiles):
        row = {"SMILES": smi, "PAINS Alert": pains[i], "Brenk Alert": brenk[i],
               "NIH Alert": nih[i], "All Filter Matches": matches[i]}
        if "name" in screen_df.columns:
            row["Name"] = screen_df.iloc[orig_idx[i]]["name"]
        rows.append(row)
    alert_df = pd.DataFrame(rows)

    st.markdown("---")
    st.write("### 🚨 Structural Alert Screening")
    st.dataframe(alert_df, use_container_width=True, column_config={
        "PAINS Alert": st.column_config.CheckboxColumn("PAINS Alert", help="Matches PAINS filters"),
        "Brenk Alert": st.column_config.CheckboxColumn("Brenk Alert", help="Matches Brenk filters"),
        "NIH Alert": st.column_config.CheckboxColumn("NIH Alert", help="Matches NIH filters"),
        "All Filter Matches": "Matched Filters",
    })

    for col, (label, flags) in zip(st.columns(3), [("PAINS", pains), ("Brenk", brenk), ("NIH", nih)]):
        with col:
            st.metric(f"{label} Alerts", f"{sum(flags)} / {len(flags)}")

    st.download_button("💾 Download Alert Results (CSV)", alert_df.to_csv(index=False).encode("utf-8"),
                       "structural_alerts_results.csv", "text/csv", key="download_alerts")


def _parameters():
    st.markdown("---")
    st.write("### ⚙️ Screening Parameters")
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            fp = st.selectbox("Fingerprint Type", FP_TYPES, key="fp_type_screen")
        with c2:
            thr = st.slider("Similarity Threshold", 0.0, 1.0, 0.7, step=0.05, key="threshold_screen",
                            help="Minimum Tanimoto similarity score to consider a match.")
        with c3:
            mx = st.slider("Max Matches per Query", 1, 50, 10, step=1, key="max_matches_screen",
                           help="Maximum similar compounds retrieved per query molecule.")
    st.markdown("---")
    return fp, thr, mx


def _run_screening(data, screen_df, screen_mols, smiles, orig_idx, pains, brenk, nih,
                   fp_type, threshold, max_matches):
    with st.status(f"Preparing database fingerprints ({fp_type})...", expanded=False) as status:
        db_fps, valid_idx = [], []
        for i, row in data.iterrows():
            fp = get_fingerprint(Chem.MolFromSmiles(str(row["smiles"])), fp_type)
            if fp is not None:
                db_fps.append(fp)
                valid_idx.append(i)
        if not db_fps:
            status.update(label="❌ Could not generate fingerprints for database compounds.", state="error")
            st.error("Failed to generate fingerprints for the database compounds.")
            return
        status.update(label=f"✅ Prepared fingerprints for {len(db_fps)} database compounds.",
                      state="complete")

    db_valid = data.iloc[valid_idx].reset_index(drop=True)
    total = len(screen_mols)
    st.write(f"Screening {total} query molecules against {len(db_fps)} database compounds...")
    bar = st.progress(0, text="Screening progress: 0%")
    results = []

    for i, qmol in enumerate(screen_mols):
        qfp = get_fingerprint(qmol, fp_type)
        if qfp is not None:
            db_valid["similarity"] = DataStructs.BulkTanimotoSimilarity(qfp, db_fps)
            matches = (db_valid[db_valid["similarity"] >= threshold]
                       .sort_values("similarity", ascending=False).head(max_matches))
            qname = screen_df.iloc[orig_idx[i]].get("name", "N/A")
            for m in matches.itertuples():
                results.append({
                    "Query SMILES": smiles[i], "Query Name": qname,
                    "Query PAINS Alert": pains[i], "Query Brenk Alert": brenk[i],
                    "Query NIH Alert": nih[i], "Match Name": m.generic_name,
                    "Match SMILES": m.smiles, "Similarity": m.similarity,
                    "Match MW": m.mw, "Match LogP": m.logp,
                })
        bar.progress((i + 1) / total, text=f"Screening progress: {int((i + 1) / total * 100)}%")
    bar.empty()

    if not results:
        st.warning(f"No matches found above the similarity threshold {threshold:.2f}.")
        return

    results_df = pd.DataFrame(results)
    st.balloons()
    st.success(f"🎉 Screening complete! Found {len(results_df)} matches above threshold {threshold:.2f}.")
    st.write("### Screening Results")
    st.dataframe(
        results_df.sort_values(["Query SMILES", "Similarity"], ascending=[True, False]),
        hide_index=True, use_container_width=True,
        column_config={
            "Similarity": st.column_config.ProgressColumn(
                "Similarity Score", help="Tanimoto similarity", format="%.3f", min_value=0, max_value=1),
            "Query PAINS Alert": st.column_config.CheckboxColumn("Query PAINS Alert"),
            "Query Brenk Alert": st.column_config.CheckboxColumn("Query Brenk Alert"),
            "Query NIH Alert": st.column_config.CheckboxColumn("Query NIH Alert"),
            "Match Name": "Database Match Name",
            "Match SMILES": "Database Match SMILES",
            "Match MW": st.column_config.NumberColumn("Match MW", format="%.2f"),
            "Match LogP": st.column_config.NumberColumn("Match LogP", format="%.2f"),
        })
    st.download_button("💾 Download Screening Results (CSV)", results_df.to_csv(index=False).encode("utf-8"),
                       "virtual_screening_results.csv", "text/csv", key="download_screening")


def render(data):
    page_header("🖥️ Virtual Screening",
                "Screen a list of compounds from an uploaded file against the built-in drug database")
    st.markdown("---")
    st.write("""
    ### 📄 Upload Compounds for Screening
    Upload a CSV or TXT file. CSV files need a column named 'smiles'; TXT files should have one SMILES per line.
    """)
    st.download_button("📥 Download Sample SMILES File (CSV)", data=SAMPLE_SMILES,
                       file_name="sample_screening_smiles.csv", mime="text/csv",
                       key="download_sample_screening")

    uploaded = st.file_uploader("Choose a file (CSV or TXT)", type=["csv", "txt"], key="screening_uploader")
    if not uploaded:
        st.info("Please upload a file to begin.")
        return

    try:
        screen_df = _load_upload(uploaded)
        if screen_df is None:
            return
        st.success(f"✅ Loaded '{uploaded.name}'. Found {len(screen_df)} rows.")
        st.dataframe(screen_df.head(), use_container_width=True)

        with st.status("Processing molecules from file...", expanded=True) as status:
            (mols, smiles, orig_idx, invalid_idx,
             pains, brenk, nih, matches) = process_screening_molecules(screen_df, "smiles")
            if not mols:
                status.update(label="❌ No valid molecules found in the uploaded file.", state="error")
                st.error("No valid molecules could be processed. Please check the SMILES strings.")
                return
            status.update(label=f"✅ Processed {len(mols)} molecules. {len(invalid_idx)} invalid/skipped.",
                          state="complete")

        _show_alerts(screen_df, smiles, orig_idx, pains, brenk, nih, matches)
        fp_type, threshold, max_matches = _parameters()

        if st.button("🚀 Start Virtual Screening", key="start_screening", type="primary",
                     use_container_width=True):
            _run_screening(data, screen_df, mols, smiles, orig_idx, pains, brenk, nih,
                           fp_type, threshold, max_matches)
    except Exception as e:
        st.error(f"An unexpected error occurred during virtual screening: {e}")
        st.write(traceback.format_exc())
