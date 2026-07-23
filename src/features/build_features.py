import numpy as np
import pandas as pd

def build_features(data):

    y = data["a_quitte_l_entreprise"]

    # 1. RATIOS (calculés avant tout drop, on a besoin des colonnes sources)
    def ratio(a, b):
        return data[a] / data[b].replace(0, np.nan)

    ratios = pd.DataFrame({
        "ratio_revenu_experience" : ratio("revenu_mensuel",                "annee_experience_totale"),
        "ratio_evolution"         : ratio("annees_dans_le_poste_actuel",   "annees_dans_l_entreprise"),
        "ratio_relation_manager"  : ratio("annees_sous_responsable_actuel","annees_dans_l_entreprise"),
    }, index=data.index)

    #2. IMPUTATION des NaN dans les ratios 
    # ratio_evolution et ratio_relation_manager : NaN quand annees_dans_l_entreprise = 0
    # --> ces employés viennent d'arriver : aucune évolution de poste ni relation manager établie
    # --> imputer à 0 est sémantiquement correct (ratio nul = pas encore de recul)
    ratios["ratio_evolution"]        = ratios["ratio_evolution"].fillna(0)
    ratios["ratio_relation_manager"] = ratios["ratio_relation_manager"].fillna(0)

    # ratio_revenu_experience : NaN quand annee_experience_totale = 0
    # --> on ne peut pas dire qu'un salaire sans expérience vaut 0 (ce serait faux : ils sont payés)
    # --> on impute par la médiane : valeur centrale robuste aux outliers salariaux
    mediane_ratio_revenu = ratios["ratio_revenu_experience"].median()
    ratios["ratio_revenu_experience"] = ratios["ratio_revenu_experience"].fillna(mediane_ratio_revenu)

    # 3. DROP des colonnes inutiles / redondantes / sources des ratios
    cols_a_supprimer = [
        # cible
        "a_quitte_l_entreprise",
        # constantes (variance nulle)
        "nombre_heures_travaillees", "nombre_employee_sous_responsabilite",
        # colonnes d'exploration créées en cours d'analyse
        "id_employee", "score_satisfaction_arrondi", "score_satisfaction_global",
        "groupe_distance", "groupe_promo", "groupe_anne",
        "salaire_groupe", "aug_groupe", "tranche_age",
        # faible pouvoir prédictif (r =env 0, p non significatif)
        "age", "note_evaluation_actuelle",
        "augmentation_salaire_precedente", "nombre_experiences_precedentes",
        # redondantes avec les ratios
        "revenu_mensuel",
        "annees_dans_l_entreprise", "annees_dans_le_poste_actuel", "annees_sous_responsable_actuel",
    ]
    X = data.drop(columns=cols_a_supprimer, errors="ignore")

    # 4. VARIABLES CATÉGORIELLES
    # Nominales (pas d'ordre entre les modalités)
    cols_nominales = [
        "genre", "statut_marital", "departement", "poste", "domaine_etude", "frequence_deplacement",
    ]
    # Ordinales
    cols_ordinales = [
        "niveau_hierarchique_poste",
        "niveau_education",
        "note_evaluation_precedente",
        "satisfaction_employee_environnement",
        "satisfaction_employee_nature_travail",
        "satisfaction_employee_equipe",
        "satisfaction_employee_equilibre_pro_perso",
    ]
    X = X.copy()
    for col in cols_nominales + cols_ordinales:
        X[col] = X[col].astype("category")

    # 5. AJOUT des ratios
    X = pd.concat([X, ratios], axis=1)

    return X, y
