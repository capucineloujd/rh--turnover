import pandas as pd
from sqlalchemy import text
from src.database import engine

with engine.connect() as conn:
    df = pd.read_sql(
        text("SELECT * FROM predictions ORDER BY created_at DESC LIMIT 10"),
        conn
    )
    print("=== 10 dernières prédictions ===")
    print(df.to_string(index=False))

    stats = conn.execute(text("""
        SELECT
            COUNT(*) AS total_predictions,
            SUM(CASE WHEN alerte THEN 1 ELSE 0 END) AS total_alertes,
            ROUND(AVG(probabilite_depart)::numeric, 3) AS proba_moyenne
        FROM predictions
    """)).fetchone()

    print("\n=== Statistiques globales ===")
    print(f"Total prédictions : {stats[0]}")
    print(f"Total alertes     : {stats[1]}")
    print(f"Proba moyenne     : {stats[2]}")
