"""Reusable cheminformatics helpers (fingerprints, properties)."""
import numpy as np
from rdkit import Chem, DataStructs
from rdkit.Chem import Crippen, Descriptors, Lipinski, MACCSkeys, rdFingerprintGenerator

FP_TYPES = ["Morgan", "MACCS", "RDKit"]


def get_fingerprint(mol, fp_type="Morgan", radius=2, n_bits=1024):
    """Single place that builds a fingerprint. Returns None on failure."""
    if mol is None:
        return None
    try:
        if fp_type == "Morgan":
            gen = rdFingerprintGenerator.GetMorganGenerator(radius=radius, fpSize=n_bits)
            return gen.GetFingerprint(mol)
        if fp_type == "MACCS":
            return MACCSkeys.GenMACCSKeys(mol)
        if fp_type == "RDKit":
            return Chem.RDKFingerprint(mol)
    except Exception:
        return None
    return None


def fp_to_array(fp):
    arr = np.zeros((1,))
    DataStructs.ConvertToNumpyArray(fp, arr)
    return arr


def get_database_fps(data, fp_type):
    """Return aligned lists (fps, mols, names) for rows with a valid fingerprint."""
    fps, mols, names = [], [], []
    for _, row in data.iterrows():
        smi = row["smiles"]
        mol = Chem.MolFromSmiles(smi)
        fp = get_fingerprint(mol, fp_type)
        if fp is not None:
            fps.append(fp)
            mols.append(mol)
            names.append(row.get("generic_name", smi))
    return fps, mols, names


def admet_properties(mol):
    return {
        "mw": Descriptors.MolWt(mol),
        "logp": Descriptors.MolLogP(mol),
        "hbd": Lipinski.NumHDonors(mol),
        "hba": Lipinski.NumHAcceptors(mol),
        "tpsa": Descriptors.TPSA(mol),
        "rot_bonds": Descriptors.NumRotatableBonds(mol),
        "mr": Crippen.MolMR(mol),
        "heavy_atoms": mol.GetNumHeavyAtoms(),
        "charge": Chem.GetFormalCharge(mol),
    }
