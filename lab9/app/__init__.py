from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager


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
            "/register": "Register",
            "/login": "Login",
            "/users": "All users",
            "/logout": "Logout",
            "/account": "Account"
        }


app = App().getApp()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# migrate = Migrate(app, db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

from . import controller, models
