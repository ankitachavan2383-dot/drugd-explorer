"""Global CSS used by the whole app."""

MAIN_CSS = """
<style>
    body {
        background-image: url('https://images.unsplash.com/photo-1581090700227-1e8e2f6e34b0');
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #4A2E4C;
        line-height: 1.6;
    }
    .stApp { background: rgba(255, 255, 255, 0.85); padding: 1rem; border-radius: 0.5rem; }

    .header {
        background: linear-gradient(135deg, #FFD6E8 0%, #FFB6C1 100%);
        color: white; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;
    }
    .card {
        background: #FFFFFF; border-radius: 0.5rem; padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 1.5rem;
        transition: transform 0.3s ease; border: 1px solid #E0B0C0;
    }
    .card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px rgba(0,0,0,0.1); }

    .stButton>button {
        background: linear-gradient(135deg, #FF6B6B 0%, #E53980 100%);
        color: white; border: none; border-radius: 0.5rem; padding: 0.5rem 1rem;
        transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        transform: translateY(-2px); box-shadow: 0 5px 10px rgba(0,0,0,0.2);
        background: linear-gradient(135deg, #E53980 0%, #FF6B6B 100%);
    }

    .metric {
        background: #FFFFFF; border-radius: 0.5rem; padding: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #E0B0C0;
    }
    .stProgress>div>div>div { background: linear-gradient(90deg, #FF6B6B 0%, #E53980 100%); }

    .molecule-card {
        background: #FFFFFF; border-radius: 0.5rem; padding: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 1rem; border: 1px solid #E0B0C0;
    }
    .molecule-card h4 { color: #E53980; }

    .property-badge {
        display: inline-block; background: #FFD1DC; color: #4A2E4C; padding: 0.25rem 0.5rem;
        border-radius: 1rem; font-size: 0.8rem; margin-right: 0.5rem; margin-bottom: 0.5rem;
        border: 1px solid #E0B0C0;
    }

    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
    .stTabs [data-baseweb="tab"] {
        background: #FFD1DC; color: #4A2E4C; border-radius: 0.5rem 0.5rem 0 0;
        padding: 0.5rem 1rem; transition: all 0.3s ease; border: 1px solid #E0B0C0; border-bottom: none;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF6B6B 0%, #E53980 100%); color: white; border-color: #E53980;
    }

    hr {
        border: none; height: 2px;
        background: linear-gradient(90deg, #E53980 0%, #FFD1DC 50%, #E53980 100%); margin: 1.5rem 0;
    }
    h1, h2, h3, h4, h5, h6 { color: #E53980; }
    p, label, .stMarkdown { color: #4A2E4C; }

    .stAlert { background-color: #FFF0F5; color: #4A2E4C; border-color: #E0B0C0; }
    .stSuccess { background-color: #F0FFF0; color: #4A2E4C; border-color: #C1E1C1; }
    .stError { background-color: #FFF0F5; color: #E53980; border-color: #E53980; }

    [data-testid="stSidebar"] {
        background-image: url('https://images.unsplash.com/photo-1581090700227-1e8e2f6e34b0');
        background-size: cover; background-position: center; color: #4A2E4C;
        padding: 1.5rem; border-right: 2px solid #E0B0C0; box-shadow: 2px 0 10px rgba(0,0,0,0.1);
    }
    [data-testid="stSidebar"] .stRadio [role="radiogroup"] { display: flex; flex-direction: column; gap: 0.5rem; }
    [data-testid="stSidebar"] .stRadio label {
        font-weight: bold; background-color: rgba(255, 255, 255, 0.9); border: 1px solid #E0B0C0;
        padding: 0.8rem 1rem; border-radius: 0.5rem; margin-bottom: 0; display: flex;
        align-items: center; min-height: 3.5rem; color: #4A2E4C; transition: all 0.3s ease;
    }
    [data-testid="stSidebar"] .stRadio label:hover { background-color: #FFD6E8; cursor: pointer; }
    [data-testid="stSidebar"] .stRadio input:checked + div > label {
        background: linear-gradient(135deg, #FF6B6B, #E53980); color: white !important;
        font-weight: 900; box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
</style>
"""
