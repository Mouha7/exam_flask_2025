from datetime import datetime
from app import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    cooking_time = db.Column(db.Integer)  # en minutes
    difficulty = db.Column(db.String(20))
    image_url = db.Column(db.String(200))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ratings = db.relationship('Rating', backref='recipe', lazy='dynamic')
    
    # Vous pouvez aussi définir une relation inverse pour cooking_now
    cooked_by = db.relationship('User', backref='cooking', 
                            foreign_keys='User.cooking_now',
                            uselist=False)
    
    def avg_rating(self):
        ratings = [r.value for r in self.ratings.all()]
        return sum(ratings) / len(ratings) if ratings else 0

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)  # 1-5
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    date_rated = db.Column(db.DateTime, default=datetime.utcnow)