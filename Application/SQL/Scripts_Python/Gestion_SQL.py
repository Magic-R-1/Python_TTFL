import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# IDs de connexion
def IDsConnexionSQL():
    # IDs
    host = "localhost"
    database = "postgres"
    user = "postgres"
    password = "admin"
    port = 5432

    return host, database, user, password, port

# Pas utilisé
def OuvrirConnSQL():
    host, database, user, password, port = IDsConnexionSQL()

    # Connexion à la base de données PostgreSQL
    conn = psycopg2.connect(
        dbname=database,
        user=user,
        password=password,
        host=host,
        port=port
    )

    return conn

# Pas utilisé
def FermerConnSQL(conn):
    # Fermer la connexion
    conn.close()

# Création de l'engine pour connexion à la base
def CreerEngineSQL():
    host, database, user, password, port = IDsConnexionSQL()

    # Création d'un moteur SQLAlchemy pour utiliser pandas to_sql
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")

    return engine

# Suppression de l'engine
def SupprimerEngineSQL(engine):
    engine.dispose()