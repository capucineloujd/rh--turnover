import pandas as pd
from fastapi import FastAPI
from app.schemas import EmployeeInput, PredictionOutput
from app.model import model
from src.config import SEUIL_FINAL
from src.database import SessionLocal, Prediction
import os


from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    expected = os.getenv("API_KEY")
    if not expected or api_key != expected:
        raise HTTPException(status_code=403, detail="Clé API invalide ou manquante")
    

app = FastAPI(
    title="RH Turnover API",
    version="1.0.0",
    description="""
## Contexte
Cette API s'inscrit dans un projet d'analyse du turnover RH.
Elle prédit la probabilité qu'un employé quitte volontairement l'entreprise,
à partir de données issues du SIRH, des évaluations annuelles et du sondage bien-être.

## Modèle
- Algorithme : **CatBoost**
- Métrique principale : **recall = 0.766** (priorité sur les faux négatifs)
- Seuil de décision : **0.535** (ajusté pour maximiser le recall)

## Interprétation des résultats
- `probabilite_depart` : score entre 0 et 1
- `alerte = true` : employé identifié comme à risque de départ

## Prérequis
L'API attend des **features préprocessées** : ratios calculés manuellement,
variables catégorielles encodées selon les règles documentées dans chaque champ.
""",
    contact={
        "name": "Capucine Jaud",
        "url": "https://github.com/capucineloujd/rh--turnover",
    },
)

COLUMN_RENAME = {
    "statut_marital_Divorcé_e": "statut_marital_Divorcé(e)",
    "poste_Directeur_Technique": "poste_Directeur Technique",
    "poste_Représentant_Commercial": "poste_Représentant Commercial",
    "poste_Tech_Lead": "poste_Tech Lead",
}


def get_db_connection():
    return SessionLocal()


@app.get(
    "/",
    summary="Vérification de l'état de l'API",
    tags=["Santé"],
)
def health_check():
    return {"status": "ok"}


@app.post(
    "/predict",
    dependencies=[Depends(verify_api_key)],
    response_model=PredictionOutput,
    summary="Prédire le risque de départ d'un employé",
    description="""
Reçoit le profil préprocessé d'un employé et retourne :
- la **probabilité de départ** (score entre 0 et 1)
- une **alerte booléenne** (`true` si probabilité ≥ 0.535)

Chaque appel est persisté en base de données (table `predictions`)
pour permettre le suivi des alertes dans le temps.
""",
    tags=["Prédictions"],
    responses={
        200: {"description": "Prédiction calculée avec succès"},
        422: {"description": "Données invalides ou champ manquant"},
    },
)
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
