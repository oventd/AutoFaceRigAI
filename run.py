import sys
import os
from pathlib import Path
import importlib

ROOT = r"D:\code\AutoFaceRigAI"

root_path = Path(ROOT)
sys.path.append(str(root_path))
visited = set()
visited.add(root_path)
python_files = []
dirs = list(root_path.iterdir())
for dir in dirs:
    if dir in visited:
        continue
    if dir.is_dir():
        sys.path.append(str(dir))
        dirs.extend(list(dir.iterdir()))
    if dir.is_file():
        if dir.suffix != ".py":
            continue
        python_files.append(dir)
    
    visited.add(dir)

print(python_files)

for python_file in python_files:
    importlib.reload(sys.modules[python_file.stem])
    importlib.import_module(python_file.stem)

if __name__ == "__main__":
    from controller import UI
    ui = UI()