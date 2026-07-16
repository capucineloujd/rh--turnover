import psycopg2

conn = psycopg2.connect(
    dbname="rh_turnover",
    user="rh_user",
    password="rh_password",
    host="localhost"
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
