import maya.cmds as cmds

from head import Head
from tracker_camera_creator import TrackerCameraCreator
from viewport_manager import ViewportManager
from TurntableGenerator.anim_playblast_generator import AnimPlayblastGenerator
from pathlib import Path
from pixel_raycaster import PixelRaycaster

class Tracker:
    def __init__(self):
        self._head = Head()
        self._camera = None
        self._group = "grp_tracker"
        self._loc_group = "grp_landmark_locators"

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
        self._loc_group = cmds.group(name=self._loc_group, em=True)

        cmds.select(clear=True)

    def delete_group(self):
        if cmds.objExists(self.group):
            cmds.delete(self.group)
        if cmds.objExists(self._loc_group):
            cmds.delete(self._loc_group)
   
    def create_head_bbox(self):
        self.head.create_bbox()
        self._parent(self.head.bbox_group)
        self.head.hide_bbox()

    def create_camera(self):
        self._camera = TrackerCameraCreator(
            target=self.head.bbox,
            group_position=self.head.transition
        )
        self._camera.create()
        

        self._parent(self._camera.group)

    def _parent(self, child):
        cmds.parent(child, self.group)
        cmds.select(clear=True)
    
    def clean_up_viewport(self):
        self.viewport_manager = ViewportManager()
        self.viewport_manager.clean_up_viewport()
    
    def playblast(self):
        camera_creator = TrackerCameraCreator(
            target=self.head.bbox,
            group_position=self.head.transition
        )
        self.playblast_generator = AnimPlayblastGenerator(camera_creator)
        
        image_path = str(Path(__file__).resolve().parent.parent / "image" / "playblast" / "playblast")
        
        self.playblast_generator.format = "image"
        self.playblast_generator.path = image_path

        self.playblast_generator.run()

    def ai(self):
        index = int(cmds.currentTime(query=True))
        landmark_path = Path(__file__).resolve().parent.parent / "image" / "landmarks" / f"landmarks.{str(index).zfill(4)}.json"

        data = load_json(str(landmark_path))
        for index, point in enumerate(data[0]):
            pixel = (point[0], point[1])
            locator = PixelRaycaster(pixel, self._camera.camera, ["head_lod0_mesh"], f"{landmark_path.stem}_{index}").run()
            if locator:
                cmds.parent(locator, self._loc_group)

def load_json(path):
    import json
    with open(path, "r") as f:
        return json.load(f)