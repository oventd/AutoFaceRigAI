from pathlib import Path

image_path = str(Path(__file__).resolve().parent / "image")

def clear_folder(folder_path):
    folder = Path(folder_path)
    for item in folder.iterdir():
        if item.is_file():
            item.unlink()

clear_folder(image_path)