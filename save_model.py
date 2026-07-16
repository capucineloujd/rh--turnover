import joblib
from sklearn.model_selection import train_test_split
from src.data.loader import load_data
from src.data.preprocessing import preprocess
from src.features.build_features import build_features
from src.features.encoding import encode
from src.models.train import train, select_features
from src.config import RANDOM_STATE, TEST_SIZE

# pipeline
X, y = build_features(preprocess(load_data()))
X = encode(X)
X = select_features(X)
X_train, _, y_train, _ = train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y)
model = train(X_train, y_train)


joblib.dump(model, "app/model.pkl")
