import psycopg2
from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from src.data.loader import load_data

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS data (
        id_employee INTEGER PRIMARY KEY,
        age INTEGER,
        genre VARCHAR,
        revenu_mensuel INTEGER,
        statut_marital VARCHAR,
        departement VARCHAR,
        poste VARCHAR,
        nombre_experiences_precedentes INTEGER,
        nombre_heures_travaillees INTEGER,
        annee_experience_totale INTEGER,
        annees_dans_entreprise INTEGER,
        annees_dans_poste_actuel INTEGER,
        satisfaction_environnement INTEGER,
        note_evaluation_precedente INTEGER,
        niveau_hierarchique_poste INTEGER,
        satisfaction_nature_travail INTEGER,
        satisfaction_equipe INTEGER,
        satisfaction_equilibre_pro_perso INTEGER,
        note_evaluation_actuelle INTEGER,
        heure_supplementaires BOOLEAN,
        augmentation_salaire_precedente VARCHAR,
        a_quitte_entreprise BOOLEAN,
        nombre_participation_pee INTEGER,
        nb_formations_suivies INTEGER,
        nombre_employes_sous_responsabilite INTEGER,
        distance_domicile_travail INTEGER,
        niveau_education INTEGER,
        domaine_etude VARCHAR,
        ayant_enfants BOOLEAN,
        frequence_deplacement VARCHAR,
        annees_depuis_derniere_promotion INTEGER,
        annees_sous_responsable_actuel INTEGER
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id SERIAL PRIMARY KEY,
        created_at TIMESTAMP DEFAULT NOW(),
        id_employee INTEGER REFERENCES data(id_employee),
        heure_supplementaires BOOLEAN,
        annee_experience_totale INTEGER,
        ratio_evolution FLOAT,
        ratio_relation_manager FLOAT,
        probabilite_depart FLOAT,
        alerte BOOLEAN
    )
""")

df = load_data()

df = df.drop(columns=["eval_number", "code_sondage"])

df["heure_supplementaires"] = df["heure_supplementaires"].map({"Oui": True, "Non": False})
df["a_quitte_l_entreprise"] = df["a_quitte_l_entreprise"].map({"Oui": True, "Non": False})
df["ayant_enfants"] = df["ayant_enfants"].map({"Y": True, "N": False})

df = df.rename(columns={
    "nombre_heures_travailless": "nombre_heures_travaillees",
    "annees_dans_l_entreprise": "annees_dans_entreprise",
    "annees_dans_le_poste_actuel": "annees_dans_poste_actuel",
    "satisfaction_employee_environnement": "satisfaction_environnement",
    "satisfaction_employee_nature_travail": "satisfaction_nature_travail",
    "satisfaction_employee_equipe": "satisfaction_equipe",
    "satisfaction_employee_equilibre_pro_perso": "satisfaction_equilibre_pro_perso",
    "augementation_salaire_precedente": "augmentation_salaire_precedente",
    "a_quitte_l_entreprise": "a_quitte_entreprise",
    "nombre_employee_sous_responsabilite": "nombre_employes_sous_responsabilite",
    "annees_depuis_la_derniere_promotion": "annees_depuis_derniere_promotion",
    "annes_sous_responsable_actuel": "annees_sous_responsable_actuel",
})

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO data VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (id_employee) DO NOTHING
    """, tuple(row))

conn.commit()
cur.close()
conn.close()

print(f"Tables créées et {len(df)} lignes insérées dans data!")
