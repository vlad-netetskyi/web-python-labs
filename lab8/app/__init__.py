from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate


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
            "/users": "All users"
        }


app = App().getApp()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

from . import controller
