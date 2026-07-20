# Guide d'utilisation de l'API

L'API est déployée sur Render et accessible à l'adresse :
**`https://rh-turnover-api.onrender.com`**

La documentation Swagger interactive est disponible sur :
**`https://rh-turnover-api.onrender.com/docs`**

## Authentification

Tous les appels à `/predict` nécessitent une clé API passée dans le header `X-API-Key` :

```
X-API-Key: votre-clé-api
```

Sans clé ou avec une clé invalide, l'API retourne une erreur `403 Forbidden`.

## Endpoints

| Méthode | Route | Description |
|---------|-------|-------------|
| `GET` | `/` | Vérification de l'état de l'API |
| `POST` | `/predict` | Prédire le risque de départ d'un employé |

## Préparer les données avant d'appeler `/predict`

L'API attend des **features préprocessées**. Deux transformations sont nécessaires avant l'appel.

### 1. Calculer les ratios engineerés

| Champ API | Formule | Cas limite |
|-----------|---------|------------|
| `ratio_revenu_experience` | `revenu_mensuel / annee_experience_totale` | Si expérience = 0 : utiliser la médiane du dataset |
| `ratio_evolution` | `annees_dans_le_poste_actuel / annees_dans_l_entreprise` | Si ancienneté = 0 : mettre `0` |
| `ratio_relation_manager` | `annees_sous_responsable_actuel / annees_dans_l_entreprise` | Si ancienneté = 0 : mettre `0` |

### 2. Encoder les variables catégorielles

**Encodage binaire :**

| Variable brute | Valeur | Code à envoyer |
|---------------|--------|----------------|
| `genre` | Homme | `0` |
| `genre` | Femme | `1` |

**Encodage ordinal :**

| Variable brute | Valeur | Code à envoyer |
|---------------|--------|----------------|
| `frequence_deplacement` | Aucun | `0` |
| `frequence_deplacement` | Occasionnel | `1` |
| `frequence_deplacement` | Fréquent | `2` |

**Encodage one-hot (variables binaires 0/1) :**

| Champ API | Vaut `1` si... | Catégorie de référence (tous à `0`) |
|-----------|---------------|-------------------------------------|
| `departement_Consulting` | Département = Consulting | Commercial *(Ressources Humaines traité comme Commercial)* |
| `statut_marital_Divorcé_e` | Statut = Divorcé(e) | Célibataire *(Marié(e) traité comme Célibataire)* |
| `poste_Consultant` | Poste = Consultant | Assistant de Direction |
| `poste_Directeur_Technique` | Poste = Directeur Technique | Assistant de Direction |
| `poste_Manager` | Poste = Manager | Assistant de Direction |
| `poste_Représentant_Commercial` | Poste = Représentant Commercial | Assistant de Direction |
| `poste_Tech_Lead` | Poste = Tech Lead | Assistant de Direction |

!!! note "Postes absents de l'encodage"
    Cadre Commercial, Ressources Humaines et Senior Manager ont été retirés lors de la
    sélection de features (importance < 1%). Ils sont encodés comme la référence
    (tous les `poste_*` à `0`), identique à Assistant de Direction.

## Exemple d'appel

### curl

```bash
curl -X POST "https://rh-turnover-api.onrender.com/predict" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: votre-clé-api" \
  -d '{
    "id_employee": 42,
    "genre": 0,
    "annee_experience_totale": 8,
    "satisfaction_employee_environnement": 2,
    "note_evaluation_precedente": 3,
    "niveau_hierarchique_poste": 2,
    "satisfaction_employee_nature_travail": 2,
    "satisfaction_employee_equipe": 3,
    "satisfaction_employee_equilibre_pro_perso": 1,
    "heure_supplementaires": true,
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
  }'
```

### Réponse attendue

```json
{
  "probabilite_depart": 0.712,
  "alerte": true
}
```

### Python

```python
import requests

payload = {
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
    "poste_Tech_Lead": 0,
}

response = requests.post(
    "https://rh-turnover-api.onrender.com/predict",
    json=payload,
    headers={"X-API-Key": "votre-clé-api"},
)
print(response.json())
# {"probabilite_depart": 0.712, "alerte": true}
```

## Codes de réponse

| Code | Signification |
|------|--------------|
| `200` | Prédiction calculée avec succès |
| `403` | Clé API manquante ou invalide |
| `422` | Données invalides ou champ manquant - vérifier les types et plages de valeurs |
