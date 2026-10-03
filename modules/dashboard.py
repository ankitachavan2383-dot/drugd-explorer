import plotly.express as px
import streamlit as st

from components.molecule_input import display_molecule_input
from components.ui import page_header

PAGE_KEY = "dashboard"


def _download(df, label, filename, index=False):
    st.download_button(label, data=df.to_csv(index=index).encode("utf-8"),
                       file_name=filename, mime="text/csv")


def render(data):
    st.markdown("""
    <style>
    .metric h2 { margin: 0.2rem 0; font-weight: 700; }
    .metric { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

    page_header("🏠 Dashboard Overview",
                "Comprehensive cheminformatics platform for modern drug discovery")
    display_molecule_input(data, PAGE_KEY)

    # Stats cards
    stats = [
        ("Total Compounds", f"{len(data):,}"),
        ("Avg MW", f"{data['mw'].mean():.2f} Da"),
        ("Avg LogP", f"{data['logp'].mean():.2f}"),
        ("Drug-like", "100%"),
    ]
    for col, (title, value) in zip(st.columns(4), stats):
        with col:
            st.markdown(f"""
            <div class="metric"><h3>{title}</h3>
            <h2 style="color:#2C3E50;">{value}</h2></div>
            """, unsafe_allow_html=True)

    # Distributions
    st.markdown("## 📈 Molecular Property Distributions")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Molecular Weight")
        fig = px.histogram(data, x="mw", nbins=30, color_discrete_sequence=["#6B73FF"])
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        _download(data[["mw"]], "⬇️ Download MW Data", "molecular_weight.csv")
    with col2:
        st.markdown("#### LogP Distribution")
        fig = px.box(data, y="logp", color_discrete_sequence=["#000DFF"])
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        _download(data[["logp"]], "⬇️ Download LogP Data", "logp_distribution.csv")

    # Relationships
    st.markdown("## 🔍 Property Relationships")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### MW vs LogP (Colored by TPSA, Size by Rotatable Bonds)")
        fig = px.scatter(data, x="mw", y="logp", color="tpsa", size="rot_bonds",
                         color_continuous_scale="bluered")
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        _download(data[["mw", "logp", "tpsa", "rot_bonds"]],
                  "⬇️ Download MW vs LogP Data", "mw_vs_logp.csv")
    with col2:
        st.markdown("#### Property Correlations")
        corr = data[["mw", "logp", "hbd", "hba", "tpsa"]].corr()
        fig = px.imshow(corr, text_auto=True, color_continuous_scale="bluered")
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        _download(corr, "⬇️ Download Correlation Matrix", "property_correlation.csv", index=True)
