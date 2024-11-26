from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contracts.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        from .routes import init_routes
        init_routes(app)

    return app

def init_db(app):
    with app.app_context():
        # Import all models here
        from .models import User, Contract
        # Create database tables
        db.create_all()
        print("Database tables created.")
