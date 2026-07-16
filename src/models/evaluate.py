from sklearn.metrics import recall_score, precision_score, f1_score, average_precision_score


def evaluate(model, X_test, y_test, seuil: float) -> dict:
    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred  = (y_proba >= seuil).astype(int)
    return {
        "recall":    recall_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "f1":        f1_score(y_test, y_pred),
        "AP":        average_precision_score(y_test, y_proba),
    }
