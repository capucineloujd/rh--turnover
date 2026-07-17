# RH Turnover

## Contexte et objectif
Ce projet est le quatrième dans le cadre de ma formation IA d'OpenClassroom. Dans le cadre d'une problématique de turnover, nous analysons les données RH de l'entreprise pour identifier objectivement les causes de démission. Trois sources de données sont disponibles : le SIRH (profil et informations contractuelles des employés), le système d'évaluation annuelle (notes de performance et satisfaction), et un sondage bien-être annuel (incluant un indicateur de départ).

## Résultat principal
Le principal facteur de démission identifié est les heures supplémentaires. Le modèle final (CatBoost) atteint un recall de 0.72 sur le jeu de test avec un seuil de décision de 0.535.

---

## Installation

Ce projet utilise [uv](https://github.com/astral-sh/uv) pour gérer les dépendances.

```bash
# Cloner le repo
git clone https://github.com/capucineloujd/rh--turnover.git
cd rh--turnover

# Installer les dépendances
uv sync --all-groups

# Copier le fichier d'environnement et le remplir
cp .env.example .env
```

## Configuration de la base de données

```bash
# Créer l'utilisateur et la base PostgreSQL
psql postgres -c "CREATE USER rh_user WITH PASSWORD 'rh_password';"
psql postgres -c "CREATE DATABASE rh_turnover OWNER rh_user;"

# Créer la table predictions
uv run python create_db.py
```

## Utilisation

### Lancer le notebook d'exploration
```bash
jupyter notebook notebook/notebook.ipynb
```

### Entraîner et sauvegarder le modèle
```bash
uv run python save_model.py
```

### Lancer l'API
```bash
uv run uvicorn app.main:app --reload
```

L'API est accessible sur `http://localhost:8000`.
La documentation Swagger est disponible sur `http://localhost:8000/docs`.

### Exemple d'appel à l'API
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"heure_supplementaires": true, "annee_experience_totale": 3, ...}'
```

### Interroger la base de données
```bash
uv run python query_db.py
```

## Tests

```bash
# Lancer les tests
uv run pytest tests/ -v

# Rapport de couverture
uv run pytest tests/ --cov=src --cov=app --cov-report=term-missing --cov-report=html
```

## Gestion des environnements

Le projet utilise des fichiers `.env` pour gérer les configurations :

| Fichier | Usage |
|---------|-------|
| `.env` | Environnement local (dev par défaut) |
| `.env.dev` | Développement |
| `.env.test` | Tests automatiques |
| `.env.prod` | Production |

Copier `.env.example` et renseigner les variables selon l'environnement cible.

## CI/CD

Le pipeline GitHub Actions (`.github/workflows/ci.yml`) se déclenche automatiquement à chaque push et pull request sur `main`. Il exécute :

1. Installation des dépendances
2. Création de la base de données de test
3. Entraînement et sauvegarde du modèle
4. Lint du code avec `ruff`
5. Exécution des 22 tests avec `pytest`

Les credentials de la base de données sont gérés via les **secrets GitHub** (Settings → Secrets and variables → Actions).

## Convention des branches

| Préfixe | Usage |
|---------|-------|
| `feature/nom` | Nouvelle fonctionnalité |
| `data/nom` | Travail sur les données |
| `fix/nom` | Correction de bug |

## Structure du projet

```
rh--turnover/
  app/              # API FastAPI
    main.py         # Serveur et endpoints
    schemas.py      # Schémas Pydantic
  src/              # Modules Python
    config.py       # Constantes et variables d'environnement
    data/           # Chargement et preprocessing
    features/       # Feature engineering et encoding
    models/         # Entraînement et évaluation
  tests/            # Tests unitaires et fonctionnels
  notebook/         # Exploration et expérimentation
  .github/
    workflows/
      ci.yml        # Pipeline CI/CD
```
