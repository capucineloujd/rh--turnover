import pytest
from pathlib import Path
from unittest.mock import patch
from src.data.loader import load_data, load_raw_data

# Vérifie que la jointure des 3 CSV produit bien un DataFrame non vide
def test_load_data_not_empty():
    df = load_data()
    assert len(df) > 0

# Vérifie qu'aucune ligne n'est perdue lors de la jointure inner entre les 3 CSV
def test_load_data_no_row_loss():
    sirh, df_eval, sondage = load_raw_data()
    df = load_data()
    assert len(df) == min(len(sirh), len(df_eval), len(sondage))

# Vérifie que les colonnes clés sont bien présentes dans le DataFrame final
def test_columns():
    df = load_data()
    for col in ["id_employee", "a_quitte_l_entreprise", "revenu_mensuel"]:
        assert col in df.columns

# Vérifie qu'une erreur est levée si les fichiers CSV sont introuvables
def test_missing_file_raises_error():
    with patch("src.data.loader.DATA_DIR", Path("/chemin/qui/nexiste/pas")):
        with pytest.raises(FileNotFoundError):
            load_data()
