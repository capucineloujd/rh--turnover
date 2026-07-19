import pandas as pd
import psycopg2
from fastapi import FastAPI
from app.schemas import EmployeeInput, PredictionOutput
from app.model import model
from src.config import SEUIL_FINAL, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

app = FastAPI(title="RH Turnover API", description="Prédit la probabilité qu'un employé quitte l'entreprise.")

COLUMN_RENAME = {
    "statut_marital_Divorcé_e": "statut_marital_Divorcé(e)",
    "poste_Directeur_Technique": "poste_Directeur Technique",
    "poste_Représentant_Commercial": "poste_Représentant Commercial",
    "poste_Tech_Lead": "poste_Tech Lead",
}


def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionOutput)
def predict(employee: EmployeeInput) -> PredictionOutput:
    data = pd.DataFrame([employee.model_dump()]).rename(columns=COLUMN_RENAME)
    proba = model.predict_proba(data)[0, 1]
    alerte = bool(proba >= SEUIL_FINAL)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO predictions (
            id_employee, heure_supplementaires, annee_experience_totale,
            ratio_evolution, ratio_relation_manager,
            probabilite_depart, alerte
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        employee.id_employee,
        employee.heure_supplementaires,
        employee.annee_experience_totale,
        employee.ratio_evolution,
        employee.ratio_relation_manager,
        round(float(proba), 3),
        alerte,
    ))
    conn.commit()
    cur.close()
    conn.close()

    return PredictionOutput(
        probabilite_depart=round(float(proba), 3),
        alerte=alerte,
    )
