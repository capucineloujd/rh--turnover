from pydantic import BaseModel, Field


class EmployeeInput(BaseModel):
    id_employee: int = Field(
        description="Identifiant unique de l'employé (clé primaire dans la table `data`)",
    )
    genre: int = Field(
        description="Genre de l'employé. 0 = Homme, 1 = Femme",
        ge=0, le=1,
    )
    annee_experience_totale: int = Field(
        description="Nombre total d'années d'expérience professionnelle (tous employeurs confondus)",
        ge=0,
    )
    satisfaction_employee_environnement: int = Field(
        description="Satisfaction vis-à-vis de l'environnement de travail. 1 = Faible, 2 = Moyen, 3 = Élevé, 4 = Très élevé",
        ge=1, le=4,
    )
    note_evaluation_precedente: int = Field(
        description="Note obtenue lors de la dernière évaluation annuelle. 1 = Faible, 2 = Bonne, 3 = Très bonne, 4 = Excellente",
        ge=1, le=4,
    )
    niveau_hierarchique_poste: int = Field(
        description="Niveau hiérarchique du poste occupé. 1 = Junior, 5 = Directeur",
        ge=1, le=5,
    )
    satisfaction_employee_nature_travail: int = Field(
        description="Satisfaction vis-à-vis de la nature des tâches effectuées. 1 = Faible, 2 = Moyen, 3 = Élevé, 4 = Très élevé",
        ge=1, le=4,
    )
    satisfaction_employee_equipe: int = Field(
        description="Satisfaction vis-à-vis de l'équipe et des relations collègues. 1 = Faible, 2 = Moyen, 3 = Élevé, 4 = Très élevé",
        ge=1, le=4,
    )
    satisfaction_employee_equilibre_pro_perso: int = Field(
        description="Satisfaction vis-à-vis de l'équilibre vie professionnelle / vie personnelle. 1 = Mauvais, 2 = Correct, 3 = Bon, 4 = Excellent",
        ge=1, le=4,
    )
    heure_supplementaires: bool = Field(
        description="L'employé effectue-t-il régulièrement des heures supplémentaires ? true = Oui, false = Non. Variable la plus prédictive du modèle.",
    )
    nombre_participation_pee: int = Field(
        description="Nombre de participations au Plan d'Épargne Entreprise",
        ge=0, le=6,
    )
    nb_formations_suivies: int = Field(
        description="Nombre de formations professionnelles suivies au cours de l'année précédente",
        ge=0, le=6,
    )
    distance_domicile_travail: int = Field(
        description="Distance entre le domicile et le lieu de travail, en kilomètres",
        ge=1,
    )
    niveau_education: int = Field(
        description="Niveau de diplôme obtenu. 1 = Sans diplôme, 2 = Bac, 3 = Bac+2/3, 4 = Bac+5, 5 = Doctorat",
        ge=1, le=5,
    )
    frequence_deplacement: int = Field(
        description="Fréquence des déplacements professionnels. 0 = Aucun, 1 = Occasionnel, 2 = Fréquent",
        ge=0, le=2,
    )
    annees_depuis_la_derniere_promotion: int = Field(
        description="Nombre d'années écoulées depuis la dernière promotion",
        ge=0,
    )
    ratio_revenu_experience: float = Field(
        description="Feature engineerée : revenu_mensuel / annee_experience_totale. "
                    "Représente le revenu mensuel rapporté à l'expérience. "
                    "Si annee_experience_totale = 0, imputer par la médiane du dataset.",
        gt=0,
    )
    ratio_evolution: float = Field(
        description="Feature engineerée : annees_dans_le_poste_actuel / annees_dans_l_entreprise. "
                    "Mesure la stabilité de poste relative à l'ancienneté. "
                    "Mettre 0 si l'employé vient d'arriver (annees_dans_l_entreprise = 0).",
        ge=0,
    )
    ratio_relation_manager: float = Field(
        description="Feature engineerée : annees_sous_responsable_actuel / annees_dans_l_entreprise. "
                    "Mesure la stabilité managériale relative à l'ancienneté. "
                    "Mettre 0 si l'employé vient d'arriver (annees_dans_l_entreprise = 0).",
        ge=0,
    )
    departement_Consulting: int = Field(
        description="1 si l'employé appartient au département Consulting, 0 sinon (Commercial ou Ressources Humaines). "
                    "Variable one-hot encodée — référence : département Commercial.",
        ge=0, le=1,
    )
    statut_marital_Divorcé_e: int = Field(
        description="1 si l'employé est divorcé(e), 0 si célibataire ou marié(e). "
                    "Variable one-hot encodée — référence : Célibataire.",
        ge=0, le=1,
    )
    poste_Consultant: int = Field(
        description="1 si le poste est Consultant, 0 sinon. Variable one-hot encodée.",
        ge=0, le=1,
    )
    poste_Directeur_Technique: int = Field(
        description="1 si le poste est Directeur Technique, 0 sinon. Variable one-hot encodée.",
        ge=0, le=1,
    )
    poste_Manager: int = Field(
        description="1 si le poste est Manager, 0 sinon. Variable one-hot encodée.",
        ge=0, le=1,
    )
    poste_Représentant_Commercial: int = Field(
        description="1 si le poste est Représentant Commercial, 0 sinon. Variable one-hot encodée.",
        ge=0, le=1,
    )
    poste_Tech_Lead: int = Field(
        description="1 si le poste est Tech Lead, 0 sinon. Variable one-hot encodée. "
                    "Si tous les champs poste_* valent 0 : l'employé est Assistant de Direction, "
                    "Cadre Commercial, Ressources Humaines ou Senior Manager "
                    "(postes retirés lors de la sélection de features, importance < 1%).",
        ge=0, le=1,
    )


class PredictionOutput(BaseModel):
    probabilite_depart: float = Field(
        description="Probabilité estimée que l'employé quitte l'entreprise. Score entre 0 et 1.",
    )
    alerte: bool = Field(
        description="true si la probabilité de départ dépasse le seuil de décision (0.535). "
                    "Indique qu'une action de rétention est recommandée.",
    )
