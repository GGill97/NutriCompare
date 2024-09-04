from flask import Blueprint

bp = Blueprint('admin', __name__)

print("Registering admin routes...")
from app.admin import routes
print("Admin routes registered.")