# Maintenance et mise à jour du modèle


## Comment réentraîner le modèle

### 1. Préparer les nouvelles données

Placer les fichiers CSV mis à jour dans `data_raw/` avec les mêmes noms et colonnes
que les fichiers originaux (SIRH, évaluations, sondage bien-être).

### 2. Réentraîner et sauvegarder

```bash
uv run python save_model.py
```

Ce script exécute le pipeline complet (chargement --> preprocessing --> features --> encodage --> entraînement)
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

##  monitorer le modèle en production

### Interroger les prédictions en base

```bash
uv run python query_db.py
```

Retourne :

- Les 10 dernières prédictions
- Le nombre total de prédictions
- Le nombre d'alertes émises
- La probabilité de départ moyenne


## Versioning du modèle

Chaque réentraînement doit être taggé dans Git :

```bash
git tag v1.1.0
git push origin v1.1.0
```
