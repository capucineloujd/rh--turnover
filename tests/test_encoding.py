from src.data.loader import load_data
from src.data.preprocessing import preprocess
from src.features.build_features import build_features
from src.features.encoding import encode


def pipeline():
    X, y = build_features(preprocess(load_data()))
    return encode(X), y


# Vérifie que genre est encodé en 0/1
def test_genre_binary():
    X, _ = pipeline()
    assert set(X["genre"].unique()).issubset({0, 1})


# Vérifie que frequence_deplacement est encodé en 0, 1, 2
def test_frequence_deplacement_ordinal():
    X, _ = pipeline()
    assert set(X["frequence_deplacement"].unique()).issubset({0, 1, 2})


# Vérifie que les colonnes one-hot sont bien créées
def test_ohe_columns_created():
    X, _ = pipeline()
    assert any(col.startswith("departement_") for col in X.columns)
    assert any(col.startswith("poste_") for col in X.columns)
    assert any(col.startswith("statut_marital_") for col in X.columns)
    assert any(col.startswith("domaine_etude_") for col in X.columns)


# Vérifie que les colonnes catégorielles brutes ont été supprimées
def test_raw_categorical_columns_dropped():
    X, _ = pipeline()
    assert "departement" not in X.columns
    assert "poste" not in X.columns
    assert "statut_marital" not in X.columns
    assert "domaine_etude" not in X.columns
