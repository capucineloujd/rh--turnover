from src.database import engine, Base, Data, SessionLocal
from src.data.loader import load_data

Base.metadata.create_all(engine)

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

session = SessionLocal()

for _, row in df.iterrows():
    exists = session.get(Data, int(row["id_employee"]))
    if not exists:
        session.add(Data(**row.to_dict()))

session.commit()
session.close()

print(f"Tables créées et {len(df)} lignes insérées dans data!")
