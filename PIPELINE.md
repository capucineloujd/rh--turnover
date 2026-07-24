# Documentation du pipeline CI/CD

## 1. Structure du code (`src/`)
Tout le code était dans un notebook. Un notebook n'est pas testable automatiquement : on ne peut pas importer une cellule dans un test. En extrayant la logique dans des modules Python (`src/`), chaque fonction devient indépendante, importable et testable.

**Donc :**
- `src/data/loader.py` : charge et joint les 3 CSV en un seul Dataframe
- `src/data/preprocessing.py` : nettoie les données (typos, booléens, colonnes inutiles)
- `src/features/build_features.py` : crée les ratios, supprime les variables redondantes, sépare X et y
- `src/features/encoding.py` : encode les variables catégorielles (one-hot encoding, ordinal, binaire)
- `src/models/train.py` : entraîne CatBoost avec les hyperparamètres finaux
- `src/models/evaluate.py` : calcule les métriques (recall, precision, F1, AP)
- `src/config.py` : centralise les constantes et variables d'environnement


## 2. Tests automatiques (`tests/`)

**Ce qu'on a fait (26 tests) :**

| Fichier | Ce qu'il teste |
|---------|---------------|
| `test_loader.py` | Chargement des CSV, jointure, colonnes attendues, fichier manquant |
| `test_preprocessing.py` | Renommage des colonnes, suppressions, types booléens |
| `test_build_features.py` | Ratios créés, colonnes supprimées, pas de NaN, y séparé de X |
| `test_encoding.py` | Encodage binaire, ordinal, one-hot, colonnes brutes supprimées |
| `test_model.py` | Entraînement sans erreur, probabilités entre 0 et 1, recall >= 0.70 |
| `test_app.py` | Health check, prédiction valide, erreur 422 sur données invalides ou manquantes (géré automatiquement par Pydantic), cas limites haut/bas risque, connexion BDD |

**Rapport de couverture :**
```bash
uv run pytest tests/ --cov=src --cov=app --cov-report=html
```

## 3. API FastAPI (`app/`)

- `app/schemas.py` : définit les données attendues en entrée (`EmployeeInput`) et en sortie (`PredictionOutput`)
- `app/model.py` : charge le modèle CatBoost sauvegardé (`model.pkl`)
- `app/main.py` : expose deux endpoints :
  - `GET /` --> health check
  - `POST /predict` --> reçoit les données d'un employé, retourne la probabilité de départ et une alerte


## 4. Base de données PostgreSQL

- `src/database.py` : modèles SQLAlchemy (`Data`, `Prediction`), engine et `SessionLocal`
- `create_db.py` : crée les tables et insère les 1470 lignes du dataset dans `data`
- `app/main.py` : à chaque appel `/predict`, insère une ligne dans `predictions` via SQLAlchemy
- `query_db.py` : interroge la base pour récupérer les dernières prédictions et les stats globales


**La foreign key**
`predictions.id_employee` référence `data.id_employee` : chaque prédiction est liée à un employé identifiable. Ca garantit la cohérence et permet de retrouver le profil complet derrière chaque alerte.

## 5. Gestion des environnements
**Ce qu'on a fait :**
- `.env.dev` --> configuration locale de développement
- `.env.test` --> configuration pour les tests automatiques
- `.env.prod` --> configuration de production
- `.env.example` --> template versionné sur Git (sans les vraies valeurs)
- `src/config.py` lit ces variables avec `python-dotenv`

## 6. Pipeline CI/CD 
Le pipeline se déclenche sur chaque `push` et `pull_request` vers `main` et exécute dans l'ordre :

1. Lance un conteneur PostgreSQL
2. Installe Python 3.11 et uv
3. Installe les dépendances (`uv sync`)
4. Crée la table (`create_db.py`)
5. Entraîne et sauvegarde le modèle (`save_model.py`)
6. Vérifie le style du code (`ruff check`)
7. Lance les 26 tests (`pytest`)

**Gestion des secrets**
Les credentials PostgreSQL ne sont pas en dur dans le YAML ; ils sont stockés dans les **secrets GitHub** et injectés via `${{ secrets.DB_USER }}`.

---

## 7. Workflows CI séparés par environnement

**3 fichiers de workflow**

| Fichier | Se déclenche sur | Étapes |
|---------|-----------------|--------|
| `ci-dev.yml` | `feature/*`, `data/*`, `fix/*` | ruff + pytest uniquement (pas de BDD, pas de modèle) |
| `ci-staging.yml` | `develop` | ruff + pytest + save_model + BDD de test |
| `ci-prod.yml` | `main` | idem staging - pipeline officiel avant production |



## 7b. Protection des branches `main` et `develop`
Un pour `main`, un pour `develop`.

- `Require a pull request before merging` 
- `Require status checks to pass` (job `test`) 
- `Block force pushes`
- `Restrict deletions` 

## 8. Versioning / convention des branches et environnements

| Branche | Environnement | Rôle |
|---------|---------------|------|
| `feature/nom` | **dev** | Développement local d'une fonctionnalité |
| `data/nom` | **dev** | Travail sur les données |
| `fix/nom` | **dev** | Correction de bug |
| `develop` | **staging** | Intégration - toutes les features fusionnent ici avant prod |
| `main` | **prod** | Production - code stable et déployé |


## 9. Déploiement (sur Render)
Le modèle est directement committé dans le repo (app/model.pkl). le fichier est léger donc c'est plus simple que de le stocker ailleurs, et il est dispo dès le démarrage de l'API sans avoir à réentraîner.

