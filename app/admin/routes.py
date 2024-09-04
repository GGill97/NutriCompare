from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from app import db
from app.admin import bp
from app.models import Product, Category, User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
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
            # Add other fields as necessary
        )
        db.session.add(product)
        try:
            db.session.commit()
            flash('Product added successfully')
            return redirect(url_for('admin.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}')
    
    categories = Category.query.all()
    return render_template('admin/product_form.html', categories=categories)

@bp.route('/product/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.brand = request.form['brand']
        product.type = request.form['type']
        product.protein_per_serving = float(request.form['protein_per_serving'])
        product.price = float(request.form['price'])
        # Update other fields as necessary
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
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully')
    return redirect(url_for('admin.index'))