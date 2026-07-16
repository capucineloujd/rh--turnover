import pandas as pd
from catboost import CatBoostClassifier


# Colonnes supprimées lors de la sélection de features (faible importance)
FEATURES_A_SUPPRIMER = [
    'poste_Cadre Commercial',
    'domaine_etude_Entrepreunariat',
    'domaine_etude_Infra & Cloud',
    'domaine_etude_Marketing',
    'poste_Senior Manager',
    'domaine_etude_Transformation Digitale',
    'domaine_etude_Ressources Humaines',
    'statut_marital_Marié(e)',
    'departement_Ressources Humaines',
    'poste_Ressources Humaines',
]


def select_features(X: pd.DataFrame) -> pd.DataFrame:
    cols_a_supprimer = [c for c in FEATURES_A_SUPPRIMER if c in X.columns]
    return X.drop(columns=cols_a_supprimer)


def train(X_train: pd.DataFrame, y_train: pd.Series) -> CatBoostClassifier:
    model = CatBoostClassifier(
        iterations=100,
        depth=3,
        learning_rate=0.05,
        l2_leaf_reg=5,
        subsample=1.0,
        scale_pos_weight=5.19,
        random_seed=42,
        verbose=0,
    )
    model.fit(X_train, y_train)
    return model
