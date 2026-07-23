from pydantic import BaseModel, Field


class EmployeeInput(BaseModel):
    model_config = {
        "json_schema_extra": {
            "example": {
                "id_employee": 42,
                "genre": 0,
                "annee_experience_totale": 8,
                "satisfaction_employee_environnement": 2,
                "note_evaluation_precedente": 3,
                "niveau_hierarchique_poste": 2,
                "satisfaction_employee_nature_travail": 2,
                "satisfaction_employee_equipe": 3,
                "satisfaction_employee_equilibre_pro_perso": 1,
                "heure_supplementaires": True,
                "nombre_participation_pee": 2,
                "nb_formations_suivies": 3,
                "distance_domicile_travail": 15,
                "niveau_education": 3,
                "frequence_deplacement": 1,
                "annees_depuis_la_derniere_promotion": 4,
                "ratio_revenu_experience": 625.0,
                "ratio_evolution": 0.6,
                "ratio_relation_manager": 0.4,
                "departement_Consulting": 1,
                "statut_marital_Divorcé_e": 0,
                "poste_Consultant": 1,
                "poste_Directeur_Technique": 0,
                "poste_Manager": 0,
                "poste_Représentant_Commercial": 0,
                "poste_Tech_Lead": 0
            }
        }
    }

    id_employee: int = Field(
        description="Identifiant unique de l'employé (clé primaire dans la table `data`)",
    )
    genre: int = Field(
        description="Genre de l'employé. 0 = Homme, 1 = Femme",
        ge=0, le=1,
    )
    annee_experience_totale: int = Field(
        description="Nombre total d'années d'expérience professionnelle",
        ge=0,
    )
    satisfaction_employee_environnement: int = Field(
        description="Satisfaction vis-à-vis de l'env",
        ge=1, le=4,
    )
    note_evaluation_precedente: int = Field(
        description="Note obtenue lors de la dernière évaluation annuelle",
        ge=1, le=4,
    )
    niveau_hierarchique_poste: int = Field(
        description="Niveau hiérarchique",
        ge=1, le=5,
    )
    satisfaction_employee_nature_travail: int = Field(
        description="Satisfaction vis-à-vis de la nature des tâches",
        ge=1, le=4,
    )
    satisfaction_employee_equipe: int = Field(
        description="Satisfaction vis-à-vis de l'équipe",
        ge=1, le=4,
    )
    satisfaction_employee_equilibre_pro_perso: int = Field(
        description="Satisfaction vis-à-vis de l'équilibre vie pro / vie perso",
        ge=1, le=4,
    )
    heure_supplementaires: bool

    nombre_participation_pee: int = Field(
        ge=0, le=6,
    )
    nb_formations_suivies: int = Field(
        ge=0, le=6,
    )
    distance_domicile_travail: int = Field(
        description="en km",
        ge=1,
    )
    niveau_education: int = Field(
        description="Niveau de diplôme obtenu:1 = Sans diplôme, 2 = Bac, 3 = Bac+2/3, 4 = Bac+5, 5 = Doctorat",
        ge=1, le=5,
    )
    frequence_deplacement: int = Field(
        description="Fréquence des déplacements professionnels:0 = Aucun, 1 = Occasionnel, 2 = Fréquent",
        ge=0, le=2,
    )
    annees_depuis_la_derniere_promotion: int = Field(
        ge=0,
    )
    ratio_revenu_experience: float = Field(
        description="Feature engineerée : revenu_mensuel / annee_experience_totale. "
                    "= Représente le revenu mensuel rapporté à l'expérience "
                    "Si annee_experience_totale = 0, imputer par la médiane du dataset",
        gt=0,
    )
    ratio_evolution: float = Field(
        description="Feature engineerée : annees_dans_le_poste_actuel / annees_dans_l_entreprise "
                    "= Mesure la stabilité de poste relative à l'ancienneté"
                    "0 si l'employé vient d'arriver",
        ge=0,
    )
    ratio_relation_manager: float = Field(
        ge=0,
    )
    departement_Consulting: int = Field(
        ge=0, le=1,
    )
    statut_marital_Divorcé_e: int = Field(
        description="1 si l'employé est divorcé, 0 si célibataire ou marié",
        ge=0, le=1,
    )
    poste_Consultant: int = Field(
        description="1 si le poste est Consultant, 0 sinon",
        ge=0, le=1,
    )
    poste_Directeur_Technique: int = Field(
        ge=0, le=1,
    )
    poste_Manager: int = Field(
        ge=0, le=1,
    )
    poste_Représentant_Commercial: int = Field(
        ge=0, le=1,
    )
    poste_Tech_Lead: int = Field(
        ge=0, le=1,
    )


class PredictionOutput(BaseModel):
    probabilite_depart: float = Field(
        description="Probabilité estimée que l'employé quitte l'entreprise",
    )
    alerte: bool = Field(
        description="true si la probabilité de départ dépasse le seuil de décision"
                    "Indique qu'une action de rétention est recommandée",
    )
