# Docker Configuration

Ce fichier contient la documentation détaillée pour la configuration Docker de l'application Flask.

## Structure des fichiers

```
flask/
├── Dockerfile          # Configuration du conteneur Flask
├── docker-compose.yml  # Configuration Docker Compose
├── init_db.py         # Script d'initialisation de la base de données
├── data/              # Dossier de persistance des données
├── .dockerignore     # Fichiers à exclure de la construction Docker
└── .gitignore        # Fichiers à exclure du versioning Git
```

## Configuration de la persistance des données

La base de données PostgreSQL est configurée pour être persistante. Les données sont stockées dans le dossier `data/` qui est monté comme volume dans le conteneur PostgreSQL.

Cela signifie que :
1. Les données de la base de données sont conservées même après l'arrêt des conteneurs
2. Les données sont restaurées automatiquement lors du redémarrage
3. Le dossier `data/` doit être préservé pour conserver les données

## Comment démarrer l'application

1. Assurez-vous d'avoir Docker et Docker Compose installés

2. Dans le dossier racine du projet, exécutez :
```bash
# Construire et démarrer les conteneurs
docker-compose -f docker-compose.yml up --build
```

L'application sera accessible sur http://localhost:5000

## Comment arrêter l'application

Pour arrêter proprement l'application :
```bash
# Arrêter les conteneurs
docker-compose -f docker-compose.yml down
```

## Sauvegarde des données

- Les données sont stockées dans le dossier `data/`
- Pour supprimer complètement les données (attention, cela supprime TOUTES les données) :
```bash
# Arrêter les conteneurs et supprimer les volumes
docker-compose -f docker-compose.yml down -v
# Supprimer le dossier data
rm -rf data/
```

## Redémarrage avec données persistantes

Pour redémarrer l'application avec les données précédentes :
```bash
# Arrêter les conteneurs existants
docker-compose -f docker-compose.yml down

# Redémarrer avec les données précédentes
docker-compose -f docker-compose.yml up --build
```

Les données de la base de données seront automatiquement restaurées depuis le dossier `data/`
