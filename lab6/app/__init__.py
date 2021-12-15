from flask import Flask
from flask_sqlalchemy import SQLAlchemy


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
            "/form": "Form",
            "/form_second": "Form_Second"
        }


app = App().getApp()
db = SQLAlchemy(app)

from app import controller