from flask import render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import login_required, current_user
from services.recipe_service import (
    get_all_recipes, get_recipe_by_id, create_recipe, 
    rate_recipe, start_cooking, stop_cooking, update_recipe, search_recipes
)
from werkzeug.utils import secure_filename
import os

def register_recipe_routes(app):
    @app.route('/')
    def home():
        page = request.args.get('page', 1, type=int)
        recipes = get_all_recipes(page=page, per_page=6)
        return render_template('home.html', recipes=recipes)
    
    @app.route('/recipes')
    def recipes_list():
        page = request.args.get('page', 1, type=int)
        search_term = request.args.get('q', '')
        
        if search_term:
            recipes = search_recipes(search_term, page=page, per_page=10)
        else:
            recipes = get_all_recipes(page=page, per_page=10)
        
        return render_template(
            'recipes/list.html', 
            recipes=recipes, 
            title='Toutes les recettes',
            search_term=search_term
        )
    
    @app.route('/recipe/<int:recipe_id>')
    def recipe_detail(recipe_id):
        recipe = get_recipe_by_id(recipe_id)
        return render_template('recipes/detail.html', recipe=recipe, title=recipe.title)
    
    @app.route('/recipe/new', methods=['GET', 'POST'])
    @login_required
    def recipe_create():
        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            ingredients = request.form.get('ingredients')
            instructions = request.form.get('instructions')
            cooking_time = int(request.form.get('cooking_time'))
            difficulty = request.form.get('difficulty')
            image = request.files.get('image')
            
            recipe = create_recipe(
                title, description, ingredients, instructions, 
                cooking_time, difficulty, image
            )
            
            flash('Votre recette a été créée avec succès!', 'success')
            return redirect(url_for('recipe_detail', recipe_id=recipe.id))
        
        return render_template('recipes/create.html', title='Nouvelle Recette')
    
    @app.route('/recipe/<int:recipe_id>/rate', methods=['POST'])
    @login_required
    def recipe_rate(recipe_id):
        rating = int(request.form.get('rating'))
        if 1 <= rating <= 5:
            avg_rating = rate_recipe(recipe_id, rating)
            return jsonify({'success': True, 'avg_rating': avg_rating})
        return jsonify({'success': False, 'error': 'Note invalide'}), 400
    
    @app.route('/recipe/<int:recipe_id>/cook', methods=['POST'])
    @login_required
    def recipe_cook(recipe_id):
        start_cooking(recipe_id)
        flash('Vous avez commencé à cuisiner cette recette!', 'success')
        return redirect(url_for('live_cooking'))
    
    @app.route('/recipe/stop-cooking', methods=['POST'])
    @login_required
    def recipe_stop_cooking():
        # Sauvegarde de l'ID avant de le réinitialiser
        recipe_id = current_user.cooking_now
        
        # Arrêt de la cuisine
        stop_cooking()
        
        flash('Vous avez arrêté de cuisiner.', 'info')
        
        # Redirection intelligente
        if recipe_id:
            return redirect(url_for('recipe_detail', recipe_id=recipe_id))
        else:
            return redirect(url_for('recipes_list'))
        
    @app.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
    @login_required
    def recipe_edit(recipe_id):
        recipe = get_recipe_by_id(recipe_id)
        
        # Vérifier que l'utilisateur actuel est bien l'auteur de la recette
        if recipe.user_id != current_user.id:
            flash("Vous n'êtes pas autorisé à modifier cette recette.", 'danger')
            return redirect(url_for('recipe_detail', recipe_id=recipe_id))
        
        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            ingredients = request.form.get('ingredients')
            instructions = request.form.get('instructions')
            cooking_time = int(request.form.get('cooking_time'))
            difficulty = request.form.get('difficulty')
            image = request.files.get('image')
            
            updated_recipe, message = update_recipe(
                recipe_id, title, description, ingredients, instructions, 
                cooking_time, difficulty, image
            )
            
            if updated_recipe:
                flash(message, 'success')
                return redirect(url_for('recipe_detail', recipe_id=recipe_id))
            else:
                flash(message, 'danger')
        
        return render_template('recipes/edit.html', recipe=recipe, title=f'Modifier: {recipe.title}')