import sys
import os
from pathlib import Path
import importlib

ROOT = r"D:\code\AutoFaceRigAI"

root_path = Path(ROOT)

if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

python_files = []
dirs = [root_path]
visited = set()

while dirs:
    p = dirs.pop()
    if p in visited:
        continue
    visited.add(p)
    if p.is_dir():
        if str(p) not in sys.path:
            sys.path.append(str(p))
        dirs.extend(p.iterdir())
    elif p.is_file() and p.suffix == ".py":
        python_files.append(p.resolve())

module_by_path = {}

for name, module in list(sys.modules.items()):
    module_file = getattr(module, "__file__", None)
    if not module_file:
        continue
    try:
        module_path = Path(module_file).resolve()
    except Exception:
        continue
    key = module_path.with_suffix(".py")
    if key not in module_by_path:
        module_by_path[key] = []
    module_by_path[key].append(module)

for py_path in python_files:
    modules = module_by_path.get(py_path, [])
    if modules:
        for m in modules:
            try:
                importlib.reload(m)
            except Exception as e:
                print("failed to reload", m.__name__, e)
    else:
        mod_name = py_path.stem
        try:
            if mod_name in sys.modules:
                importlib.reload(sys.modules[mod_name])
            else:
                importlib.import_module(mod_name)
        except Exception as e:
            print("failed to import by name", mod_name, e)

if __name__ == "__main__":
    from controller import UI
    ui = UI()
