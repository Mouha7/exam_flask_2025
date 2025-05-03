from models.user import User
from app import db
from flask_login import login_user, logout_user

def register_user(username, email, password):
    user = User.query.filter_by(username=username).first()
    if user:
        return False, "Ce nom d'utilisateur est déjà pris."
    
    user = User.query.filter_by(email=email).first()
    if user:
        return False, "Cet email est déjà utilisé."
    
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return True, "Compte créé avec succès!"

def authenticate_user(username, password, remember=False):
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return False, "Nom d'utilisateur ou mot de passe incorrect."
    
    login_user(user, remember=remember)
    return True, "Connexion réussie!"

def logout():
    logout_user()
    return True, "Déconnexion réussie!"