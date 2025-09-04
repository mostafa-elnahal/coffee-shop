from pathlib import Path
import yaml
from apispec import APISpec

from flask import Flask
from flask_smorest import Api

from config import BaseConfig

from api.api import blueprint

app = Flask(__name__)
app.config.from_object(BaseConfig)

api_spec = yaml.safe_load((Path(__file__).parent / "oas.yaml").read_text())
spec = APISpec(
    title=api_spec["info"]["title"],
    version=api_spec["info"]["version"],
    openapi_version=api_spec["openapi"],
)
spec.to_dict = lambda: api_spec

app.config["API_SPEC"] = spec
kitchen_api = Api(app)

kitchen_api.register_blueprint(blueprint)