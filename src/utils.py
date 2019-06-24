import os
from pkgutil import ModuleInfo


def moduleinfo_to_path(module_info: ModuleInfo) -> str:
    return os.path.join(module_info.module_finder.path, module_info.name).replace('/', '.')
