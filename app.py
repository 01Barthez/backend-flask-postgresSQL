from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/flask_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Vérifier que tous les champs requis sont présents
    required_fields = ['username', 'email', 'password']
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        return jsonify({
            'error': f'Missing required fields: {", ".join(missing_fields)}'
        }), 400
    
    # Vérifier si l'utilisateur existe déjà
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    # Créer l'utilisateur
    user = User(
        username=data.get('username'),
        email=data.get('email')
    )
    user.set_password(data.get('password'))
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        }
    }), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Vérifier que tous les champs requis sont présents
    required_fields = ['username', 'password']
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        return jsonify({
            'error': f'Missing required fields: {", ".join(missing_fields)}'
        }), 400
    
    # Vérifier les identifiants
    user = User.query.filter_by(username=data.get('username')).first()
    
    if user and user.check_password(data.get('password')):
        session['user_id'] = user.id
        return jsonify({
            'message': 'Logged in successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    
    # Vérifier que l'utilisateur est connecté
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Vérifier que l'utilisateur essaye de modifier son propre compte
    if session['user_id'] != user_id:
        return jsonify({'error': 'Cannot update another user'}), 403
    
    user = User.query.get_or_404(user_id)
    
    # Mettre à jour les champs si présents
    if 'username' in data:
        # Vérifier que le nouveau username n'est pas déjà utilisé
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'error': 'Username already exists'}), 400
        user.username = data['username']
    
    if 'email' in data:
        # Vérifier que le nouvel email n'est pas déjà utilisé
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'error': 'Email already exists'}), 400
        user.email = data['email']
    
    if 'password' in data:
        user.set_password(data['password'])
    
    db.session.commit()
    
    return jsonify({
        'message': 'User updated successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        }
    })

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Vérifier que l'utilisateur est connecté
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Vérifier que l'utilisateur essaye de supprimer son propre compte
    if session['user_id'] != user_id:
        return jsonify({'error': 'Cannot delete another user'}), 403
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    # Déconnexion automatique après suppression
    session.pop('user_id', None)
    
    return jsonify({
        'message': 'User deleted successfully'
    })

@app.route('/users/delete-all', methods=['DELETE'])
def delete_all_users():
    # Vérifier que l'utilisateur est connecté
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Supprimer tous les utilisateurs sauf celui qui fait la requête
    User.query.filter(User.id != session['user_id']).delete()
    db.session.commit()
    
    return jsonify({
        'message': 'All users except current user deleted successfully'
    })

@app.route('/users', methods=['GET'])
def get_users():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    users = User.query.all()
    return jsonify({
        'users': [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        } for user in users]
    })

def wait_for_db():
    import time
    max_retries = 10
    retry_delay = 2  # Secondes
    
    for attempt in range(max_retries):
        try:
            with app.app_context():
                db.create_all()
            print("Base de données initialisée avec succès")
            return True
        except Exception as e:
            print(f"Tentative {attempt + 1}/{max_retries} - Erreur: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Attente {retry_delay} secondes avant la prochaine tentative...")
                time.sleep(retry_delay)
    return False

if __name__ == '__main__':
    if wait_for_db():
        app.run(host='0.0.0.0', port=5000)
    else:
        print("Impossible de se connecter à la base de données après plusieurs tentatives")
