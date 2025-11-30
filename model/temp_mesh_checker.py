import maya.api.OpenMaya as om
import maya.cmds as cmds
from pathlib import Path
import math

# from camera_fuctions import position_to_camera_angle
class MeshChecker:
    def __init__(self, json_path, camera_name="camera1"):
        self._json_path = Path(json_path)
        self._data = self.read_json(self._json_path)[0]

        self.camera = self.create_camera()

        position = (self._data[0][0], self._data[0][1])
        point_angle = self.position_to_camera_angle(position, self.camera)

        point_angle_x, point_angle_y = point_angle
        x = (point_angle_x)

        print(f"Camera Angle: {point_angle}")

    @staticmethod
    def read_json(json_path):
        import json

        with open(json_path, 'r') as f:
            data = json.load(f)
        
        return data
    @staticmethod
    def get_fov(cam_shape):
        h_fov = cmds.camera(cam_shape, q=True, hfv=True)
        v_fov = cmds.camera(cam_shape, q=True, vfv=True)
        return h_fov, v_fov
    
    def position_to_camera_angle(self, position, camera, resolution=(1280, 720)):
        h_fov, v_fov = self.get_fov(camera)

        position_x, position_y = position
        resolution_x, resolution_y = resolution

        center_x = resolution_x / 2
        center_y = resolution_y / 2

        distance_from_center_x = position_x - center_x
        distance_from_center_y = position_y - center_y

        ratio_x = distance_from_center_x / resolution_x
        ratio_y = distance_from_center_y / resolution_y

        angle_x = h_fov * ratio_x
        angle_y = v_fov * ratio_y
        return angle_x, angle_y

    def create_camera(self):
        trans, camera = cmds.camera(name="checker_camera1")
        cmds.xform(trans, ws=True, t=(0, 0, 10))
        return camera

    def delete_camera(self):
        cmds.delete(self.camera)

    def point_to_world_ray(self, landmark, assume_pixel=True):
        position = (landmark[0], landmark[1])
        depth = landmark[2]

        """Return (origin_world: MPoint, direction_world: MVector) ray."""
        angle_x_deg, angle_y_deg = self.position_to_camera_angle(
            position, assume_pixel=assume_pixel
        )

        # Convert degrees to radians
        ax = math.radians(angle_x_deg)
        ay = math.radians(angle_y_deg)

        # Camera local space: camera looks along -Z in Maya by default
        dir_cam = om.MVector(
            math.tan(ax),      # left/right
            -math.tan(ay),     # up/down (flip Y)
            -1               # forward
        ).normalize()

        # Get camera world matrix
        sel = om.MSelectionList()
        sel.add(self.camera_transform)
        cam_dag = sel.getDagPath(0)
        cam_mtx = cam_dag.inclusiveMatrix()  # MDagPath -> world matrix

        # Transform origin and direction to world
        origin_world = om.MPoint(0, 0, 0) * cam_mtx
        direction_world = dir_cam * cam_mtx  # for vectors, rotation only

        # Make sure direction is normalized
        direction_world = om.MVector(direction_world).normal()

        return origin_world, direction_world