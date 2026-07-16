from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID_EMPLOYEE = {
    "genre": 0,
    "annee_experience_totale": 5,
    "satisfaction_employee_environnement": 3,
    "note_evaluation_precedente": 3,
    "niveau_hierarchique_poste": 2,
    "satisfaction_employee_nature_travail": 3,
    "satisfaction_employee_equipe": 3,
    "satisfaction_employee_equilibre_pro_perso": 3,
    "heure_supplementaires": False,
    "nombre_participation_pee": 2,
    "nb_formations_suivies": 2,
    "distance_domicile_travail": 10,
    "niveau_education": 3,
    "frequence_deplacement": 1,
    "annees_depuis_la_derniere_promotion": 2,
    "ratio_revenu_experience": 1200.0,
    "ratio_evolution": 0.5,
    "ratio_relation_manager": 0.4,
    "departement_Consulting": 0,
    "statut_marital_Divorcé_e": 0,
    "poste_Consultant": 0,
    "poste_Directeur_Technique": 0,
    "poste_Manager": 1,
    "poste_Représentant_Commercial": 0,
    "poste_Tech_Lead": 0,
}


# Vérifie que le health check retourne status ok
def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# Vérifie que /predict retourne une probabilité entre 0 et 1 et un booléen alerte
def test_predict_valid_input():
    response = client.post("/predict", json=VALID_EMPLOYEE)
    assert response.status_code == 200
    data = response.json()
    assert 0.0 <= data["probabilite_depart"] <= 1.0
    assert isinstance(data["alerte"], bool)


# Vérifie que /predict retourne une erreur 422 si les données sont invalides
def test_predict_invalid_input():
    response = client.post("/predict", json={"genre": "invalide"})
    assert response.status_code == 422
