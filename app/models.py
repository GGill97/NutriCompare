from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

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
    price = db.Column(db.Float, nullable=False)
    serving_size = db.Column(db.String(10), nullable=True)
    servings_per_container = db.Column(db.Integer, nullable=True)
    flavors = db.Column(db.Text, nullable=True)
    allergens = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    source = db.Column(db.String(100), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('products', lazy=True))


    def __repr__(self):
        return f'<Product {self.name}>'
    
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))