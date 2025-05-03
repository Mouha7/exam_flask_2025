from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_migrate import Migrate
import os
from config import Config
from datetime import datetime

# Initialisation des extensions
db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialisation avec l'app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    socketio.init_app(app)
    migrate.init_app(app, db)
    
    # Ajout du context processor pour now()
    @app.context_processor
    def utility_processor():
        return {
            'now': datetime.utcnow
        }
    
    with app.app_context():
        # Import à l'intérieur du contexte d'application
        from routes.auth_routes import register_auth_routes
        from routes.recipe_routes import register_recipe_routes
        from routes.live_routes import register_live_routes
        
        register_auth_routes(app)
        register_recipe_routes(app)
        register_live_routes(app)
    
    return app

# Création d'une instance d'application pour l'exécution
app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)