import psycopg2
from src.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST
)

cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id SERIAL PRIMARY KEY,
        created_at TIMESTAMP DEFAULT NOW(),
        heure_supplementaires BOOLEAN,
        annee_experience_totale INTEGER,
        ratio_evolution FLOAT,
        ratio_relation_manager FLOAT,
        probabilite_depart FLOAT,
        alerte BOOLEAN
    )
""")

conn.commit()
cur.close()
conn.close()

print("Table predictions créée!")
