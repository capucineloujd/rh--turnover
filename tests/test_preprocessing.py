from src.data.loader import load_data
from src.data.preprocessing import preprocess


# Vérifie que les fautes de frappe dans les noms de colonnes sont corrigées
def test_columns_renamed():
    df = preprocess(load_data())
    assert "nombre_heures_travailless" not in df.columns
    assert "augementation_salaire_precedente" not in df.columns
    assert "annes_sous_responsable_actuel" not in df.columns
    assert "nombre_heures_travaillees" in df.columns
    assert "augmentation_salaire_precedente" in df.columns
    assert "annees_sous_responsable_actuel" in df.columns


# Vérifie que les colonnes inutiles sont bien supprimées
def test_columns_dropped():
    df = preprocess(load_data())
    assert "ayant_enfants" not in df.columns


# Vérifie que les colonnes booléennes ont bien le bon type
def test_boolean_types():
    df = preprocess(load_data())
    assert df["a_quitte_l_entreprise"].dtype == bool
    assert df["heure_supplementaires"].dtype == bool
