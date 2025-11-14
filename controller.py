import sys
from pathlib import Path
import maya.cmds as cmds

from PySide2.QtUiTools import QUiLoader

from model.tracker import Tracker

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
        
        self.tracker = None
        
        self.window.set_head_button.clicked.connect(self.set_head)
        self.window.create_head_bb_button.clicked.connect(self.create_head_bb)
        self.window.create_camera_button.clicked.connect(self.create_camera)
        self.window.clean_up_viewport_button.clicked.connect(self.clean_up_viewport)
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()
    
    def set_head(self):
        self.tracker = Tracker()
        self.window.head_name.setText(self.tracker.head.name)
        self.window.head_x.setText(f"{self.tracker.head.x:.3f}")
        self.window.head_y.setText(f"{self.tracker.head.y:.3f}")
        self.window.head_z.setText(f"{self.tracker.head.z:.3f}")

    def create_head_bb(self):
        self.tracker.create_head_bbox()

    def create_camera(self):
        self.tracker.create_camera()
    
    def clean_up_viewport(self):
        self.tracker.clean_up_viewport()

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
