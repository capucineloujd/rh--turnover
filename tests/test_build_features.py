from src.data.loader import load_data
from src.data.preprocessing import preprocess
from src.features.build_features import build_features


# Vérifie que les ratios sont bien créés
def test_ratios_created():
    X, y = build_features(preprocess(load_data()))
    assert "ratio_evolution" in X.columns
    assert "ratio_relation_manager" in X.columns
    assert "ratio_revenu_experience" in X.columns


# Vérifie que les colonnes redondantes ou inutiles sont supprimées
def test_columns_dropped():
    X, y = build_features(preprocess(load_data()))
    assert "age" not in X.columns
    assert "revenu_mensuel" not in X.columns
    assert "annees_dans_l_entreprise" not in X.columns


# Vérifie qu'il ne reste aucun NaN dans X
def test_no_nan():
    X, y = build_features(preprocess(load_data()))
    assert X.isna().sum().sum() == 0


# Vérifie que la cible y est bien séparée de X
def test_target_not_in_X():
    X, y = build_features(preprocess(load_data()))
    assert "a_quitte_l_entreprise" not in X.columns
