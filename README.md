# 🧪 DrugD Explorer

**Streamlit-based cheminformatics platform for exploring drug candidates, with similarity search, ADMET prediction, scaffold analysis and virtual screening, built on RDKit.**

![Python](https://img.shields.io/badge/python-3.11-blue)
![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-FF4B4B)
![RDKit](https://img.shields.io/badge/cheminformatics-RDKit-green)

---

## 📖 Overview

DrugD Explorer is a web-based toolkit that helps researchers explore drug-like compounds, calculate molecular properties, find structurally similar molecules and screen compounds for structural alerts, all in one interface.

It ships with a built-in library of drug-like compounds (filtered by Lipinski-style rules) and also accepts your own SMILES lists as CSV/TXT files.

## ✨ Features

| Module | What it does |
|---|---|
| **Dashboard Overview** | Summary statistics and interactive plots of property distributions and correlations |
| **Drug Explorer** | Filter the compound database by MW, LogP, TPSA and rotatable bonds; PCA / t-SNE chemical space map |
| **Molecular Property Calculator** | Basic properties, Mordred descriptors, 2D/3D viewer, fingerprints (single and batch) |
| **Advanced Similarity Search** | Tanimoto similarity with Morgan or MACCS fingerprints; batch upload; two-molecule comparison |
| **ADMET Prediction** | Lipinski / Ghose / Veber rules, absorption, toxicophore check, blood-brain barrier score |
| **Scaffold Analysis** | Murcko scaffold extraction and similar-scaffold search in the database |
| **Virtual Screening** | Upload a library, flag PAINS / Brenk / NIH alerts, find similar database compounds |
| **Compound Optimization** | Lipinski compliance, toxicophore alerts, bioisostere suggestions, optimization tips |

> ⚠️ The solubility (LogS), LD50 and BBB values are **simplified heuristic models** for teaching and quick triage. They are not validated predictors and should not replace experimental data or dedicated ADMET tools.

## 🗂️ Project Structure

```
drugd-explorer/
├── app.py                      # Entry point: page config, CSS, sidebar, routing
├── requirements.txt
├── config/
│   └── styles.py               # Global CSS
├── core/
│   ├── state.py                # Session-state helpers
│   ├── data_loader.py          # Dataset download and drug-like filtering
│   ├── chem_utils.py           # Fingerprints and property helpers
│   └── screening_utils.py      # PAINS / Brenk / NIH alert processing
├── components/
│   ├── ui.py                   # Page header component
│   └── molecule_input.py       # Shared molecule input widget
└── modules/                    # One file per page, each exposing render(data)
    ├── home.py
    ├── dashboard.py
    ├── explorer.py
    ├── property_calculator.py
    ├── similarity.py
    ├── admet.py
    ├── scaffold.py
    ├── virtual_screening.py
    ├── optimization.py
    └── about.py
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11 (recommended for RDKit and Mordred compatibility)
- An internet connection (the dataset and 3D viewer library are loaded online)

### Installation

```bash
git clone https://github.com/username/drugd-explorer.git
cd drugd-explorer

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Run

```bash
streamlit run app.py
```

The app opens at <http://localhost:8501>.

## 📂 Input File Formats

**Virtual Screening / Similarity Search**
- **CSV:** must contain a `smiles` column (Virtual Screening) or `SMILES` column (Similarity Search); an optional `name` column is used for labelling
- **TXT:** one SMILES string per line

Example:

```csv
smiles,name
CCO,Ethanol
CC(=O)OC1=CC=CC=C1C(=O)O,Aspirin
```

A sample file can be downloaded from the Virtual Screening page.

## ☁️ Deployment

**Streamlit Community Cloud**
1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **Create app**.
3. Select the repo, set the main file to `app.py`, and choose **Python 3.11** under Advanced settings.
4. Deploy.

**Docker**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🛠️ Built With

- [Streamlit](https://streamlit.io/): web interface
- [RDKit](https://www.rdkit.org/): cheminformatics engine
- [Mordred](https://github.com/JacksonBurns/mordred-community): molecular descriptors
- [Pandas](https://pandas.pydata.org/) and [scikit-learn](https://scikit-learn.org/): data handling, PCA, t-SNE
- [Plotly](https://plotly.com/python/) and [Matplotlib](https://matplotlib.org/): visualization
- [3Dmol.js](https://3dmol.csb.pitt.edu/): in-browser 3D molecule viewer
- [streamlit-aggrid](https://github.com/PablocFonseca/streamlit-aggrid): interactive tables

