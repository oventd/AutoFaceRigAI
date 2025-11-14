import maya.cmds as cmds

from head import Head
from tracker_camera_creator import TrackerCameraCreator
from viewport_manager import ViewportManager

class Tracker:
    def __init__(self):
        self._head = Head()
        self._camera = None
        self._group = "grp_tracker"

        self._create_group()

    @property
    def head(self):
        return self._head

    @property
    def group(self):
        return self._group

    @property
    def camera_creator(self):
        return self._camera
        
    def _create_group(self):
        self.delete_group()
        self._group = cmds.group(name=self._group, em=True)
        cmds.select(clear=True)

    def delete_group(self):
        if cmds.objExists(self.group):
            cmds.delete(self.group)
   
    def create_head_bbox(self):
        self.head.create_bbox()
        self._parent(self.head.bbox_group)

    def create_camera(self):
        self._camera = TrackerCameraCreator(
            target=self.head.bbox,
            group_position=self.head.transition
        )
        self._camera.create()
        self.head.hide_bbox()

        self._parent(self._camera.group)

    def _parent(self, child):
        cmds.parent(child, self.group)
        cmds.select(clear=True)
    
    def clean_up_viewport(self):
        self.viewport_manager = ViewportManager()
        self.viewport_manager.clean_up_viewport()
