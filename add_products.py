from app import create_app, db
from app.models import Category, Product
from sqlalchemy import func
app = create_app()
with app.app_context():
  Product.query.delete()
  db.session.commit()
  print("All existing products deleted.")

  products = [
    # Whey Proteins
    {
    "id": 39,
    "name": "Organic Pea Protein",
    "brand": "Bulk Supplements",
    "type": "Pea Protein Isolate",
    "price": 19.96,
    "size": "1 kg",
    "servings_per_container": 40,
    "protein_per_serving": 24,
    "serving_size": "25g",
    "flavors": ["Unflavored"],
    "nutritional_info": {
      "calories": 100,
      "total_fat": 0.5,
      "saturated_fat": 0,
      "cholesterol": 0,
      "sodium": 230,
      "total_carbohydrate": 1,
      "dietary_fiber": 1,
      "sugars": 0,
      "protein": 24
    },
    "ingredients": [
      "Organic Pea Protein Isolate"
    ]
  },
  {
    "id": 40,
    "name": "Grass-Fed Whey Isolate",
    "brand": "ProMix Nutrition",
    "type": "Grass-Fed Whey Protein Isolate",
    "price": 79.99,
    "size": "5 lbs",
    "servings_per_container": 76,
    "protein_per_serving": 30,
    "serving_size": "31g",
    "flavors": ["Unflavored", "Chocolate", "Vanilla"],
    "nutritional_info": {
      "calories": 115,
      "total_fat": 0,
      "saturated_fat": 0,
      "cholesterol": 5,
      "sodium": 55,
      "total_carbohydrate": 1,
      "dietary_fiber": 0,
      "sugars": 0,
      "protein": 30
    },
    "ingredients": [
      "Grass-Fed Whey Protein Isolate",
      "Sunflower Lecithin",
      "Natural Flavors (for flavored versions)",
      "Stevia Leaf Extract (for flavored versions)"
    ]
  },
  {
    "id": 41,
    "name": "Plant-Based Protein",
    "brand": "Orgain",
    "type": "Organic Plant Protein Blend",
    "price": 26.99,
    "size": "2.03 lbs",
    "servings_per_container": 20,
    "protein_per_serving": 21,
    "serving_size": "46g",
    "flavors": ["Creamy Chocolate Fudge", "Vanilla Bean", "Peanut Butter"],
    "nutritional_info": {
      "calories": 150,
      "total_fat": 4,
      "saturated_fat": 0.5,
      "cholesterol": 0,
      "sodium": 200,
      "total_carbohydrate": 15,
      "dietary_fiber": 7,
      "sugars": 1,
      "protein": 21
    },
    "ingredients": [
      "Organic Pea Protein",
      "Organic Brown Rice Protein",
      "Organic Chia Seed",
      "Organic Cocoa Powder (for Chocolate flavor)",
      "Organic Natural Flavors",
      "Organic Erythritol",
      "Organic Stevia"
    ]
  },
  {
    "id": 42,
    "name": "ISO100",
    "brand": "Dymatize",
    "type": "Hydrolyzed Whey Protein Isolate",
    "price": 64.99,
    "size": "5 lbs",
    "servings_per_container": 71,
    "protein_per_serving": 25,
    "serving_size": "32g",
    "flavors": ["Gourmet Chocolate", "Smooth Banana", "Birthday Cake"],
    "nutritional_info": {
      "calories": 110,
      "total_fat": 0.5,
      "saturated_fat": 0,
      "cholesterol": 5,
      "sodium": 160,
      "total_carbohydrate": 1,
      "dietary_fiber": 0,
      "sugars": 0,
      "protein": 25
    },
    "ingredients": [
      "Hydrolyzed Whey Protein Isolate",
      "Whey Protein Isolate",
      "Natural and Artificial Flavors",
      "Salt",
      "Soy Lecithin",
      "Sucralose"
    ]
  },
  {
    "id": 43,
    "name": "Beef Protein Isolate",
    "brand": "CarnivoreMuscle",
    "type": "Beef Protein Isolate",
    "price": 39.99,
    "size": "2 lbs",
    "servings_per_container": 28,
    "protein_per_serving": 23,
    "serving_size": "30g",
    "flavors": ["Chocolate", "Vanilla", "Unflavored"],
    "nutritional_info": {
      "calories": 110,
      "total_fat": 0,
      "saturated_fat": 0,
      "cholesterol": 0,
      "sodium": 340,
      "total_carbohydrate": 0,
      "dietary_fiber": 0,
      "sugars": 0,
      "protein": 23
    },
    "ingredients": [
      "Beef Protein Isolate",
      "Cocoa Powder (for Chocolate flavor)",
      "Natural and Artificial Flavors",
      "Salt",
      "Acesulfame Potassium",
      "Sucralose"
    ]
  },
  {
    "id": 44,
    "name": "Organic Brown Rice Protein",
    "brand": "Nutribiotic",
    "type": "Brown Rice Protein",
    "price": 24.95,
    "size": "1.5 lbs",
    "servings_per_container": 30,
    "protein_per_serving": 12,
    "serving_size": "15g",
    "flavors": ["Plain"],
    "nutritional_info": {
      "calories": 60,
      "total_fat": 0.5,
      "saturated_fat": 0,
      "cholesterol": 0,
      "sodium": 5,
      "total_carbohydrate": 2,
      "dietary_fiber": 1,
      "sugars": 0,
      "protein": 12
    },
    "ingredients": [
      "Organic Sprouted Brown Rice Protein"
    ]
  },
  {
    "id": 45,
    "name": "Nitro-Tech",
    "brand": "MuscleTech",
    "type": "Whey Protein Blend",
    "price": 49.99,
    "size": "4 lbs",
    "servings_per_container": 40,
    "protein_per_serving": 30,
    "serving_size": "46g",
    "flavors": ["Milk Chocolate", "Vanilla Birthday Cake", "Cookies and Cream"],
    "nutritional_info": {
      "calories": 160,
      "total_fat": 2,
      "saturated_fat": 1,
      "cholesterol": 90,
      "sodium": 160,
      "total_carbohydrate": 4,
      "dietary_fiber": 1,
      "sugars": 2,
      "protein": 30
    },
    "ingredients": [
      "Whey Protein Isolate",
      "Whey Peptides",
      "Whey Protein Concentrate",
      "Cocoa (Processed with Alkali)",
      "Natural and Artificial Flavors",
      "Soy Lecithin",
      "Acesulfame-Potassium",
      "Sucralose"
    ]
  },
  {
    "id": 46,
    "name": "Organic Hemp Protein",
    "brand": "Manitoba Harvest",
    "type": "Hemp Protein",
    "price": 14.99,
    "size": "16 oz",
    "servings_per_container": 15,
    "protein_per_serving": 15,
    "serving_size": "30g",
    "flavors": ["Unflavored"],
    "nutritional_info": {
      "calories": 110,
      "total_fat": 3,
      "saturated_fat": 0,
      "cholesterol": 0,
      "sodium": 0,
      "total_carbohydrate": 9,
      "dietary_fiber": 8,
      "sugars": 1,
      "protein": 15
    },
    "ingredients": [
      "Organic Hemp Protein Powder"
    ]
  },
  {
    "id": 47,
    "name": "Syntha-6",
    "brand": "BSN",
    "type": "Protein Matrix",
    "price": 54.99,
    "size": "5 lbs",
    "servings_per_container": 48,
    "protein_per_serving": 22,
    "serving_size": "47g",
    "flavors": ["Chocolate Milkshake", "Vanilla Ice Cream", "Strawberry Milkshake"],
    "nutritional_info": {
      "calories": 200,
      "total_fat": 6,
      "saturated_fat": 2,
      "cholesterol": 55,
      "sodium": 220,
      "total_carbohydrate": 15,
      "dietary_fiber": 1,
      "sugars": 4,
      "protein": 22
    },
    "ingredients": [
      "Protein Matrix (Whey Protein Concentrate, Whey Protein Isolate, Calcium Caseinate, Micellar Casein, Milk Protein Isolate, Egg Albumen)",
      "Cocoa Powder (Processed with Alkali)",
      "Natural and Artificial Flavors",
      "Sunflower Powder",
      "Lecithin",
      "Cellulose Gum",
      "Acesulfame Potassium",
      "Sucralose"
    ]
  },
  {
    "id": 48,
    "name": "Organic Quinoa Protein",
    "brand": "TruRoots",
    "type": "Quinoa Protein",
    "price": 19.99,
    "size": "8 oz",
    "servings_per_container": 15,
    "protein_per_serving": 8,
    "serving_size": "15g",
    "flavors": ["Unflavored"],
    "nutritional_info": {
      "calories": 60,
      "total_fat": 1,
      "saturated_fat": 0,
      "cholesterol": 0,
      "sodium": 0,
      "total_carbohydrate": 9,
      "dietary_fiber": 2,
      "sugars": 0,
      "protein": 8
    },
    "ingredients": [
      "Organic Quinoa Protein Powder"
    ]
  },
  {
    "id": 49,
    "name": "Ascent Native Fuel",
    "brand": "Ascent",
    "type": "Native Whey Protein Isolate",
    "price": 39.99,
    "size": "2 lbs",
    "servings_per_container": 27,
    "protein_per_serving": 25,
    "serving_size": "33g",
    "flavors": ["Chocolate", "Vanilla Bean", "Cappuccino"],
    "nutritional_info": {
      "calories": 120,
      "total_fat": 1,
      "saturated_fat": 0,
      "cholesterol": 30,
      "sodium": 55,
      "total_carbohydrate": 3,
      "dietary_fiber": 0,
      "sugars": 1,
      "protein": 25
    },
    "ingredients": [
      "Native Whey Protein Isolate",
      "Natural Flavors",
      "Sunflower Lecithin",
      "Monk Fruit Extract",
      "Stevia Leaf Extract"
    ]
  },
  {
    "id": 50,
    "name": "Multi-Source Protein",
    "brand": "MusclePharm",
    "type": "Protein Blend",
    "price": 54.99,
    "size": "4 lbs",
    "servings_per_container": 52,
    "protein_per_serving": 24,
    "serving_size": "35g",
    "flavors": ["Chocolate Milk", "Vanilla Ice Cream", "Cookies N' Cream"],
    "nutritional_info": {
      "calories": 130,
      "total_fat": 2,
      "saturated_fat": 1,
      "cholesterol": 60,
      "sodium": 140,
      "total_carbohydrate": 4,
      "dietary_fiber": 1,
      "sugars": 1,
      "protein": 24
    },
    "ingredients": [
      "Protein Blend (Whey Protein Concentrate, Milk Protein Concentrate, Whey Protein Isolate, Micellar Casein, Egg White Albumen, L-Glutamine)",
      "Cocoa Powder",
      "Natural and Artificial Flavors",
      "Salt",
      "Cellulose Gum",
      "Sucralose",
      "Acesulfame Potassium"
    ]
  }
]

# Ensure categories exist
  categories = {
        'Whey Protein Concentrate': Category.query.filter_by(name='Whey Protein Concentrate').first() or Category(name='Whey Protein Concentrate'),
        'Whey Protein Isolate': Category.query.filter_by(name='Whey Protein Isolate').first() or Category(name='Whey Protein Isolate'),
        'Hydrolyzed Whey Protein': Category.query.filter_by(name='Hydrolyzed Whey Protein').first() or Category(name='Hydrolyzed Whey Protein'),
        'Pea Protein': Category.query.filter_by(name='Pea Protein').first() or Category(name='Pea Protein'),
        'Vegan Protein Blend': Category.query.filter_by(name='Vegan Protein Blend').first() or Category(name='Vegan Protein Blend'),
        'Casein Protein': Category.query.filter_by(name='Casein Protein').first() or Category(name='Casein Protein'),
        'Protein Blend': Category.query.filter_by(name='Protein Blend').first() or Category(name='Protein Blend'),
        'Egg White Protein': Category.query.filter_by(name='Egg White Protein').first() or Category(name='Egg White Protein'),
        'Hemp Protein': Category.query.filter_by(name='Hemp Protein').first() or Category(name='Hemp Protein'),
        'Soy Protein': Category.query.filter_by(name='Soy Protein').first() or Category(name='Soy Protein'),
        'Collagen Protein': Category.query.filter_by(name='Collagen Protein').first() or Category(name='Collagen Protein'),
        'Brown Rice Protein': Category.query.filter_by(name='Brown Rice Protein').first() or Category(name='Brown Rice Protein'),
        'Beef Protein': Category.query.filter_by(name='Beef Protein').first() or Category(name='Beef Protein'),
        'Bone Broth Protein': Category.query.filter_by(name='Bone Broth Protein').first() or Category(name='Bone Broth Protein'),
        'Goat Whey Protein': Category.query.filter_by(name='Goat Whey Protein').first() or Category(name='Goat Whey Protein'),
        'Cricket Protein': Category.query.filter_by(name='Cricket Protein').first() or Category(name='Cricket Protein'),
        'Quinoa Protein': Category.query.filter_by(name='Quinoa Protein').first() or Category(name='Quinoa Protein'),
        'Protein Blend': Category.query.filter_by(name='Protein Blend').first() or Category(name='Protein Blend'), 
    }

  for category in categories.values():
        if category.id is None:
            db.session.add(category)

  db.session.commit()

    # Add products
  for product_data in products:
        # Find the appropriate category
      category = None
      for cat_name, cat_obj in categories.items():
            if cat_name.lower() in product_data['type'].lower():
                category = cat_obj
                break
        
      if not category:
            print(f"Unknown category for product {product_data['name']} with type {product_data['type']}")
            continue

      product = Product(
            name=product_data['name'],
            brand=product_data['brand'],
            type=product_data['type'],
            protein_per_serving=product_data['protein_per_serving'],
            calories=product_data['nutritional_info']['calories'],
            price=product_data['price'],
            serving_size=product_data['serving_size'],
            servings_per_container=product_data['servings_per_container'],
            flavors=", ".join(product_data['flavors']),  # Join flavors into a string
            category=category
        )
      db.session.add(product)

  db.session.commit()

  print("Products added successfully!")

    # Remove duplicates
  for name, in db.session.query(Product.name).group_by(Product.name).having(func.count() > 1):
        duplicates = Product.query.filter_by(name=name).order_by(Product.id.desc()).all()[1:]
        for duplicate in duplicates:
            db.session.delete(duplicate)
  db.session.commit()

  print("Duplicates removed.")

    # Verify products were added
  products = Product.query.all()
  for product in products:
        print(f"{product.name} - {product.brand} - {product.type} - ${product.price}")