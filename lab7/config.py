import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'SuprePuperSecret'
WTF_CSRF_ENABLED = True

# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
