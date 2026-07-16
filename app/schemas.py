from pydantic import BaseModel


class EmployeeInput(BaseModel):
    genre: int
    annee_experience_totale: int
    satisfaction_employee_environnement: int
    note_evaluation_precedente: int
    niveau_hierarchique_poste: int
    satisfaction_employee_nature_travail: int
    satisfaction_employee_equipe: int
    satisfaction_employee_equilibre_pro_perso: int
    heure_supplementaires: bool
    nombre_participation_pee: int
    nb_formations_suivies: int
    distance_domicile_travail: int
    niveau_education: int
    frequence_deplacement: int
    annees_depuis_la_derniere_promotion: int
    ratio_revenu_experience: float
    ratio_evolution: float
    ratio_relation_manager: float
    departement_Consulting: int
    statut_marital_Divorcé_e: int
    poste_Consultant: int
    poste_Directeur_Technique: int
    poste_Manager: int
    poste_Représentant_Commercial: int
    poste_Tech_Lead: int


class PredictionOutput(BaseModel):
    probabilite_depart: float
    alerte: bool
