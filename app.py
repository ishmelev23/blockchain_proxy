import importlib
import os
import pkgutil

from settings import BLUEPRINTS_DIR, API_ENDPOINT
from flask import Flask

app = Flask(__name__)

# Register api endpoints
for module_info in pkgutil.iter_modules([BLUEPRINTS_DIR]):
    module = importlib.import_module(os.path.join(BLUEPRINTS_DIR, module_info.name).replace('/', '.'))
    app.register_blueprint(module.blueprint, url_prefix=API_ENDPOINT)


if __name__ == '__main__':
    app.run()
