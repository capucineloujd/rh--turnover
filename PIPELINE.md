# Documentation du pipeline CI/CD

Ce document explique les choix techniques faits dans ce projet et comment les justifier.

---

## 1. Structure du code (`src/`)

**Pourquoi ?**
Tout le code était dans un notebook. Un notebook n'est pas testable automatiquement — on ne peut pas importer une cellule dans un test. En extrayant la logique dans des modules Python (`src/`), chaque fonction devient indépendante, importable et testable.

**Ce qu'on a fait :**
- `src/data/loader.py` — charge et joint les 3 CSV en un seul DataFrame
- `src/data/preprocessing.py` — nettoie les données (typos, booléens, colonnes inutiles)
- `src/features/build_features.py` — crée les ratios, supprime les variables redondantes, sépare X et y
- `src/features/encoding.py` — encode les variables catégorielles (one-hot, ordinal, binaire)
- `src/models/train.py` — entraîne CatBoost avec les hyperparamètres finaux
- `src/models/evaluate.py` — calcule les métriques (recall, precision, F1, AP)
- `src/config.py` — centralise les constantes et variables d'environnement

**Règle clé :** un module ne contient que des fonctions. Pas de code qui s'exécute à l'import, pas de `print` de vérification.

---

## 2. Tests automatiques (`tests/`)

**Pourquoi ?**
Sans tests, on ne sait pas si une modification casse quelque chose. Les tests permettent de détecter les régressions automatiquement.

**Ce qu'on a fait (22 tests) :**

| Fichier | Ce qu'il teste |
|---------|---------------|
| `test_loader.py` | Chargement des CSV, jointure, colonnes attendues, fichier manquant |
| `test_preprocessing.py` | Renommage des colonnes, suppressions, types booléens |
| `test_build_features.py` | Ratios créés, colonnes supprimées, pas de NaN, y séparé de X |
| `test_encoding.py` | Encodage binaire, ordinal, one-hot, colonnes brutes supprimées |
| `test_model.py` | Entraînement sans erreur, probabilités entre 0 et 1, recall >= 0.70 |
| `test_app.py` | Health check, prédiction valide, erreur 422 sur données invalides |

**Pourquoi pytest ?** C'est le standard Python pour les tests — simple, extensible, compatible avec la CI.

**Rapport de couverture :**
```bash
uv run pytest tests/ --cov=src --cov=app --cov-report=html
```
Génère un rapport HTML dans `htmlcov/` montrant quelles lignes de code sont couvertes.

---

## 3. API FastAPI (`app/`)

**Pourquoi FastAPI ?**
- Génère automatiquement une documentation Swagger (`/docs`)
- Validation automatique des données avec Pydantic
- Très rapide à développer et à tester

**Ce qu'on a fait :**
- `app/schemas.py` — définit les données attendues en entrée (`EmployeeInput`) et en sortie (`PredictionOutput`)
- `app/model.py` — charge le modèle CatBoost sauvegardé (`model.pkl`)
- `app/main.py` — expose deux endpoints :
  - `GET /` → health check
  - `POST /predict` → reçoit les données d'un employé, retourne la probabilité de départ et une alerte

**Pourquoi sauvegarder le modèle ?**
On ne peut pas réentraîner CatBoost à chaque démarrage de l'API — trop lent. On entraîne une fois avec `save_model.py` et on charge `model.pkl` au démarrage.

---

## 4. Base de données PostgreSQL

**Pourquoi ?**
Stocker l'historique des prédictions permet de suivre les alertes dans le temps et d'auditer les décisions du modèle.

**Ce qu'on a fait :**
- `create_db.py` — crée la table `predictions` avec les colonnes inputs + outputs
- `app/main.py` — à chaque appel `/predict`, insère une ligne en base
- `query_db.py` — interroge la base pour récupérer les dernières prédictions et les stats globales

**Structure de la table :**
```sql
predictions (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    heure_supplementaires BOOLEAN,
    annee_experience_totale INTEGER,
    ratio_evolution FLOAT,
    ratio_relation_manager FLOAT,
    probabilite_depart FLOAT,
    alerte BOOLEAN
)
```

---

## 5. Gestion des environnements

**Pourquoi ?**
On ne veut pas écrire dans la BDD de production quand on fait des tests, ni exposer les mots de passe dans le code.

**Ce qu'on a fait :**
- `.env.dev` → configuration locale de développement
- `.env.test` → configuration pour les tests automatiques
- `.env.prod` → configuration de production
- `.env.example` → template versionné sur Git (sans les vraies valeurs)
- `src/config.py` lit ces variables avec `python-dotenv`

**Règle clé :** les fichiers `.env` sont dans `.gitignore` — jamais pushés sur Git. Les vraies valeurs sont soit dans les fichiers `.env` locaux, soit dans les secrets GitHub pour la CI.

---

## 6. Pipeline CI/CD (`.github/workflows/ci.yml`)

**Pourquoi ?**
Sans CI, les tests ne tournent que quand on y pense. Avec la CI, ils tournent automatiquement à chaque push et chaque PR — impossible d'oublier.

**Ce qu'on a fait :**
Le pipeline se déclenche sur chaque `push` et `pull_request` vers `main` et exécute dans l'ordre :

1. Lance un conteneur PostgreSQL
2. Installe Python 3.11 et uv
3. Installe les dépendances (`uv sync`)
4. Crée la table (`create_db.py`)
5. Entraîne et sauvegarde le modèle (`save_model.py`)
6. Vérifie le style du code (`ruff check`)
7. Lance les 22 tests (`pytest`)

**Gestion des secrets :**
Les credentials PostgreSQL ne sont pas en dur dans le YAML — ils sont stockés dans les **secrets GitHub** (Settings → Secrets and variables → Actions) et injectés via `${{ secrets.DB_USER }}`.

---

## 7. Protection de la branche `main`

**Pourquoi ?**
Empêcher de merger du code cassé ou non relu directement sur `main`.

**Ce qu'on a configuré (GitHub Settings → Rules → Rulesets) :**
- `Require a pull request before merging` — tout changement passe par une PR
- `Require status checks to pass` (job `test`) — la CI doit être verte avant de merger
- `Require branches to be up to date` — la PR doit être testée avec le dernier code de main
- `Block force pushes` — interdit de réécrire l'historique Git
- `Restrict deletions` — interdit de supprimer la branche main

---

## 8. Versioning

**Convention des branches et environnements :**

| Branche | Environnement | Rôle |
|---------|---------------|------|
| `feature/nom` | **dev** | Développement local d'une fonctionnalité |
| `data/nom` | **dev** | Travail sur les données |
| `fix/nom` | **dev** | Correction de bug |
| `develop` | **staging** | Intégration — toutes les features fusionnent ici avant prod |
| `main` | **prod** | Production — code stable et déployé |

**Flux de travail :**
```
feature/ma-feature  →  develop  →  main
       (dev)           (staging)   (prod)
```

1. Créer une branche depuis `develop` : `git checkout -b feature/xxx`
2. PR vers `develop` — la CI tourne, validation en staging
3. Quand `develop` est stable : PR `develop → main` pour déployer en prod

**La CI se déclenche sur `develop` et `main`** — jamais directement sur une branche `feature/`.

**Tags de version :**
```bash
git tag v1.0.0
git push origin v1.0.0
```
Les tags marquent les versions stables du projet — `v1.0.0` est la première version complète.
