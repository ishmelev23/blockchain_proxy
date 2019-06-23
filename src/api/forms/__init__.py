import importlib
import os
import pkgutil
from collections import defaultdict

from src.utils import moduleinfo_to_path

NAME2FORM = defaultdict(lambda: {})

for contract_info in pkgutil.iter_modules(['src/api/forms']):
    for module_info in pkgutil.iter_modules([os.path.join(contract_info.module_finder.path, contract_info.name)]):
        NAME2FORM[module_info.module_finder.path.split(os.sep)[-1]][module_info.name] \
            = importlib.import_module(moduleinfo_to_path(module_info)).ActionForm
