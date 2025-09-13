from pathlib import Path
import yaml
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(debug=True, openapi_url="/openapi/orders.json", docs_url="/docs/orders")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oas_doc = yaml.safe_load(
    (Path(__file__).parent / '../../oas.yaml').read_text()
)
app.openapi_schema = oas_doc

from .api import api