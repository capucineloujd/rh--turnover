import pandas as pd


def encode(X: pd.DataFrame) -> pd.DataFrame:
    X_encoded = X.copy()

    # LABEL ENCODING BINAIRE
    # genre : 2 catégories sans ordre --> 0/1 suffit, pas besoin de one-hot
    X_encoded["genre"] = X_encoded["genre"].map({"M": 0, "F": 1}).astype(int)

    # LABEL ENCODING ORDINAL
    # frequence_deplacement : ordre explicite Aucun < Occasionnel < Frequent
    ordre_freq = ["Aucun", "Occasionnel", "Frequent"]
    X_encoded["frequence_deplacement"] = pd.Categorical(
        X_encoded["frequence_deplacement"],
        categories=ordre_freq,
        ordered=True
    ).codes

    # Variables ordinales numériques --> on les remet en int
    cols_ordinales = [
        "niveau_hierarchique_poste",
        "niveau_education",
        "note_evaluation_precedente",
        "satisfaction_employee_environnement",
        "satisfaction_employee_nature_travail",
        "satisfaction_employee_equipe",
        "satisfaction_employee_equilibre_pro_perso",
    ]
    for col in cols_ordinales:
        X_encoded[col] = X_encoded[col].astype(int)

    # ONE-HOT ENCODING
    cols_ohe = ["departement", "statut_marital", "domaine_etude", "poste"]
    X_encoded = pd.get_dummies(X_encoded, columns=cols_ohe, drop_first=True, dtype=int)

    return X_encoded
