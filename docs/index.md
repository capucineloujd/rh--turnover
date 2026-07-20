# RH Turnover - Prédiction du risque de départ

## Contexte métier

Ce projet s'inscrit dans une problématique de turnover RH pour une entreprise fictive.
L'objectif est d'**identifier en amont les employés susceptibles de quitter l'entreprise**,
afin de permettre aux équipes RH de mettre en place des actions de rétention ciblées.

Trois sources de données ont été exploitées :

| Source | Contenu |
|--------|---------|
| SIRH | Profil et informations contractuelles des employés |
| Système d'évaluation annuelle | Notes de performance et de satisfaction |
| Sondage bien-être | Indicateurs de satisfaction et intention de départ |

## Résultat principal

Le principal facteur de démission identifié est **les heures supplémentaires**.

Le modèle final (CatBoost) atteint un **recall de 0.766** sur le jeu de test avec un seuil de décision de **0.535** :
sur 47 employés qui quittent réellement l'entreprise, **36 sont détectés à l'avance**.

## Architecture du projet

```
GitHub (code)  →  CI/CD (GitHub Actions)  →  Render (API FastAPI)  →  Supabase (PostgreSQL)
```

| Composant | Technologie |
|-----------|-------------|
| Modèle ML | CatBoost |
| API | FastAPI + Uvicorn |
| Base de données | PostgreSQL (Supabase en prod) |
| Déploiement | Render (Docker) |
| CI/CD | GitHub Actions |

## Navigation

- [Pipeline ML et choix techniques](model.md) - comment le modèle a été construit et pourquoi CatBoost
- [Maintenance et mise à jour](maintenance.md) - protocole pour réentraîner et monitorer le modèle
- [Guide d'utilisation de l'API](api.md) - comment appeler `/predict`, exemples et règles d'encodage
- [Documentation Swagger](https://rh-turnover-api.onrender.com/docs) - interface interactive de l'API
