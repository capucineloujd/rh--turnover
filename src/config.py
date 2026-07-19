import os
from dotenv import load_dotenv

load_dotenv()

# Constantes ML (fixes, pas d'environnement)
RANDOM_STATE = 42
SEUIL_FINAL = 0.535
TEST_SIZE = 0.2

# Variables de base de données (lues depuis .env)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "rh_turnover")
DB_USER = os.getenv("DB_USER", "rh_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "rh_password")
ENV = os.getenv("ENV", "dev")
