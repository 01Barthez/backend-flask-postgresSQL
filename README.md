# Flask User Management API

Une API simple pour la gestion des utilisateurs avec Flask, PostgreSQL et SQLAlchemy.

## Installation

1. Assurez-vous d'avoir Docker et Docker Compose installés

2. Clonez le repository

3. Lancez les conteneurs avec :
```bash
docker-compose up --build
```

L'application sera accessible sur http://localhost:5000

## Endpoints

### 1. Inscription (Register)
- **URL**: `/register`
- **Méthode**: POST
- **Corps de la requête**:
```json
{
    "username": "votre_nom_utilisateur",
    "email": "votre_email@example.com",
    "password": "votre_mot_de_passe"
}
```
- **Réponse en cas de succès**:
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "votre_nom_utilisateur",
        "email": "votre_email@example.com",
        "created_at": "2025-06-17T21:10:11+00:00"
    }
}
```

### 2. Connexion (Login)
- **URL**: `/login`
- **Méthode**: POST
- **Corps de la requête**:
```json
{
    "username": "votre_nom_utilisateur",
    "password": "votre_mot_de_passe"
}
```
- **Réponse en cas de succès**:
```json
{
    "message": "Logged in successfully",
    "user": {
        "id": 1,
        "username": "votre_nom_utilisateur",
        "email": "votre_email@example.com"
    }
}
```

### 3. Déconnexion (Logout)
- **URL**: `/logout`
- **Méthode**: POST
- **Réponse**:
```json
{
    "message": "Logged out successfully"
}
```

### 4. Liste des utilisateurs
- **URL**: `/users`
- **Méthode**: GET
- **Nécessite d'être connecté**
- **Réponse**:
```json
{
    "users": [
        {
            "id": 1,
            "username": "votre_nom_utilisateur",
            "email": "votre_email@example.com",
            "created_at": "2025-06-17T21:10:11+00:00"
        }
    ]
}
```

### 5. Modifier un utilisateur
- **URL**: `/user/<id>`
- **Méthode**: PUT
- **Nécessite d'être connecté**
- **Nécessite d'être l'utilisateur en question**
- **Corps de la requête**:
```json
{
    "username": "nouveau_nom_utilisateur",
    "email": "nouvel_email@example.com",
    "password": "nouveau_mot_de_passe"
}
```
- **Note**: Vous pouvez mettre à jour un ou plusieurs champs en même temps
- **Réponse en cas de succès**:
```json
{
    "message": "User updated successfully",
    "user": {
        "id": 1,
        "username": "nouveau_nom_utilisateur",
        "email": "nouvel_email@example.com",
        "created_at": "2025-06-17T21:10:11+00:00"
    }
}
```

### 6. Supprimer un utilisateur
- **URL**: `/user/<id>`
- **Méthode**: DELETE
- **Nécessite d'être connecté**
- **Nécessite d'être l'utilisateur en question**
- **Réponse**:
```json
{
    "message": "User deleted successfully"
}
```
- **Note**: Vous serez automatiquement déconnecté après la suppression

### 7. Supprimer tous les utilisateurs
- **URL**: `/users/delete-all`
- **Méthode**: DELETE
- **Nécessite d'être connecté**
- **Réponse**:
```json
{
    "message": "All users except current user deleted successfully"
}
```
- **Note**: Supprime tous les utilisateurs sauf celui qui fait la requête

### 1. Inscription (Register)
- **URL**: `/register`
- **Méthode**: POST
- **Corps de la requête**:
```json
{
    "username": "votre_nom_utilisateur",
    "email": "votre_email@example.com",
    "password": "votre_mot_de_passe"
}
```
- **Réponse en cas de succès**:
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "votre_nom_utilisateur",
        "email": "votre_email@example.com",
        "created_at": "2025-06-17T21:10:11+00:00"
    }
}
```

### 2. Connexion (Login)
- **URL**: `/login`
- **Méthode**: POST
- **Corps de la requête**:
```json
{
    "username": "votre_nom_utilisateur",
    "password": "votre_mot_de_passe"
}
```
- **Réponse en cas de succès**:
```json
{
    "message": "Logged in successfully",
    "user": {
        "id": 1,
        "username": "votre_nom_utilisateur",
        "email": "votre_email@example.com"
    }
}
```

### 3. Déconnexion (Logout)
- **URL**: `/logout`
- **Méthode**: POST
- **Réponse**:
```json
{
    "message": "Logged out successfully"
}
```

### 4. Liste des utilisateurs
- **URL**: `/users`
- **Méthode**: GET
- **Nécessite d'être connecté**
- **Réponse**:
```json
{
    "users": [
        {
            "id": 1,
            "username": "votre_nom_utilisateur",
            "email": "votre_email@example.com",
            "created_at": "2025-06-17T21:10:11+00:00"
        }
    ]
}
```

## Exemples d'utilisation avec curl

### Inscription
```bash
curl -X POST http://localhost:5000/register \
-H "Content-Type: application/json" \
-d '{"username": "Barthez", "email": "kenwoubarthez@gmail.com", "password": "password123"}'
```

### Connexion
```bash
curl -X POST http://localhost:5000/login \
-H "Content-Type: application/json" \
-d '{"username": "Barthez", "password": "password123"}'
```

### Liste des utilisateurs
```bash
curl http://localhost:5000/users
```

## Notes
- Assurez-vous d'inclure tous les champs requis dans vos requêtes POST
- La connexion est requise pour accéder à l'endpoint `/users`
- Les mots de passe sont stockés de manière sécurisée avec un hash
