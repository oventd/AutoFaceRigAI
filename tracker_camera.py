import maya.cmds as cmds

from TurntableGenerator.camera_creator import TurnTableCameraCreator


class TrackerCameraCreator(TurnTableCameraCreator):
    def __init__(self, camera_name="ai_tracker_camera1"):
        super().__init__(camera_name=camera_name, group_name=f"grp_{camera_name}")
        
    def create(self, target=None, start_frame=1, end_frame=119, padding=1.3, group_position=[0, 0, 0]):
        
        self._padding = padding        

        # Clean up any existing nodes with the same names
        self.delete()

        # Create camera
        self.create_camera(target=target)

        # Create group
        self.create_group( group_position )

    def create_group(self, group_position=[0, 0, 0]):
        # make camera group
        cmds.select(clear=True)
        self._group = cmds.group(name=self._group, em=True)
        cmds.xform(self._group, t=group_position)
        cmds.parent(self._camera, self._group)

