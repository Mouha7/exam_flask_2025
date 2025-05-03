from flask import url_for, current_app
from flask_login import current_user
from datetime import datetime
from werkzeug.utils import secure_filename  # Ajoutez cette importation
import os
from app import db, socketio
from models.recipe import Recipe, Rating
from models.user import User

def get_all_recipes(page=1, per_page=10):
    return Recipe.query.order_by(Recipe.date_posted.desc()).paginate(page=page, per_page=per_page)

def get_recipe_by_id(recipe_id):
    return Recipe.query.get_or_404(recipe_id)

def create_recipe(title, description, ingredients, instructions, cooking_time, difficulty, image=None):
    recipe = Recipe(
        title=title,
        description=description,
        ingredients=ingredients,
        instructions=instructions,
        cooking_time=cooking_time,
        difficulty=difficulty,
        user_id=current_user.id
    )
    
    if image and image.filename:
        filename = secure_filename(image.filename)
        # Créer le dossier s'il n'existe pas
        os.makedirs('static/uploads', exist_ok=True)
        # Chemin complet pour sauvegarder le fichier
        file_path = os.path.join('static/uploads', filename)
        # Sauvegarder le fichier
        image.save(file_path)
        # Stocker seulement le chemin relatif dans la base de données
        recipe.image_url = 'uploads/' + filename  # Corriger cette ligne
    
    db.session.add(recipe)
    db.session.commit()
    return recipe

def rate_recipe(recipe_id, rating_value):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Vérifier si l'utilisateur a déjà noté cette recette
    existing_rating = Rating.query.filter_by(
        user_id=current_user.id,
        recipe_id=recipe_id
    ).first()
    
    if existing_rating:
        existing_rating.value = rating_value
    else:
        new_rating = Rating(
            value=rating_value,
            user_id=current_user.id,
            recipe_id=recipe_id
        )
        db.session.add(new_rating)
    
    db.session.commit()
    return recipe.avg_rating()

def start_cooking(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    current_user.cooking_now = recipe_id
    db.session.commit()
    
    # Notifier les autres utilisateurs via WebSocket
    socketio.emit('cooking_started', {
        'user': current_user.username,
        'recipe_id': recipe_id,
        'recipe_title': recipe.title
    })
    
    print(f"Émission de l'événement cooking_started: {current_user.username} cuisine {recipe.title}")
    
    return True

def stop_cooking():
    if current_user.is_authenticated and current_user.cooking_now is not None:
        recipe_id = current_user.cooking_now
        recipe = Recipe.query.get(recipe_id)
        
        # Récupérer le nom de la recette avant de réinitialiser
        recipe_title = recipe.title if recipe else "une recette"
        
        # Réinitialiser
        current_user.cooking_now = None
        db.session.commit()
        
        # Notifier les autres utilisateurs via WebSocket
        socketio.emit('cooking_stopped', {
            'user': current_user.username,
            'recipe_id': recipe_id,
            'recipe_title': recipe_title
        })
        
        print(f"Émission de l'événement cooking_stopped: {current_user.username} a arrêté de cuisiner {recipe_title}")
        
    return True

def get_live_cooking():
    cooks = User.query.filter(User.cooking_now.isnot(None)).all()
    cooking_data = []
    
    for cook in cooks:
        recipe = Recipe.query.get(cook.cooking_now)
        if recipe:
            cooking_data.append({
                'user': cook.username,
                'recipe_id': recipe.id,
                'recipe_title': recipe.title
            })
    
    return cooking_data

def update_recipe(recipe_id, title, description, ingredients, instructions, cooking_time, difficulty, image=None):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Vérifier que l'utilisateur actuel est bien l'auteur de la recette
    if recipe.user_id != current_user.id:
        return None, "Vous n'êtes pas autorisé à modifier cette recette."
    
    # Mise à jour des champs
    recipe.title = title
    recipe.description = description
    recipe.ingredients = ingredients
    recipe.instructions = instructions
    recipe.cooking_time = cooking_time
    recipe.difficulty = difficulty
    
    # Traitement de l'image si nécessaire
    if image and image.filename:
        filename = secure_filename(image.filename)
        # Créer le dossier s'il n'existe pas
        os.makedirs('static/uploads', exist_ok=True)
        # Chemin complet pour sauvegarder le fichier
        file_path = os.path.join('static/uploads', filename)
        # Sauvegarder le fichier
        image.save(file_path)
        # Stocker seulement le chemin relatif dans la base de données
        recipe.image_url = 'uploads/' + filename
    
    db.session.commit()
    return recipe, "La recette a été mise à jour avec succès!"

def search_recipes(search_term, page=1, per_page=10):
    """Recherche des recettes par titre, description ou ingrédients"""
    if not search_term:
        return get_all_recipes(page, per_page)
    
    search = f"%{search_term}%"
    return Recipe.query.filter(
        db.or_(
            Recipe.title.ilike(search),
            Recipe.description.ilike(search),
            Recipe.ingredients.ilike(search)
        )
    ).order_by(Recipe.date_posted.desc()).paginate(page=page, per_page=per_page)

