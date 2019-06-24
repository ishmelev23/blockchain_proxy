import importlib
import pkgutil

from src.database.base import Base, DATABASE
from src.utils import moduleinfo_to_path

for module_info in pkgutil.iter_modules(['src/database/models']):
    importlib.import_module(moduleinfo_to_path(module_info))

Base.prepare(DATABASE)
