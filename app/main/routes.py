from flask import render_template, request, current_app, url_for, redirect, jsonify, flash, abort
from app.main import bp
from app.models import Product, db
from sqlalchemy import or_, func, and_

@bp.route('/protein-101')
def protein_101():
    protein_types = [
        {
            "name": "Whey Protein",
            "description": "A fast-absorbing protein derived from milk, ideal for post-workout recovery.",
            "short_description": "Fast-absorbing, milk-derived protein."
        },
        {
            "name": "Casein Protein",
            "description": "A slow-absorbing protein also derived from milk, often used before bed for sustained release.",
            "short_description": "Slow-absorbing, milk-derived protein."
        },
        {
            "name": "Plant-based Protein",
            "description": "Protein derived from plant sources like pea, rice, or soy. Suitable for vegans and those with dairy allergies.",
            "short_description": "Vegan-friendly protein from plant sources."
        },
        # Add more protein types as needed
    ]
    return render_template('protein_101.html', protein_types=protein_types)

@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PRODUCTS_PER_PAGE']

    # Base query
    query = current_app.extensions['sqlalchemy'].session.query(Product)

    # Apply filters
    brand = request.args.get('brand')
    categories = request.args.getlist('category')
    price_range = request.args.get('price_range')
    protein_range = request.args.get('protein_range')
    search_query = request.args.get('search')

    if brand:
        query = query.filter(Product.brand == brand)

    if categories:
        query = query.filter(Product.type.in_(categories))

    if price_range:
        if price_range == '0-20':
            query = query.filter(and_(Product.price >= 0, Product.price < 20))
        elif price_range == '20-40':
            query = query.filter(and_(Product.price >= 20, Product.price < 40))
        elif price_range == '40-60':
            query = query.filter(and_(Product.price >= 40, Product.price < 60))
        elif price_range == '60+':
            query = query.filter(Product.price >= 60)

    if protein_range:
        if protein_range == '0-15':
            query = query.filter(and_(Product.protein_per_serving >= 0, Product.protein_per_serving < 15))
        elif protein_range == '15-25':
            query = query.filter(and_(Product.protein_per_serving >= 15, Product.protein_per_serving < 25))
        elif protein_range == '25+':
            query = query.filter(Product.protein_per_serving >= 25)

    if search_query:
        search = f"%{search_query}%"
        query = query.filter(or_(
            Product.name.ilike(search),
            Product.brand.ilike(search),
            Product.type.ilike(search)
        ))

    # Apply sorting
    sort = request.args.get('sort', 'name')
    order = request.args.get('order', 'asc')

    if sort == 'price':
        query = query.order_by(Product.price.asc() if order == 'asc' else Product.price.desc())
    elif sort == 'protein':
        query = query.order_by(Product.protein_per_serving.asc() if order == 'asc' else Product.protein_per_serving.desc())
    else:
        query = query.order_by(Product.name.asc() if order == 'asc' else Product.name.desc())

    # Paginate results
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # Get unique brands and categories for filter options
    brands = db.session.query(Product.brand).distinct().order_by(Product.brand)
    categories = db.session.query(Product.type).distinct().order_by(Product.type)

    protein_types = [
        {
            "name": "Whey Protein",
            "icon_class": "icon-whey",
            "description": "Fast-absorbing, milk-derived protein."
        },
        {
            "name": "Casein Protein",
            "icon_class": "icon-casein",
            "description": "Slow-absorbing, milk-derived protein."
        },
        {
            "name": "Plant-based Protein",
            "icon_class": "icon-plant",
            "description": "Protein derived from plant sources like pea, rice, or soy."
        },
        # Add more protein types as needed
    ]
    
    # Modify the query to include protein type information
    products = pagination.items
    for product in products:
        if "whey" in product.type.lower():
            product.protein_type_icon = "icon-whey"
            product.protein_type_description = "Whey protein: Fast-absorbing, milk-derived protein."
        elif "casein" in product.type.lower():
            product.protein_type_icon = "icon-casein"
            product.protein_type_description = "Casein protein: Slow-absorbing, milk-derived protein."
        else:
            product.protein_type_icon = "icon-plant"
            product.protein_type_description = "Plant-based protein: Protein derived from plant sources."
    
    return render_template('index.html', 
                           pagination=pagination,
                           brands=brands,
                           categories=categories,
                           protein_types=protein_types,
                           current_filters={
                               'brand': brand,
                               'category': categories,
                               'price_range': price_range,
                               'protein_range': protein_range,
                               'sort': sort,
                               'order': order,
                               'search': search_query
                           })

@bp.route('/product/<int:id>')
def product_detail(id):
    product = current_app.extensions['sqlalchemy'].session.get(Product, id)
    if product is None:
        abort(404)
    similar_products = current_app.extensions['sqlalchemy'].session.query(Product).filter(
    Product.type == product.type,
    Product.id != product.id
).order_by(func.random()).limit(3).all()
    return render_template('product_detail.html', title=product.name, product=product, similar_products=similar_products)

@bp.route('/compare')
def compare():
    product_ids = request.args.getlist('products')
    
    if len(product_ids) < 2:
        flash('Please select at least two products to compare.', 'warning')
        return redirect(url_for('main.index'))

    products_to_compare = current_app.extensions['sqlalchemy'].session.query(Product).filter(Product.id.in_(product_ids)).all()

    if len(products_to_compare) != len(product_ids):
        flash('One or more selected products could not be found.', 'error')
        return redirect(url_for('main.index'))

    # Prepare data for charts
    chart_data = {
        'labels': [product.name for product in products_to_compare],
        'protein': [product.protein_per_serving for product in products_to_compare],
        'carbs': [product.carbohydrates for product in products_to_compare],
        'fat': [product.fats for product in products_to_compare],
        'sugar': [product.sugar for product in products_to_compare],
        'fiber': [product.dietary_fiber for product in products_to_compare],
        'calories': [product.calories for product in products_to_compare],
        'sodium': [product.sodium for product in products_to_compare],
        'cholesterol': [product.cholesterol for product in products_to_compare]
    }

    return render_template('compare.html', 
                           products=products_to_compare, 
                           chart_data=chart_data)

@bp.route('/search')
def search():
    query = request.args.get('query', '')
    if query:
        search = f"%{query}%"
        products = current_app.extensions['sqlalchemy'].session.query(Product).filter(or_(
    Product.name.ilike(search),
    Product.brand.ilike(search),
    Product.type.ilike(search)
)).limit(10).all()
        return jsonify([{'id': p.id, 'name': p.name, 'brand': p.brand} for p in products])
    return jsonify([])