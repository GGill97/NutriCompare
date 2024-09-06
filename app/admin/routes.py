from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user, login_user, logout_user
# from werkzeug.security import check_password_hash
from app import db
from app.admin import bp
from app.models import Product, Category, Admin
from werkzeug.utils import secure_filename 
import os
import logging 

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_product_image(file):
    if file and file.filename != '' and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_dir = os.path.join(current_app.root_path, 'static', 'images')
        
        if not os.path.exists(upload_dir):
            try:
                os.makedirs(upload_dir)
            except OSError as e:
                logging.error(f"Error creating directory: {str(e)}")
                return None
        
        file_path = os.path.join(upload_dir, filename)
        logging.debug(f"Saving file to: {file_path}")
        
        try:
            file.save(file_path)
            logging.debug("File saved successfully")
            return f'/static/images/{filename}'
        except Exception as e:
            logging.error(f"Error saving file: {str(e)}")
            return None
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
    return redirect(url_for('main.index'))

@bp.route('/')
@login_required
def index():
    products = Product.query.all()
    return render_template('admin/index.html', products=products)

@bp.route('/product/create', methods=['GET', 'POST'])
@login_required
def create_new_product():
    if request.method == 'POST':
        category = Category.query.filter_by(name=request.form['type']).first()
        if not category:
            category = Category(name=request.form['type'])
            db.session.add(category)
        
        product = Product(
            name=request.form['name'],
            brand=request.form['brand'],
            type=request.form['type'],
            protein_per_serving=float(request.form['protein_per_serving']),
            price=float(request.form['price']),
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
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        category = Category.query.filter_by(name=request.form['type']).first()
        if not category:
            category = Category(name=request.form['type'])
            db.session.add(category)
        
        product.name = request.form['name']
        product.brand = request.form['brand']
        product.type = request.form['type']
        product.protein_per_serving = float(request.form['protein_per_serving'])
        product.price = float(request.form['price'])
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