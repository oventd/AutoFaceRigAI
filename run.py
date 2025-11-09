import sys
import os
from pathlib import Path
import importlib

# Resolve project root robustly (works when __file__ is unavailable in Maya)
def _detect_project_root() -> Path:
    # 1) Prefer location of this file
    try:
        here = Path(r"D:\code\AutoFaceRigAI").resolve()
        if (here / "controller.py").exists() or (here / "model.py").exists():
            return here
    except NameError:
        # Running from a string (e.g., Maya Script Editor)
        pass

    # 2) Check sys.path entries for a folder containing known markers
    for entry in list(sys.path):
        try:
            p = Path(entry)
        except Exception:
            continue
        try:
            if p.is_dir() and ((p / "controller.py").exists() or (p / "model.py").exists()):
                return p
        except Exception:
            continue

    # 3) Environment variable override
    env_root = os.environ.get("AUTO_FACERIGAI_ROOT")
    if env_root:
        p = Path(env_root)
        if p.exists():
            return p

    # 4) Fallback to current working directory
    return Path.cwd()


PROJECT_ROOT = _detect_project_root()

# Ensure project root is importable
project_root_str = str(PROJECT_ROOT)
# Insert at front to prefer project over site-packages
if project_root_str not in sys.path:
    sys.path.insert(0, project_root_str)

importlib.invalidate_caches()


def _iter_local_package_dirs(root: Path):
    """Yield top-level subdirectories in the project that look like local
    Python packages (contain at least one .py). No keyword filtering.
    """
    exclude = {".git", "__pycache__", ".venv", "venv", "env", "build", "dist"}
    for d in root.iterdir():
        if not d.is_dir():
            continue
        if d.name in exclude or d.name.startswith("."):
            continue
        # Must contain at least one .py to be relevant
        try:
            has_py = any(p.is_file() and p.suffix == ".py" for p in d.iterdir())
        except Exception:
            has_py = False
        if has_py:
            yield d


def _setup_local_package(pkg_dir: Path):
    """Make an extra local package usable both as a package import
    (e.g. Package.camera_creator) and via bare imports inside it
    (e.g. from position_calculator import ...).
    """
    # Insert the package directory into sys.path so bare imports inside it can resolve
    pkg_dir_str = str(pkg_dir)
    if pkg_dir_str not in sys.path:
        sys.path.insert(0, pkg_dir_str)

    # Compute the package import path relative to project root
    try:
        rel = pkg_dir.relative_to(PROJECT_ROOT)
        pkg_name = ".".join(rel.parts)
    except Exception:
        # Fallback: use directory name as package name
        pkg_name = pkg_dir.name

    importlib.invalidate_caches()

    # Collect module basenames in the package directory
    basenames = [p.stem for p in pkg_dir.glob("*.py") if p.is_file() and p.stem != "__init__"]

    # Try to import fully-qualified modules first
    for base in basenames:
        fqmn = f"{pkg_name}.{base}"
        try:
            if fqmn in sys.modules:
                importlib.reload(sys.modules[fqmn])
            else:
                importlib.import_module(fqmn)
        except Exception:
            # Import may still succeed via bare-name during another module's import
            pass

    # Mirror module objects between bare name and fully-qualified name
    for base in basenames:
        fqmn = f"{pkg_name}.{base}"
        bare = base
        if fqmn in sys.modules and bare not in sys.modules:
            sys.modules[bare] = sys.modules[fqmn]
        elif bare in sys.modules and fqmn not in sys.modules:
            sys.modules[fqmn] = sys.modules[bare]


# Auto-detect and set up any extra packages in the project
for extra_dir in _iter_local_package_dirs(PROJECT_ROOT):
    _setup_local_package(extra_dir)


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
    except Exception:
        # Keep going even if some optional modules fail to import
        pass

from controller import UI
ui = UI()
print("done")
