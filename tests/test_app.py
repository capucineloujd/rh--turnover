import os
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app, get_db_connection

has_db = os.getenv("DB_HOST") is not None

client = TestClient(app)


def make_mock_conn():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn

VALID_EMPLOYEE = {
    "id_employee": 1,
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


HIGH_RISK_EMPLOYEE = {
    "id_employee": 2,
    "genre": 0,
    "annee_experience_totale": 1,
    "satisfaction_employee_environnement": 1,
    "note_evaluation_precedente": 1,
    "niveau_hierarchique_poste": 1,
    "satisfaction_employee_nature_travail": 1,
    "satisfaction_employee_equipe": 1,
    "satisfaction_employee_equilibre_pro_perso": 1,
    "heure_supplementaires": True,
    "nombre_participation_pee": 0,
    "nb_formations_suivies": 0,
    "distance_domicile_travail": 30,
    "niveau_education": 1,
    "frequence_deplacement": 2,
    "annees_depuis_la_derniere_promotion": 0,
    "ratio_revenu_experience": 500.0,
    "ratio_evolution": 0.0,
    "ratio_relation_manager": 0.0,
    "departement_Consulting": 0,
    "statut_marital_Divorcé_e": 1,
    "poste_Consultant": 0,
    "poste_Directeur_Technique": 0,
    "poste_Manager": 0,
    "poste_Représentant_Commercial": 1,
    "poste_Tech_Lead": 0,
}

LOW_RISK_EMPLOYEE = {
    "id_employee": 3,
    "genre": 0,
    "annee_experience_totale": 15,
    "satisfaction_employee_environnement": 4,
    "note_evaluation_precedente": 4,
    "niveau_hierarchique_poste": 4,
    "satisfaction_employee_nature_travail": 4,
    "satisfaction_employee_equipe": 4,
    "satisfaction_employee_equilibre_pro_perso": 4,
    "heure_supplementaires": False,
    "nombre_participation_pee": 5,
    "nb_formations_suivies": 5,
    "distance_domicile_travail": 1,
    "niveau_education": 5,
    "frequence_deplacement": 0,
    "annees_depuis_la_derniere_promotion": 5,
    "ratio_revenu_experience": 3000.0,
    "ratio_evolution": 1.0,
    "ratio_relation_manager": 1.0,
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
    with patch("app.main.get_db_connection", return_value=make_mock_conn()):
        response = client.post("/predict", json=VALID_EMPLOYEE)
    assert response.status_code == 200
    data = response.json()
    assert 0.0 <= data["probabilite_depart"] <= 1.0
    assert isinstance(data["alerte"], bool)


# Vérifie que /predict retourne une erreur 422 si les données sont invalides
def test_predict_invalid_input():
    response = client.post("/predict", json={"genre": "invalide"})
    assert response.status_code == 422


# Vérifie qu'un profil à haut risque déclenche une alerte
def test_predict_high_risk_employee():
    with patch("app.main.get_db_connection", return_value=make_mock_conn()):
        response = client.post("/predict", json=HIGH_RISK_EMPLOYEE)
    assert response.status_code == 200
    assert response.json()["alerte"] is True

# Vérifie qu'un profil à bas risque ne déclenche pas d'alerte
def test_predict_low_risk_employee():
    with patch("app.main.get_db_connection", return_value=make_mock_conn()):
        response = client.post("/predict", json=LOW_RISK_EMPLOYEE)
    assert response.status_code == 200
    assert response.json()["alerte"] is False


# Vérifie que get_db_connection retourne une session SQLAlchemy valide
@pytest.mark.skipif(not has_db, reason="pas de base de données disponible en CI dev")
def test_get_db_connection_returns_session():
    session = get_db_connection()
    assert isinstance(session, Session)
    session.close()
