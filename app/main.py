import pandas as pd
from fastapi import FastAPI
from app.schemas import EmployeeInput, PredictionOutput
from app.model import model
from src.config import SEUIL_FINAL
from src.database import SessionLocal, Prediction

app = FastAPI(title="RH Turnover API", description="Prédit la probabilité qu'un employé quitte l'entreprise.")

COLUMN_RENAME = {
    "statut_marital_Divorcé_e": "statut_marital_Divorcé(e)",
    "poste_Directeur_Technique": "poste_Directeur Technique",
    "poste_Représentant_Commercial": "poste_Représentant Commercial",
    "poste_Tech_Lead": "poste_Tech Lead",
}


def get_db_connection():
    return SessionLocal()


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionOutput)
def predict(employee: EmployeeInput) -> PredictionOutput:
    data = pd.DataFrame([employee.model_dump()]).rename(columns=COLUMN_RENAME)
    proba = model.predict_proba(data)[0, 1]
    alerte = bool(proba >= SEUIL_FINAL)

    session = get_db_connection()
    session.add(Prediction(
        id_employee=employee.id_employee,
        heure_supplementaires=employee.heure_supplementaires,
        annee_experience_totale=employee.annee_experience_totale,
        ratio_evolution=employee.ratio_evolution,
        ratio_relation_manager=employee.ratio_relation_manager,
        probabilite_depart=round(float(proba), 3),
        alerte=alerte,
    ))
    session.commit()
    session.close()

    return PredictionOutput(
        probabilite_depart=round(float(proba), 3),
        alerte=alerte,
    )
