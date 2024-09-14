import unittest
from app import create_app, db
from app.models import Product, Category, Admin
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
    PRODUCTS_PER_PAGE = 15

class RouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create an admin user for testing
        self.admin = Admin(username='testadmin')
        self.admin.set_password('testpassword')
        db.session.add(self.admin)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Protein Powder Comparison', response.data)

    def test_product_detail_route(self):
        category = Category(name='Whey Protein')
        product = Product(name='Test Protein', brand='Test Brand', type='Whey', protein_per_serving=25.0, price=39.99, category=category)
        db.session.add(product)
        db.session.commit()

        response = self.client.get(f'/product/{product.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Protein', response.data)

    def test_compare_route(self):
        category = Category(name='Whey Protein')
        product1 = Product(name='Test Protein 1', brand='Test Brand', type='Whey', protein_per_serving=25.0, price=39.99, category=category)
        product2 = Product(name='Test Protein 2', brand='Test Brand', type='Whey', protein_per_serving=30.0, price=49.99, category=category)
        db.session.add_all([product1, product2])
        db.session.commit()

        response = self.client.get(f'/compare?products={product1.id}&products={product2.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Protein 1', response.data)
        self.assertIn(b'Test Protein 2', response.data)

    def test_product_detail_nonexistent_product(self):
        response = self.client.get('/product/9999')  # Assuming 9999 is a non-existent ID
        self.assertEqual(response.status_code, 404)

    def test_compare_route_with_invalid_ids(self):
        response = self.client.get('/compare?products=9999&products=10000')
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertIn('/index', response.location)

    def test_search_route(self):
        category = Category(name='Whey Protein')
        product = Product(name='Test Protein', brand='Test Brand', type='Whey', protein_per_serving=25.0, price=39.99, category=category)
        db.session.add(product)
        db.session.commit()

        response = self.client.get('/search?query=Test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Protein', response.data)

    def test_search_route_no_results(self):
        response = self.client.get('/search?query=NonexistentProduct')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

if __name__ == '__main__':
    unittest.main()