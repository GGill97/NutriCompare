from app import create_app, db
from app.models import Category, Product
from sqlalchemy import func

app = create_app()

def reset_products():
    with app.app_context():
        try:
            # Delete all existing products
            Product.query.delete()
            db.session.commit()
            print("All existing products deleted.")

            # Define new products
            products = [
                {
                    "name": "Super Whey Pro",
                    "brand": "FitnessFuel",
                    "type": "Whey Protein Isolate",
                    "price": 54.99,
                    "size": "5 lbs",
                    "servings_per_container": 75,
                    "protein_per_serving": 25,
                    "serving_size": "30g",
                    "flavors": ["Chocolate", "Vanilla", "Strawberry"],
                    "nutritional_info": {
                        "calories": 120,
                        "total_fat": 1,
                        "saturated_fat": 0.5,
                        "cholesterol": 5,
                        "sodium": 50,
                        "total_carbohydrate": 2,
                        "dietary_fiber": 0,
                        "sugars": 1,
                        "protein": 25
                    }
                },
                {
                    "name": "Vegan Blend Supreme",
                    "brand": "GreenProtein",
                    "type": "Vegan Protein Blend",
                    "price": 39.99,
                    "size": "2 lbs",
                    "servings_per_container": 30,
                    "protein_per_serving": 20,
                    "serving_size": "33g",
                    "flavors": ["Chocolate", "Vanilla", "Berry"],
                    "nutritional_info": {
                        "calories": 130,
                        "total_fat": 2.5,
                        "saturated_fat": 0,
                        "cholesterol": 0,
                        "sodium": 300,
                        "total_carbohydrate": 6,
                        "dietary_fiber": 2,
                        "sugars": 0,
                        "protein": 20
                    }
                },
                # Add more products as needed
            ]

            # Ensure categories exist
            categories = {
                'Whey Protein Isolate': Category.query.filter_by(name='Whey Protein Isolate').first() or Category(name='Whey Protein Isolate'),
                'Vegan Protein Blend': Category.query.filter_by(name='Vegan Protein Blend').first() or Category(name='Vegan Protein Blend'),
                # Add more categories as needed
            }

            for category in categories.values():
                if category.id is None:
                    db.session.add(category)

            db.session.commit()

            # Add new products
            for product_data in products:
                category = categories.get(product_data['type'])
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
                    flavors=", ".join(product_data['flavors']),
                    category=category
                )
                db.session.add(product)

            db.session.commit()
            print("New products added successfully!")

            # Verify products were added
            products = Product.query.all()
            for product in products:
                print(f"{product.name} - {product.brand} - {product.type} - ${product.price}")

        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {str(e)}")
        finally:
            db.session.close()

if __name__ == "__main__":
    reset_products()
    
    
# Summary
# Purpose: This script resets the Product table in your database by deleting all existing entries and adding a fresh set of predefined products.
# Key Steps:
# Deletes old products.
# Ensures necessary categories are present.
# Adds new products with associated data.
# Verifies that the products were added correctly.
# This script is useful for quickly resetting your product data, especially during development or testing phases.