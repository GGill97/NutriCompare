import unittest
from app import create_app, db
from app.models import Product, Category, Admin
from config import Config



# def test_something(self):
#     # Set up any necessary data
#     # Perform an action
#     # Check the result
#     self.assertEqual(expected_result, actual_result)


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
    
    
class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()  # Add the client for route tests
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

    def test_admin_creation(self):
        admin = Admin(username='testadmin')
        admin.set_password('testpassword')
        db.session.add(admin)
        db.session.commit()
        self.assertIsNotNone(admin.id)
        self.assertTrue(admin.check_password('testpassword'))
        self.assertFalse(admin.check_password('wrongpassword'))

    def test_relationship_models(self):
        #create a category
        category =  Category(name='Vegan Protein', description='Plant-based protein')
        db.session.add(category)
        db.session.commit()
        #create a product associated with the category
        product = Product (
            name= 'Vegan Protein Powder',
            brand = 'Vegan Brand',
            type = "Vegan",
            protein_per_serving = 20.0,
            price = 29.99,
            category = category
        )
        db.session.add(product)
        db.session.commit()
        
        #Retreieve the product from the database
        retrieved_product = Product.query.first()
        
        #Check if the product is correctly lined to the category
        self.assertIsNotNone(retrieved_product)
        self.assertEqual(retrieved_product.category_id, category.id)
        self.assertEqual(retrieved_product.category.name,"Vegan Protein")
        self.assertEqual(retrieved_product.category.description, 'Plant-based protein')
        self.assertEqual(str(retrieved_product), '<Product Vegan Protein Powder>')
        
        
        
        
        
        
        
        
        
if __name__ == '__main__':
    unittest.main()