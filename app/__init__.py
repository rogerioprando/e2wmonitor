from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the app
# if we set instant_relative_config to True we can use app.config.from_object('config') to load the config.py file
app = Flask(__name__)

# load the config file
app.config.from_object('config')

db = SQLAlchemy()
db.init_app(app)

from .views.website import website
app.register_blueprint(website)

from .views.auth import auth
app.register_blueprint(auth)
