import maya.api.OpenMaya as om
import maya.cmds as cmds

def get_fov(cam_shape):
    h_fov = cmds.camera(cam_shape, q=True, hfv=True)
    v_fov = cmds.camera(cam_shape, q=True, vfv=True)
    return h_fov, v_fov

def position_to_camera_angle(position, camera, resolution=(1280, 720)):
    h_fov, v_fov = get_fov(camera)

    position_x, position_y = position
    resolution_x, resolution_y = resolution

    return h_fov * (position_x / resolution_x), v_fov * (position_y / resolution_y)

