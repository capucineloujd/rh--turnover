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


# Vérifie que get_db_connection retourne une session SQLAlchemy valide
@pytest.mark.skipif(not has_db, reason="pas de base de données disponible en CI dev")
def test_get_db_connection_returns_session():
    session = get_db_connection()
    assert isinstance(session, Session)
    session.close()
