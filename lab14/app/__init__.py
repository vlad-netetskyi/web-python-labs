from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config


class App:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(App, cls).__new__(cls)
            cls.instance.__app = Flask(__name__)
            cls.instance.__app.config.from_object('config')
        return cls.instance

    def getApp(self):
        return self.__app

    @staticmethod
    def getMenu():
        return {
            "/": "Home",
            "/about": "About me",
            "/achievements": "Achievements",
            "/form/form_second": "Form",
            "/auth/register": "Register",
            "/auth/login": "Login",
            "/auth/users": "All users",
            "/auth/logout": "Logout",
            "/auth/account": "Account",
            "/post": "Posts",
            "/post/create": "Create post"
        }


# app = App().getApp()
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'


def create_app(config_name='default'):
    """Construct the core application."""
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config.get(config_name))
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.jinja_env.globals.update(slice_post_text=slice_post_text)

    with app.app_context():
        # Imports
        from . import controller

        from .auth import auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='/auth')

        from .form import form_blueprint
        app.register_blueprint(form_blueprint, url_prefix='/form')

        from .posts import post_blueprint
        app.register_blueprint(post_blueprint, url_prefix='/post')

        return app


def slice_post_text(text):
    return text[:50] + "..."
