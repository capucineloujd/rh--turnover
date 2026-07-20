# Maintenance et mise à jour du modèle

## Quand réentraîner le modèle ?

Le modèle doit être réentraîné lorsque l'une des conditions suivantes est observée :

| Signal | Seuil d'alerte | Comment le détecter |
|--------|---------------|---------------------|
| Baisse du recall en production | Recall < 0.70 | Comparer les alertes émises aux départs réels sur une période |
| Dérive des données d'entrée | Distribution des features significativement différente | Analyser `query_db.py` sur les prédictions récentes |
| Nouvelles données disponibles | > 6 mois de données fraîches | Calendrier fixe (voir ci-dessous) |
| Changement organisationnel | Restructuration, nouveau système de notation | Décision RH |

!!! tip "Calendrier recommandé"
    En l'absence de signal d'alerte, un réentraînement **annuel** est recommandé,
    à l'issue du cycle d'évaluation annuelle pour intégrer les nouvelles données RH.

## Comment réentraîner le modèle

### 1. Préparer les nouvelles données

Placer les fichiers CSV mis à jour dans `data_raw/` avec les mêmes noms et colonnes
que les fichiers originaux (SIRH, évaluations, sondage bien-être).

### 2. Réentraîner et sauvegarder

```bash
uv run python save_model.py
```

Ce script exécute le pipeline complet (chargement → preprocessing → features → encodage → entraînement)
et écrase `app/model.pkl` avec le nouveau modèle.

### 3. Vérifier les métriques

```bash
uv run pytest tests/test_model.py -v
```

Le test `test_model.py` vérifie que le recall reste ≥ 0.70 sur le jeu de test.
Si le test échoue, analyser les métriques détaillées avant de déployer.

### 4. Déployer

Committer `app/model.pkl` et pousser sur `main` :

```bash
git add app/model.pkl
git commit -m "model: réentraînement sur données YYYY"
git push origin main
```

Render redéploie automatiquement depuis `main`.

## Comment monitorer le modèle en production

### Interroger les prédictions en base

```bash
uv run python query_db.py
```

Retourne :

- Les 10 dernières prédictions
- Le nombre total de prédictions
- Le nombre d'alertes émises
- La probabilité de départ moyenne

### Indicateurs à surveiller

| Indicateur | Calcul | Interprétation |
|-----------|--------|---------------|
| Taux d'alerte | `nb_alertes / nb_prédictions` | Si > 30%, le modèle sur-alerte - seuil à recalibrer |
| Probabilité moyenne | Moyenne de `probabilite_depart` | Doit rester stable dans le temps |
| Taux de confirmation | Alertes confirmées / nb_alertes | À mesurer sur les départs réels constatés ensuite |

### Requête SQL directe (Supabase ou PostgreSQL local)

```sql
-- Taux d'alerte sur les 30 derniers jours
SELECT
    COUNT(*) AS total,
    SUM(CASE WHEN alerte THEN 1 ELSE 0 END) AS alertes,
    ROUND(AVG(probabilite_depart)::numeric, 3) AS proba_moyenne
FROM predictions
WHERE created_at >= NOW() - INTERVAL '30 days';
```

## Versioning du modèle

Chaque réentraînement doit être taggé dans Git :

```bash
git tag v1.1.0
git push origin v1.1.0
```

Convention de nommage : `vMAJEUR.MINEUR.PATCH`

| Type de changement | Version |
|-------------------|---------|
| Nouvelles données, mêmes features | `MINEUR` |
| Nouvelles features ou nouveau modèle | `MAJEUR` |
| Correction de bug pipeline | `PATCH` |
