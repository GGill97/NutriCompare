from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=True)
    flavor = db.Column(db.String(50), nullable=True)
    
    ingredients = db.Column(db.Text, nullable=True)
    protein_per_serving = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Integer, nullable=True)
    sugar = db.Column(db.Float, nullable=True)
    carbohydrates = db.Column(db.Float, nullable=True)
    fats = db.Column(db.Float, nullable=True)
    saturated_fats = db.Column(db.Float, nullable=True)
    cholesterol = db.Column(db.Float, nullable=True)
    sodium = db.Column(db.Float, nullable=True)
    dietary_fiber = db.Column(db.Float, nullable=True)
    
    price = db.Column(db.Float, nullable=False)
    serving_size = db.Column(db.String(10), nullable=True)
    servings_per_container = db.Column(db.Integer, nullable=True)
    flavors = db.Column(db.Text, nullable=True)
    allergens = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    source = db.Column(db.String(100), nullable=True)
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('products', lazy=True))
    image_url = db.Column(db.String(200), nullable=True)
    
            
    def __repr__(self):
        return f'<Product {self.name}>'
    
class Admin(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # Add other fields as needed
    def __repr__(self):
        return f'<Admin {self.username}>'

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)