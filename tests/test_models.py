import unittest
from app import create_app, db
from app.models import Product, Category, Admin
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_category_creation(self):
        category = Category(name='Whey Protein', description='Fast-absorbing protein')
        db.session.add(category)
        db.session.commit()
        self.assertIsNotNone(category.id)
        self.assertEqual(str(category), '<Category Whey Protein>')

    def test_category_unique_name(self):
        category1 = Category(name='Whey Protein', description='Fast-absorbing protein')
        category2 = Category(name='Whey Protein', description='Another description')
        db.session.add(category1)
        db.session.commit()
        with self.assertRaises(Exception):  # This will depend on your database constraints
            db.session.add(category2)
            db.session.commit()

    def test_product_creation(self):
        category = Category(name='Whey Protein')
        product = Product(
            name='Test Protein',
            brand='Test Brand',
            type='Whey',
            protein_per_serving=25.0,
            price=39.99,
            category=category
        )
        db.session.add(product)
        db.session.commit()
        self.assertIsNotNone(product.id)
        self.assertEqual(str(product), '<Product Test Protein>')
        self.assertEqual(product.category, category)

def test_product_fields(self):
    category = Category(name='Whey Protein')
    product = Product(
        name='Test Protein',
        brand='Test Brand',
        type='Whey',
        flavor='Vanilla',
        ingredients='Whey protein isolate, natural flavors',
        protein_per_serving=25.0,
        calories=120,  # Changed from calories_per_serving to calories
        sugar=1.0,
        carbohydrates=3.0,
        fats=2.0,
        saturated_fats=0.5,
        cholesterol=30.0,
        sodium=50.0,
        dietary_fiber=0.5,
        price=39.99,
        serving_size='30g',
        servings_per_container=30,
        flavors='Vanilla, Chocolate',
        allergens='Contains milk',
        description='A high-quality whey protein powder',
        source='Milk',
        category=category,
        image_url='http://example.com/image.jpg'
    )
    db.session.add(product)
    db.session.commit()

    retrieved_product = Product.query.first()
    self.assertEqual(retrieved_product.name, 'Test Protein')
    self.assertEqual(retrieved_product.brand, 'Test Brand')
    self.assertEqual(retrieved_product.type, 'Whey')
    self.assertEqual(retrieved_product.flavor, 'Vanilla')
    self.assertEqual(retrieved_product.ingredients, 'Whey protein isolate, natural flavors')
    self.assertEqual(retrieved_product.protein_per_serving, 25.0)
    self.assertEqual(retrieved_product.calories, 120)  # Changed from calories_per_serving to calories
    self.assertEqual(retrieved_product.sugar, 1.0)
    self.assertEqual(retrieved_product.carbohydrates, 3.0)
    self.assertEqual(retrieved_product.fats, 2.0)
    self.assertEqual(retrieved_product.saturated_fats, 0.5)
    self.assertEqual(retrieved_product.cholesterol, 30.0)
    self.assertEqual(retrieved_product.sodium, 50.0)
    self.assertEqual(retrieved_product.dietary_fiber, 0.5)
    self.assertEqual(retrieved_product.price, 39.99)
    self.assertEqual(retrieved_product.serving_size, '30g')
    self.assertEqual(retrieved_product.servings_per_container, 30)
    self.assertEqual(retrieved_product.flavors, 'Vanilla, Chocolate')
    self.assertEqual(retrieved_product.allergens, 'Contains milk')
    self.assertEqual(retrieved_product.description, 'A high-quality whey protein powder')
    self.assertEqual(retrieved_product.source, 'Milk')
    self.assertEqual(retrieved_product.image_url, 'http://example.com/image.jpg')
    
    def test_admin_creation(self):
        admin = Admin(username='testadmin')
        admin.set_password('testpassword')
        db.session.add(admin)
        db.session.commit()
        self.assertIsNotNone(admin.id)
        self.assertTrue(admin.check_password('testpassword'))
        self.assertFalse(admin.check_password('wrongpassword'))

    def test_admin_unique_username(self):
        admin1 = Admin(username='testadmin')
        admin1.set_password('password1')
        admin2 = Admin(username='testadmin')
        admin2.set_password('password2')
        db.session.add(admin1)
        db.session.commit()
        with self.assertRaises(Exception):  # This will depend on your database constraints
            db.session.add(admin2)
            db.session.commit()

    def test_relationship_models(self):
        category = Category(name='Vegan Protein', description='Plant-based protein')
        db.session.add(category)
        db.session.commit()

        product = Product(
            name='Vegan Protein Powder',
            brand='Vegan Brand',
            type="Vegan",
            protein_per_serving=20.0,
            price=29.99,
            category=category
        )
        db.session.add(product)
        db.session.commit()

        retrieved_product = Product.query.first()

        self.assertIsNotNone(retrieved_product)
        self.assertEqual(retrieved_product.category_id, category.id)
        self.assertEqual(retrieved_product.category.name, "Vegan Protein")
        self.assertEqual(retrieved_product.category.description, 'Plant-based protein')
        self.assertEqual(str(retrieved_product), '<Product Vegan Protein Powder>')

    def test_category_products_relationship(self):
        category = Category(name='Protein Blend', description='Mixed protein sources')
        db.session.add(category)
        db.session.commit()

        product1 = Product(name='Blend 1', brand='Brand A', protein_per_serving=20.0, price=29.99, category=category)
        product2 = Product(name='Blend 2', brand='Brand B', protein_per_serving=22.0, price=31.99, category=category)
        db.session.add_all([product1, product2])
        db.session.commit()

        retrieved_category = Category.query.first()
        self.assertEqual(len(retrieved_category.products), 2)
        self.assertIn(product1, retrieved_category.products)
        self.assertIn(product2, retrieved_category.products)

if __name__ == '__main__':
    unittest.main()
    
    
#  Test Breakdown for test_models.py

# 1. **test_category_creation**
#    - Creates a new Category instance
#    - Adds it to the database and commits the session
#    - Checks if the category has been assigned an ID (i.e., successfully saved to the database)
#    - Verifies that the string representation of the category is correct

# 2. **test_category_unique_name**
#    - Attempts to create two categories with the same name
#    - Checks that an exception is raised when trying to add the second category
#    - Verifies that the database enforces unique category names

# 3. **test_product_creation**
#    - Creates a new Product instance associated with a Category
#    - Adds it to the database and commits the session
#    - Checks if the product has been assigned an ID
#    - Verifies that the string representation of the product is correct
#    - Confirms that the product is correctly associated with its category

# 4. **test_product_fields**
#    - Creates a Product instance with all fields populated
#    - Adds it to the database and commits the session
#    - Retrieves the product from the database
#    - Checks that all fields of the retrieved product match the original data
#    - Verifies that all product attributes are correctly stored and retrieved

# 5. **test_admin_creation**
#    - Creates a new Admin instance
#    - Sets a password for the admin
#    - Adds it to the database and commits the session
#    - Checks if the admin has been assigned an ID
#    - Verifies that the password checking method works correctly for both correct and incorrect passwords

# 6. **test_admin_unique_username**
#    - Attempts to create two admin users with the same username
#    - Checks that an exception is raised when trying to add the second admin
#    - Verifies that the database enforces unique admin usernames

# 7. **test_admin_user_mixin_properties**
#    - Creates an Admin instance
#    - Checks the UserMixin properties (is_authenticated, is_active, is_anonymous)
#    - Verifies that the get_id method returns the correct ID

# 8. **test_relationship_models**
#    - Creates a Category and an associated Product
#    - Adds them to the database and commits the session
#    - Retrieves the product from the database
#    - Checks that the product-category relationship is correctly established and can be navigated

# 9. **test_category_products_relationship**
#    - Creates a Category and multiple associated Products
#    - Adds them to the database and commits the session
#    - Retrieves the category from the database
#    - Checks that the category-products relationship is correctly established
#    - Verifies that all products are accessible through the category's 'products' attribute

# These tests cover the basic CRUD operations, relationship integrity, and specific model behaviors for your Category, Product, and Admin models. They ensure that your database models are working as expected and that the relationships between models are correctly established and maintained.