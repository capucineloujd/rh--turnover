import pandas as pd


def preprocess(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()

    # Suppression des colonnes techniques de jointure
    data = data.drop(columns=["eval_number", "code_sondage"], errors="ignore")

    # Corrections de fautes de frappe dans les noms de colonnes
    data = data.rename(columns={
        "nombre_heures_travailless": "nombre_heures_travaillees",
        "augementation_salaire_precedente": "augmentation_salaire_precedente",
        "annes_sous_responsable_actuel": "annees_sous_responsable_actuel",
    })

    # Suppression de la colonne mal encodée
    data = data.drop(columns=["ayant_enfants"], errors="ignore")

    # Conversion en booléens
    data["a_quitte_l_entreprise"] = data["a_quitte_l_entreprise"] == "Oui"
    data["heure_supplementaires"] = data["heure_supplementaires"] == "Oui"

    # Suppression des colonnes temporaires créées pendant l'exploration
    cols_temporaires = [
        "groupe_distance",
        "groupe_promo",
        "groupe_anne",
        "tranche_age",
        "salaire_groupe",
        "score_satisfaction_arrondi",
        "aug_groupe",
    ]
    data = data.drop(columns=cols_temporaires, errors="ignore")

    return data
