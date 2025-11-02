import sys
from pathlib import Path

import maya.cmds as cmds

from PySide2 import QtWidgets
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

class UiApp:
    def __init__(self):
        self.ui_path = str(Path(__file__).with_name("view.ui"))
        self.window = QUiLoader().load(self.ui_path, None)

    #     self.window.set_head_button.clicked.connect(self.set_head)
    
    # def set_head(self):
    #     sel = cmds.ls(selection=True)[0]
    #     tx, ty, tz = cmds.xform(sel, q=True, t=True)
    #     self.window.head_x.setText(str(tx))
    #     self.window.head_y.setText(str(ty))
    #     self.window.head_z.setText(str(tz))

    def run(self) -> int:
        self.window.show()
        return 
