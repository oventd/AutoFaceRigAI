import sys
from pathlib import Path
from model import AITracker
import maya.cmds as cmds

from PySide2.QtUiTools import QUiLoader

class UI:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UI, cls).__new__(cls)
        else:
            try:
                cls._instance.window.close()
            except Exception:
                pass
        return cls._instance

    def __init__(self):
        if UI._initialized:
            return
        UI._initialized = True
        
        self.ui_path = str(Path(__file__).with_name("view.ui"))
        self.window = QUiLoader().load(self.ui_path)
        self.tracker = AITracker()

        self.window.set_head_button.clicked.connect(self.set_head)
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()
    
    def set_head(self):
        self.tracker.head.init()
        self.window.head_name.setText(self.tracker.head.name)
        self.window.head_x.setText(f"{self.tracker.head.x:.3f}")
        self.window.head_y.setText(f"{self.tracker.head.y:.3f}")
        self.window.head_z.setText(f"{self.tracker.head.z:.3f}")
        
    def test(self):
        print("test")

    @classmethod
    def run(cls):
        global ui
        if ui:
            ui.close()
        ui = cls()
        ui.window.show()
        ui.window.raise_()
        ui.window.activateWindow()
        return cls._instance
