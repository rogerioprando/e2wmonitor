from flask import Flask

# Initialize the app
# if we set instante_relative_config to True we can use app.config.from_object('config') to load the config.py file
app = Flask(__name__)

# load the config file
app.config.from_object('config')

from .views.website import website
app.register_blueprint(website)

from .views.auth import auth
app.register_blueprint(auth)
