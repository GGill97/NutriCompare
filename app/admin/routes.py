from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, login_user, logout_user
from app import db
from app.admin import bp
from app.models import Product, Category, Admin
from werkzeug.utils import secure_filename 
import os
import logging 
from sqlalchemy import or_
# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_product_image(file):
    logging.info(f"Attempting to save image: {file.filename}")
    if file and file.filename != '' and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_dir = os.path.join(current_app.root_path, 'static', 'images')
        logging.info(f"Upload directory: {upload_dir}")
        
        # Ensure the upload directory exists
        os.makedirs(upload_dir, exist_ok=True)
        logging.info(f"Ensured directory exists: {upload_dir}")
        
        # Generate a unique filename
        base, extension = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(upload_dir, filename)):
            filename = f"{base}_{counter}{extension}"
            counter += 1
        
        file_path = os.path.join(upload_dir, filename)
        logging.info(f"Attempting to save file to: {file_path}")
        
        try:
            file.save(file_path)
            logging.info(f"File saved successfully: {file_path}")
            return f'/static/images/{filename}'
        except Exception as e:
            logging.error(f"Error saving file: {str(e)}", exc_info=True)
            return None
    else:
        logging.warning(f"Invalid file or filename: {file.filename}")
        return None
    
    
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('admin.index'))
        flash('Invalid username or password')
    return render_template('admin/login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@bp.route('/')
@login_required
def index():
    search_query = request.args.get('search', '')
    if search_query:
        products = Product.query.filter(
            or_(
                Product.name.ilike(f'%{search_query}%'),
                Product.brand.ilike(f'%{search_query}%'),
                Product.type.ilike(f'%{search_query}%')
            )
        ).all()
    else:
        products = Product.query.all()
    return render_template('admin/index.html', products=products, search_query=search_query)


@bp.route('/product/create', methods=['GET', 'POST'])
@login_required
def create_new_product():
    if request.method == 'POST':
        logging.info("Received POST request to create new product")
        logging.debug(f"Form data: {request.form}")
        logging.debug(f"Files: {request.files}")
        
        category = Category.query.filter_by(name=request.form['type']).first()
        if not category:
            category = Category(name=request.form['type'])
            db.session.add(category)
        
        product = Product(
            name=request.form['name'],
            brand=request.form['brand'],
            type=request.form['type'],
            flavor=request.form.get('flavor'),
            ingredients=request.form.get('ingredients'),
            protein_per_serving=float(request.form['protein_per_serving']),
            calories=int(request.form['calories']) if request.form.get('calories') else None,
            sugar=float(request.form['sugar']) if request.form.get('sugar') else None,
            carbohydrates=float(request.form['carbohydrates']) if request.form.get('carbohydrates') else None,
            fats=float(request.form['fats']) if request.form.get('fats') else None,
            saturated_fats=float(request.form['saturated_fats']) if request.form.get('saturated_fats') else None,
            cholesterol=float(request.form['cholesterol']) if request.form.get('cholesterol') else None,
            sodium=float(request.form['sodium']) if request.form.get('sodium') else None,
            dietary_fiber=float(request.form['dietary_fiber']) if request.form.get('dietary_fiber') else None,
            price=float(request.form['price']),
            serving_size=request.form.get('serving_size'),
            servings_per_container=int(request.form['servings_per_container']) if request.form.get('servings_per_container') else None,
            flavors=request.form.get('flavors'),
            allergens=request.form.get('allergens'),
            description=request.form.get('description'),
            source=request.form.get('source'),
            category=category
        )
        
        if 'image' in request.files:
            file = request.files['image']
            logging.debug(f"Received file: {file.filename}")
            if file.filename == '':
                logging.warning("No file selected")
                flash('No file selected for uploading')
            elif not allowed_file(file.filename):
                logging.warning(f"File type not allowed: {file.filename}")
                flash('File type not allowed')
            else:
                try:
                    image_url = save_product_image(file)
                    if image_url:
                        product.image_url = image_url
                        logging.debug(f"Image URL set to: {image_url}")
                    else:
                        logging.warning("Failed to save image")
                        flash('Failed to save image. Please try again.')
                except Exception as e:
                    logging.error(f"Error saving image: {str(e)}")
                    flash(f'Error saving image: {str(e)}')
        else:
            logging.debug("No image file in request")
        
        db.session.add(product)
        try:
            db.session.commit()
            flash('Product added successfully')
            return redirect(url_for('admin.index'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding product to database: {str(e)}")
            flash(f'An error occurred: {str(e)}')
    
    categories = Category.query.all()
    return render_template('admin/product_form.html', categories=categories)

@bp.route('/product/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    logging.info(f"Editing product with id: {id}")
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        logging.info("Received POST request to edit product")
        logging.debug(f"Form data: {request.form}")
        logging.debug(f"Files: {request.files}")
        
        category = Category.query.filter_by(name=request.form['type']).first()
        if not category:
            category = Category(name=request.form['type'])
            db.session.add(category)
        
        product.name = request.form['name']
        product.brand = request.form['brand']
        product.type = request.form['type']
        product.flavor = request.form.get('flavor')
        product.ingredients = request.form.get('ingredients')
        product.protein_per_serving = float(request.form['protein_per_serving'])
        product.calories = int(request.form['calories']) if request.form.get('calories') else None
        product.sugar = float(request.form['sugar']) if request.form.get('sugar') else None
        product.carbohydrates = float(request.form['carbohydrates']) if request.form.get('carbohydrates') else None
        product.fats = float(request.form['fats']) if request.form.get('fats') else None
        product.saturated_fats = float(request.form['saturated_fats']) if request.form.get('saturated_fats') else None
        product.cholesterol = float(request.form['cholesterol']) if request.form.get('cholesterol') else None
        product.sodium = float(request.form['sodium']) if request.form.get('sodium') else None
        product.dietary_fiber = float(request.form['dietary_fiber']) if request.form.get('dietary_fiber') else None
        product.price = float(request.form['price'])
        product.serving_size = request.form.get('serving_size')
        product.servings_per_container = int(request.form['servings_per_container']) if request.form.get('servings_per_container') else None
        product.flavors = request.form.get('flavors')
        product.allergens = request.form.get('allergens')
        product.description = request.form.get('description')
        product.source = request.form.get('source')
        product.category = category
        
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '' and allowed_file(file.filename):
                # Delete old image if exists
                if product.image_url:
                    old_file_path = os.path.join(current_app.root_path, product.image_url.lstrip('/'))
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)

                # Save new image
                image_url = save_product_image(file)
                if image_url:
                    product.image_url = image_url

        try:
            db.session.commit()
            flash('Product updated successfully')
            return redirect(url_for('admin.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}')
    
    categories = Category.query.all()
    return render_template('admin/product_form.html', product=product, categories=categories)



@bp.route('/product/<int:id>/delete', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    if product.image_url:
        file_path = os.path.join(current_app.root_path, product.image_url.lstrip('/'))
        if os.path.exists(file_path):
            os.remove(file_path)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully')
    return redirect(url_for('admin.index'))

@bp.errorhandler(413)
def too_large(e):
    flash("File is too large", "error")
    return redirect(request.url)