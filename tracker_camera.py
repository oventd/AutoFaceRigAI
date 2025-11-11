import maya.cmds as cmds

from TurntableGenerator.camera_creator import TurnTableCameraCreator


class TrackerCameraCreator(TurnTableCameraCreator):
    def __init__(self, camera_name="AITracker_camera"):
        super().__init__(camera_name=camera_name)

    def create_group(self):
        # make camera group
        cmds.select(clear=True)
        grp_camera = cmds.group(name="grp_AITracker_camera", em=True)
        cmds.xform(grp_camera, t=self.head.transition)
        cmds.parent(self._camera, grp_camera)

