import sys
from pathlib import Path
import importlib

PROJECT_ROOT = Path(r"D:\code\AutoFaceRigAI\AutoFaceRigAI").resolve()

project_root_str = str(PROJECT_ROOT)
if project_root_str not in sys.path:
    sys.path.insert(0, project_root_str)

importlib.invalidate_caches()

module_names = []
for py_file in PROJECT_ROOT.rglob("*.py"):
    rel = py_file.relative_to(PROJECT_ROOT).with_suffix("")
    mod_name = ".".join(rel.parts)
    if not mod_name or mod_name == "run":
        continue
    module_names.append(mod_name)

module_names.sort(key=len, reverse=True)

for mod_name in module_names:
    try:
        if mod_name in sys.modules:
            importlib.reload(sys.modules[mod_name])
        else:
            importlib.import_module(mod_name)
    except Exception as e:
        print(f"failed: {mod_name} -> {e}")

from controller import UI
ui = UI()
print("done")