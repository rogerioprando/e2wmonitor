from flask import Flask

# Initialize the app
# if we set instante_relative_config to True we can use app.config.from_object('config') to load the config.py file
app = Flask(__name__)

# load the config file
app.config.from_object('config')

from app.views import home
app.register_blueprint(home.mod)
