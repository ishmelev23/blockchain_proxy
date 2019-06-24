import importlib
import json
import os
import pkgutil
from collections import defaultdict

from src.utils import moduleinfo_to_path

NAME2FORM = defaultdict(lambda: {'address': None})

for contract_info in pkgutil.iter_modules(['src/api/forms']):
    address = getattr(importlib.import_module('src.api.forms.%s' % contract_info.name), 'address', None)
    abi = getattr(importlib.import_module('src.api.forms.%s' % contract_info.name), 'abi', None)
    if abi:
        try:
            abi = json.loads(abi)
        except:
            abi = None

    assert address, "You should setup contract address"
    assert abi, "You should setup valid contract abi"

    NAME2FORM[contract_info.name].update({
        'abi': abi,
        'address': address
    })
    for module_info in pkgutil.iter_modules([os.path.join(contract_info.module_finder.path, contract_info.name)]):
        NAME2FORM[contract_info.name][module_info.name] \
            = importlib.import_module(moduleinfo_to_path(module_info)).ActionForm
