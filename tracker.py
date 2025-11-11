import maya.cmds as cmds

from head import Head
from tracker_camera import TrackerCameraCreator
from samplerate import SampleRate

class Tracker:
    def __init__(self):
        self._head = Head()
        self._camera_creator = TrackerCameraCreator()
        self._camera_limit = {"x": (-20, 20), "y": (-60, 60)}
        self._sample_rate = SampleRate()
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
        return self._camera_creator

    @property
    def sample_rate(self):
        return (self._sample_rate.x, self._sample_rate.y)

    @sample_rate.setter
    def sample_rate(self, value=10, x=None, y=None):
        self._sample_rate.x = value if x is None else x
        self._sample_rate.y = value if y is None else y
        
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
        self._camera_creator.create(
            target=self.head.bbox,
            group_position=self.head.transition)
        self.head.hide_bbox()

        self._parent(self._camera_creator.group)

    def _parent(self, child):
        cmds.parent(child, self.group)
        cmds.select(clear=True)
    

