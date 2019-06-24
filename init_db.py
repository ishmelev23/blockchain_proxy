import importlib
import pkgutil

from src.database import Base
from src.utils import moduleinfo_to_path

for module_info in pkgutil.iter_modules(['src/models']):
    importlib.import_module(moduleinfo_to_path(module_info))

Base.metadata.create_all()
