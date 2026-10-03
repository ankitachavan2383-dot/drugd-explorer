import plotly.express as px
import streamlit as st
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from st_aggrid import AgGrid, GridOptionsBuilder

from components.molecule_input import display_molecule_input
from components.ui import page_header

PAGE_KEY = "explorer"


def _filters(data):
    with st.expander("🔍 Advanced Filters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            mw = st.slider("Molecular Weight (Da)", int(data["mw"].min()), int(data["mw"].max()),
                           (150, 500), step=10, key=f"mw_range_{PAGE_KEY}")
            logp = st.slider("LogP Range", float(data["logp"].min()), float(data["logp"].max()),
                             (-1.0, 3.0), step=0.1, key=f"logp_range_{PAGE_KEY}")
        with col2:
            tpsa = st.slider("TPSA (Å²)", int(data["tpsa"].min()), int(data["tpsa"].max()),
                             (20, 120), step=5, key=f"tpsa_range_{PAGE_KEY}")
            rot = st.slider("Max Rotatable Bonds", 0, int(data["rot_bonds"].max()), 5,
                            key=f"rot_bonds_{PAGE_KEY}")
    return data[
        data["mw"].between(*mw) & data["logp"].between(*logp)
        & data["tpsa"].between(*tpsa) & (data["rot_bonds"] <= rot)
    ]


def _table(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(filterable=True, sortable=True, resizable=True,
                                editable=False, wrapText=True, autoHeight=True)
    gb.configure_column("smiles", headerName="SMILES", width=300)
    gb.configure_grid_options(domLayout="normal")
    AgGrid(df, gridOptions=gb.build(), height=400, width="100%", theme="streamlit",
           fit_columns_on_grid_load=False,
           custom_css={".ag-header-cell-label": {"justify-content": "center"},
                       ".ag-cell": {"display": "flex", "align-items": "center"}},
           key=f"aggrid_{PAGE_KEY}")


def _chemical_space(filtered):
    st.markdown("## 📈 Chemical Space Analysis")
    col1, col2 = st.columns([3, 1])
    with col1:
        viz_type = st.radio("Visualization Method:", ["PCA", "t-SNE"], horizontal=True,
                            help="PCA shows global trends, t-SNE shows local clusters",
                            key=f"viz_type_{PAGE_KEY}")
    with col2:
        if st.button("🔄 Generate Visualization", use_container_width=True,
                     key=f"generate_viz_button_{PAGE_KEY}"):
            st.session_state.generate_viz = True

    if not (st.session_state.get("generate_viz") and not filtered.empty):
        return

    with st.spinner("Computing visualization..."):
        features = filtered[["mw", "logp", "tpsa", "hbd", "hba", "rot_bonds"]]
        try:
            if viz_type == "PCA":
                reducer = PCA(n_components=2)
            else:
                perplexity = min(30, len(filtered) - 1)
                if perplexity <= 1:
                    st.warning("Not enough data points for t-SNE. Need at least 2.")
                    st.session_state.generate_viz = False
                    return
                reducer = TSNE(n_components=2, perplexity=perplexity)

            emb = reducer.fit_transform(features)
            fig = px.scatter(
                x=emb[:, 0], y=emb[:, 1], color=filtered["logp"], size=filtered["mw"] / 100,
                hover_name=filtered["generic_name"], color_continuous_scale="bluered",
                labels={"color": "LogP", "size": "MW"},
                title=f"{viz_type} Projection of Chemical Space",
            )
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                              xaxis_title=f"{viz_type}-1", yaxis_title=f"{viz_type}-2")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Visualization failed: {e}")
            st.session_state.generate_viz = False


def render(data):
    page_header("🔍 Drug Explorer", "Browse and filter the compound database")
    display_molecule_input(data, PAGE_KEY)

    st.markdown("## 🗃️ Compound Database")
    filtered = _filters(data)
    st.markdown(f"""
    <div class="card"><h3 style="margin-top:0;">🔬 Found {len(filtered)} matching compounds</h3></div>
    """, unsafe_allow_html=True)
    _table(filtered)
    _chemical_space(filtered)
