import sys
from pathlib import Path

from PySide2 import QtWidgets
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

class UiApp:
    def __init__(self):
        # Load the .ui file that sits next to this module
        ui_path = str(Path(__file__).with_name("ai_ui.ui"))

        self.ui_path = ui_path
        self.app = QtWidgets.QApplication(sys.argv)
        loader = QUiLoader()
        file = QFile(self.ui_path)
        file.open(QFile.ReadOnly)
        try:
            self.window = loader.load(file, None)
        finally:
            file.close()

    def run(self) -> int:
        self.window.show()
        # PySide2 uses exec_ for compatibility
        return self.app.exec_()
