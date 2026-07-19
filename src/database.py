from sqlalchemy import create_engine, Column, Integer, Float, Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Data(Base):
    __tablename__ = "data"

    id_employee = Column(Integer, primary_key=True)
    age = Column(Integer)
    genre = Column(String)
    revenu_mensuel = Column(Integer)
    statut_marital = Column(String)
    departement = Column(String)
    poste = Column(String)
    nombre_experiences_precedentes = Column(Integer)
    nombre_heures_travaillees = Column(Integer)
    annee_experience_totale = Column(Integer)
    annees_dans_entreprise = Column(Integer)
    annees_dans_poste_actuel = Column(Integer)
    satisfaction_environnement = Column(Integer)
    note_evaluation_precedente = Column(Integer)
    niveau_hierarchique_poste = Column(Integer)
    satisfaction_nature_travail = Column(Integer)
    satisfaction_equipe = Column(Integer)
    satisfaction_equilibre_pro_perso = Column(Integer)
    note_evaluation_actuelle = Column(Integer)
    heure_supplementaires = Column(Boolean)
    augmentation_salaire_precedente = Column(String)
    a_quitte_entreprise = Column(Boolean)
    nombre_participation_pee = Column(Integer)
    nb_formations_suivies = Column(Integer)
    nombre_employes_sous_responsabilite = Column(Integer)
    distance_domicile_travail = Column(Integer)
    niveau_education = Column(Integer)
    domaine_etude = Column(String)
    ayant_enfants = Column(Boolean)
    frequence_deplacement = Column(String)
    annees_depuis_derniere_promotion = Column(Integer)
    annees_sous_responsable_actuel = Column(Integer)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, server_default=func.now())
    id_employee = Column(Integer, ForeignKey("data.id_employee"))
    heure_supplementaires = Column(Boolean)
    annee_experience_totale = Column(Integer)
    ratio_evolution = Column(Float)
    ratio_relation_manager = Column(Float)
    probabilite_depart = Column(Float)
    alerte = Column(Boolean)
