from flask import render_template, jsonify
from flask_login import login_required
from services.recipe_service import get_live_cooking
from app import socketio

def register_live_routes(app):
    @app.route('/live-cooking')
    def live_cooking():
        cooking_data = get_live_cooking()
        return render_template('recipes/live.html', cooking_data=cooking_data, title='Cuisine en direct')
    
    @app.route('/api/live-cooking')
    def api_live_cooking():
        cooking_data = get_live_cooking()
        return jsonify(cooking_data)
    
    # Socket.IO pour les mises à jour en temps réel
    @socketio.on('connect')
    def handle_connect():
        print('Client connecté')
    
    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client déconnecté')