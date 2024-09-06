from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager # add this import
from config import Config
from flask.cli import with_appcontext
import click

db = SQLAlchemy()
login_manager = LoginManager() # create a loginmanager instance 

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)  # Initialize LoginManager with the app

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    with app.app_context():
        from app import models  # Import models inside app context
    
    @login_manager.user_loader
    def load_user(user_id):
        return models.Admin.query.get(int(user_id))

    @app.cli.command("init-db")
    @with_appcontext
    def init_db_command():
        """Clear the existing data and create new tables."""
        db.create_all()
        click.echo('Initialized the database.')

    return app