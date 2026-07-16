import psycopg2
import pandas as pd

conn = psycopg2.connect(
    dbname="rh_turnover",
    user="rh_user",
    password="rh_password",
    host="localhost"
)

cur = conn.cursor()

# 10 dernières prédictions
cur.execute("SELECT * FROM predictions ORDER BY created_at DESC LIMIT 10")
rows = cur.fetchall()
colonnes = [desc[0] for desc in cur.description]
df = pd.DataFrame(rows, columns=colonnes)
print("=== 10 dernières prédictions ===")
print(df.to_string(index=False))

# Stats globales
cur.execute("""
    SELECT
        COUNT(*) AS total_predictions,
        SUM(CASE WHEN alerte THEN 1 ELSE 0 END) AS total_alertes,
        ROUND(AVG(probabilite_depart)::numeric, 3) AS proba_moyenne
    FROM predictions
""")
stats = cur.fetchone()
print("\n=== Statistiques globales ===")
print(f"Total prédictions : {stats[0]}")
print(f"Total alertes     : {stats[1]}")
print(f"Proba moyenne     : {stats[2]}")

cur.close()
conn.close()
