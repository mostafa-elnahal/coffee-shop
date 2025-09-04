from flask import Flask
from flask_smorest import Api

from config import BaseConfig

from api.api import blueprint

app = Flask(__name__)
app.config.from_object(BaseConfig)

kitchen_api = Api(app)

kitchen_api.register_blueprint(blueprint)

