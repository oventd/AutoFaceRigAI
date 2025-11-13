import sys
import os
from pathlib import Path
import importlib

ROOT = Path(__file__).resolve().parent

root_path = ROOT
sys.path.append(str(root_path))
visited = {root_path}
python_files = []
dirs = list(root_path.iterdir())
while dirs:
    node = dirs.pop()
    if node in visited:
        continue
    visited.add(node)
    if node.is_dir():
        sys.path.append(str(node))
        dirs.extend(node.iterdir())
        continue
    if node.is_file() and node.suffix == ".py":
        python_files.append(node)

for python_file in python_files:
    mod_name = python_file.stem
    if mod_name == Path(__file__).stem:
        continue
    if mod_name in sys.modules:
        importlib.reload(sys.modules[mod_name])
    importlib.import_module(mod_name)

if __name__ == "__main__":
    from controller import UI
    ui = UI()
