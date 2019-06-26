import importlib
import pkgutil
from flask import Flask

from settings import BLUEPRINTS_DIR, API_ENDPOINT

import src.database
from src.utils import moduleinfo_to_path

app = Flask(__name__)

# Register api endpoints
for module_info in pkgutil.iter_modules([BLUEPRINTS_DIR]):
    module = importlib.import_module(moduleinfo_to_path(module_info))
    app.register_blueprint(module.blueprint, url_prefix=API_ENDPOINT)

if __name__ == '__main__':
    app.run()
