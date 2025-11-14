import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMayaUI as omui
import maya.api.OpenMaya as om


class ViewportManager:
    def __init__(self):
        self.panel = self._get_viewport()
    

    def _get_viewport(self):
        view = omui.M3dView.active3dView()
        cam_dag = view.getCamera()

        cam_transform_obj = cam_dag.transform()  
        cam_transform_dag = om.MDagPath.getAPathTo(cam_transform_obj)
        for panel in cmds.getPanel(type="modelPanel"):
            if cmds.modelEditor(panel, q=True, camera=True) == cam_transform_dag.fullPathName():
                return panel

    def clean_up_viewport(self):
        cmds.modelEditor(self.panel, e=True, allObjects=False)
        
        cmds.modelEditor(self.panel, e=True, polymeshes=True)
        cmds.modelEditor(self.panel, e=True, cameras=True)
        
        cmds.modelEditor(self.panel, e=True, displayAppearance="smoothShaded")
        cmds.modelEditor(self.panel, e=True, displayTextures=True)
        cmds.modelEditor(self.panel, e=True, displayLights="all")
        cmds.modelEditor(self.panel, e=True, useDefaultMaterial=False)
        cmds.modelEditor(self.panel, e=True, wireframeOnShaded=False)
        # cmds.modelEditor(self.panel, e=True, shadows=True)