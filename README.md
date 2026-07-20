# RH Turnover

[![CI Prod](https://github.com/capucineloujd/rh--turnover/actions/workflows/ci-prod.yml/badge.svg)](https://github.com/capucineloujd/rh--turnover/actions/workflows/ci-prod.yml)
![Python 3.11](https://img.shields.io/badge/python-3.11-pink?logo=python)
![Deployed on Render](https://img.shields.io/badge/deployed%20on-Render-46E3B7?logo=render)

**[Documentation complète](https://capucineloujd.github.io/rh--turnover/)** | **[API Swagger](https://rh-turnover-api.onrender.com/docs)**

## Contexte et objectif
Ce projet est le quatrième dans le cadre de ma formation IA d'OpenClassroom. Dans le cadre d'une problématique de turnover, nous analysons les données RH de l'entreprise pour identifier objectivement les causes de démission. Trois sources de données sont disponibles : le SIRH (profil et informations contractuelles des employés), le système d'évaluation annuelle (notes de performance et satisfaction), et un sondage bien-être annuel (incluant un indicateur de départ).

## Résultat principal
Le principal facteur de démission identifié est les heures supplémentaires. Le modèle final (CatBoost) atteint un recall de 0.766 sur le jeu de test avec un seuil de décision de 0.535.

## Standards d'expérimentation ML

**Dataset** : issu d'une base de données privée pour une entreprise fictive (fichiers CSV non versionnés).

**Choix du modèle** : CatBoost a été retenu pour son bon compromis précision/recall sur ce jeu de données déséquilibré, sans nécessiter de prétraitement des variables catégorielles.

**Métrique principale : recall**. Dans ce contexte métier, rater un employé qui va partir (faux négatif) est plus coûteux que signaler à tort un employé qui reste (faux positif). Le recall est donc prioritaire sur la précision.

**Seuil de décision à 0.535** : le seuil par défaut de 0.5 a été ajusté pour maximiser le recall sur le jeu de test tout en maintenant une précision acceptable.

**Split train/test** : 80/20 avec stratification sur la variable cible. Les hyperparamètres ont été ajustés manuellement en observant les métriques sur le jeu de validation.

**Reproductibilité** : un `random_state` fixe est utilisé dans tous les modules (`src/models/train.py`) pour garantir des résultats identiques à chaque exécution.

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

## Déploiement

```
GitHub (code)  →  CI/CD (GitHub Actions)  →  Render (API FastAPI)  →  Supabase (PostgreSQL)
```

L'API est déployée sur **Render** via Docker et accessible à :
**https://rh-turnover-api.onrender.com/docs**

### Composants

| Composant | Solution | Pourquoi |
|-----------|----------|----------|
| API | Render (Docker) | Hébergement gratuit, déploiement automatique depuis GitHub |
| Modèle | Commité dans le repo (`app/model.pkl`) | Fichier léger, disponible au démarrage sans réentraînement |
| Base de données | Supabase (PostgreSQL managé) | PostgreSQL managé gratuit, facile à connecter |

### Redéployer depuis zéro

1. Créer un projet **Supabase** → récupérer les credentials (host, port, user, password, db name)
2. Créer un service **Render** de type Web Service, connecté au repo GitHub, runtime Docker
3. Ajouter les variables d'environnement Supabase dans Render (Environment → Environment Variables) :
   `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
4. Pousser sur `main` → Render détecte le push et redéploie automatiquement

La configuration Render est versionnée dans [`render.yaml`](render.yaml).

## CI/CD

Trois pipelines GitHub Actions selon l'environnement :

| Workflow | Branche(s) | Étapes |
|----------|-----------|--------|
| `ci-dev.yml` | `feature/*`, `data/*`, `fix/*` | lint (ruff) + tests (pytest) |
| `ci-staging.yml` | `develop` | lint + tests + BDD PostgreSQL + sauvegarde modèle |
| `ci-prod.yml` | `main` | idem staging |

Chaque pipeline se déclenche automatiquement sur `push` et `pull_request` vers la branche cible.

Les credentials de la base de données sont gérés via les **secrets GitHub** (Settings --> Secrets and variables --> Actions).

## Schéma UML de la base de données

![Schéma BDD](docs/uml-rh.png)

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
      ci-dev.yml      # Pipeline dev (feature/*, data/*, fix/*)
      ci-staging.yml  # Pipeline staging (develop)
      ci-prod.yml     # Pipeline prod (main)
```
