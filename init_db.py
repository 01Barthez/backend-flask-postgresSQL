import os
import psycopg2

DB_NAME = 'flask_app'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = 'db'
DB_PORT = '5432'

try:
    # Connexion à la base de données par défaut (postgres)
    conn = psycopg2.connect(
        dbname='postgres',
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Vérifier si la base de données existe déjà
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    exists = cursor.fetchone()
    
    if not exists:
        # Créer la base de données
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"Base de données {DB_NAME} créée avec succès")
    else:
        print(f"Base de données {DB_NAME} existe déjà")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Erreur lors de l'initialisation de la base de données: {e}")
