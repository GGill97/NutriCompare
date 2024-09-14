from app import create_app, db
from app.models import Product, Category

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Product': Product, 'Category': Category}


# Summary
# run.py initializes your Flask app and makes it convenient to work with your database models from the command line.
# create_app() sets up your Flask app.
# db represents the connection to your database.
# Product and Category are your data models.
# Shell context allows easy access to db, Product, and Category when using the Flask shell.
