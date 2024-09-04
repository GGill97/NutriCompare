from flask import render_template, request, current_app, url_for, redirect, jsonify
from app.main import bp
from app.models import Product, db, User
from sqlalchemy import or_, func, and_
from flask_login import current_user, login_required

@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PRODUCTS_PER_PAGE']

    # Get filter parameters
    brand = request.args.get('brand')
    category = request.args.getlist('category')
    price_ranges = request.args.getlist('price_range')
    protein_ranges = request.args.getlist('protein_range')
    search_query = request.args.get('search')

    # Get sort parameter
    sort = request.args.get('sort', 'name')
    order = request.args.get('order', 'asc')

    # Base query
    query = Product.query

    # Apply filters
    if brand:
        query = query.filter(Product.brand == brand)
    if category:
        query = query.filter(Product.type.in_(category))
    if price_ranges:
        price_conditions = []
        for range in price_ranges:
            if range == '45+':
                price_conditions.append(Product.price >= 45)
            else:
                min_price, max_price = map(float, range.split('-'))
                price_conditions.append(and_(Product.price >= min_price, Product.price < max_price))
        query = query.filter(or_(*price_conditions))
    if protein_ranges:
        protein_conditions = []
        for range in protein_ranges:
            if range == '25+':
                protein_conditions.append(Product.protein_per_serving >= 25)
            else:
                min_protein, max_protein = map(float, range.split('-'))
                protein_conditions.append(and_(Product.protein_per_serving >= min_protein, Product.protein_per_serving < max_protein))
        query = query.filter(or_(*protein_conditions))
    if search_query:
        search = f"%{search_query}%"
        query = query.filter(or_(
            Product.name.ilike(search),
            Product.brand.ilike(search),
            Product.type.ilike(search)
        ))

    # Apply sorting
    if sort == 'price':
        query = query.order_by(Product.price.asc() if order == 'asc' else Product.price.desc())
    elif sort == 'protein':
        query = query.order_by(Product.protein_per_serving.asc() if order == 'asc' else Product.protein_per_serving.desc())
    else:
        query = query.order_by(Product.name.asc() if order == 'asc' else Product.name.desc())

    # Get unique brands and categories for filter options
    brands = db.session.query(Product.brand).distinct().order_by(Product.brand)
    categories = db.session.query(Product.type).distinct().order_by(Product.type)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('index.html', 
                           pagination=pagination,
                           brands=brands,
                           categories=categories,
                           current_filters={
                               'brand': brand,
                               'category': category,
                               'price_range': price_ranges,
                               'protein_range': protein_ranges,
                               'sort': sort,
                               'order': order,
                               'search': search_query
                           })

@bp.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    similar_products = Product.query.filter(
        Product.type == product.type,
        Product.id != product.id
    ).order_by(func.random()).limit(3).all()
    return render_template('product_detail.html', title=product.name, product=product, similar_products=similar_products)

@bp.route('/compare')
def compare():
    product_ids = request.args.getlist('products')
    if len(product_ids) < 2 or len(product_ids) > 4:
        return redirect(url_for('main.index'))

    products_to_compare = Product.query.filter(Product.id.in_(product_ids)).all()
    return render_template('compare.html', products=products_to_compare)

# @bp.route('/favorite/<int:product_id>', methods=['POST'])
# @login_required
# def favorite_product(product_id):
#     product = Product.query.get_or_404(product_id)
#     if product in current_user.favorites:
#         current_user.favorites.remove(product)
#         db.session.commit()
#         return jsonify({'status': 'removed'})
#     else:
#         current_user.favorites.append(product)
#         db.session.commit()
#         return jsonify({'status': 'added'})

# @bp.route('/favorites')
# @login_required
# def favorites():
#     return render_template('favorites.html', favorites=current_user.favorites)

@bp.route('/search')
def search():
    query = request.args.get('query', '')
    if query:
        search = f"%{query}%"
        products = Product.query.filter(or_(
            Product.name.ilike(search),
            Product.brand.ilike(search),
            Product.type.ilike(search)
        )).limit(10).all()
        return jsonify([{'id': p.id, 'name': p.name, 'brand': p.brand} for p in products])
    return jsonify([])

@bp.route('/protein-calculator')
def protein_calculator():
    return render_template('protein_calculator.html')

@bp.route('/api/price-history/<int:product_id>')
def price_history(product_id):
    # This is a placeholder. You would need to implement actual price tracking.
    return jsonify([
        {'date': '2023-01-01', 'price': 29.99},
        {'date': '2023-02-01', 'price': 27.99},
        {'date': '2023-03-01', 'price': 31.99},
        {'date': '2023-04-01', 'price': 28.99},
    ])