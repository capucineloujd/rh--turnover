import joblib
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "model.pkl"

model = joblib.load(MODEL_PATH)
