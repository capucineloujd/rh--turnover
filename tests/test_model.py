from sklearn.model_selection import train_test_split
from src.data.loader import load_data
from src.data.preprocessing import preprocess
from src.features.build_features import build_features
from src.features.encoding import encode
from src.models.train import train, select_features
from src.models.evaluate import evaluate
from src.config import SEUIL_FINAL, RANDOM_STATE, TEST_SIZE


def pipeline():
    # Reproduit exactement le pipeline complet jusqu'au train/test split
    X, y = build_features(preprocess(load_data()))
    X = encode(X)
    X = select_features(X)
    return train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y)


# Vérifie que le modèle s'entraîne sans erreur
def test_train_runs():
    X_train, X_test, y_train, y_test = pipeline()
    model = train(X_train, y_train)
    assert model is not None


# Vérifie que predict_proba retourne des probabilités entre 0 et 1
def test_predict_proba_range():
    X_train, X_test, y_train, y_test = pipeline()
    model = train(X_train, y_train)
    probas = model.predict_proba(X_test)[:, 1]
    assert probas.min() >= 0.0
    assert probas.max() <= 1.0


# Vérifie que le nombre de prédictions correspond au nombre de lignes de X_test
def test_predictions_shape():
    X_train, X_test, y_train, y_test = pipeline()
    model = train(X_train, y_train)
    probas = model.predict_proba(X_test)[:, 1]
    assert len(probas) == len(X_test)


# Vérifie que le recall minimum acceptable est atteint sur le jeu de test
def test_recall_minimum():
    X_train, X_test, y_train, y_test = pipeline()
    model = train(X_train, y_train)
    metrics = evaluate(model, X_test, y_test, SEUIL_FINAL)
    assert metrics["recall"] >= 0.70, f"Recall trop bas : {metrics['recall']:.2f}"
