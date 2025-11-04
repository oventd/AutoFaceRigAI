import sys
from pathlib import Path
import importlib

PROJECT_ROOT = Path(r"D:\code\AutoFaceRigAI\AutoFaceRigAI").resolve()

# Ensure project root is importable
project_root_str = str(PROJECT_ROOT)
if project_root_str not in sys.path:
    sys.path.insert(0, project_root_str)

# Also add the 'turntable' folder to support legacy absolute imports inside it
turntable_dir = PROJECT_ROOT / "turntable"
turntable_dir_str = str(turntable_dir)
if turntable_dir.exists() and turntable_dir_str not in sys.path:
    sys.path.insert(0, turntable_dir_str)

importlib.invalidate_caches()

# Pre-import and alias modules so bare imports inside turntable/* work
def _ensure_alias(pkg_name: str, alias_name: str):
    try:
        pkg_mod = importlib.import_module(pkg_name)
        # If alias not set, point it to the same module object
        if alias_name not in sys.modules:
            sys.modules[alias_name] = pkg_mod
    except Exception as e:
        print(f"failed: {pkg_name} (alias {alias_name}) -> {e}")

# Order matters: camera_creator depends on position_calculator
_ensure_alias("turntable.position_calculator", "position_calculator")
_ensure_alias("turntable.playblast_generator", "playblast_generator")
_ensure_alias("turntable.camera_creator", "camera_creator")
_ensure_alias("turntable.TurnTable_generator", "TurnTable_generator")

# Bulk import all modules under project for hot-reload-like behavior
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
