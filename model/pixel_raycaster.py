import maya.api.OpenMaya as om
import maya.cmds as cmds
from pathlib import Path
import math


class PixelRaycaster:
    """
    Converts a 2D pixel position into a camera ray, 
    performs intersection against meshes, 
    and returns the hit point in world space.
    """

    def __init__(self, pixel, camera_name="camera1", mesh_list=None, locator_name=None):
        self.camera_name = camera_name
        self.pixel = pixel
        self.mesh_list = mesh_list
        self.locator_name = locator_name or f"locator_ray_{pixel[0]}_{pixel[1]}"

    def run(self):
        # Perform raycast
        hit_point = self.raycast_pixel(self.pixel, mesh_list=self.mesh_list)
        if hit_point is None:
            return None
        locator_name = cmds.spaceLocator(name=self.locator_name, position=(hit_point.x, hit_point.y, hit_point.z))

        return locator_name

    # --------------------------------------------------
    # Camera FOV
    # --------------------------------------------------

    @staticmethod
    def _get_camera_fov(camera_shape, resolution=(1280, 720)):
        """
        플레이블라스트의 aspect ratio에 맞춘 수직 FOV 계산
        """
        res_x, res_y = resolution
        aspect = float(res_x) / float(res_y)

        h_fov = cmds.camera(camera_shape, q=True, hfv=True)

        # tan(v/2) = tan(h/2) * (res_y / res_x)
        half_h = math.tan(math.radians(h_fov * 0.5))
        half_v = half_h * (res_y / float(res_x))
        v_fov_effective = math.degrees(2.0 * math.atan(half_v))

        return h_fov, v_fov_effective

    # --------------------------------------------------
    # Pixel → Angle
    # --------------------------------------------------

    def _pixel_to_camera_direction(self, pixel, camera, resolution=(1280, 720)):
        """
        픽셀 → 카메라 로컬 방향 벡터.
        effective vFOV를 고려하여 resolution gate에 맞는 정확한 방향을 만든다.
        """

        # camera 가 transform이면 shape로 바꿔주는 게 안전
        shapes = cmds.listRelatives(camera, shapes=True, fullPath=True) or [camera]
        cam_shape = shapes[0]

        # 해상도 기준으로 보정된 FOV 계산 (중요!)
        h_fov, v_fov = self._get_camera_fov(cam_shape, resolution)

        px, py = pixel
        res_x, res_y = resolution

        # 화면 중심
        cx = res_x * 0.5
        cy = res_y * 0.5

        dx = px - cx
        dy = py - cy

        # 픽셀 위치를 -1~1의 비율로 정규화
        ratio_x = dx / res_x
        ratio_y = dy / res_y

        # 각도로 변환
        angle_x = math.radians(h_fov * ratio_x)
        angle_y = math.radians(-v_fov * ratio_y)   # 주의: y는 flip

        # 각도를 카메라 로컬 방향 벡터로 변환
        x = math.tan(angle_x)
        y = math.tan(angle_y)
        z = -1.0  # 카메라는 -Z 방향을 바라봄

        v = om.MVector(x, y, z)
        v.normalize()
        return v

    @staticmethod
    def _angle_to_local_direction(angle_x, angle_y):
        """Convert camera-relative angular offsets to a local-direction vector."""
        ax = math.radians(angle_x)
        ay = math.radians(angle_y)

        x = math.tan(ax)
        y = math.tan(ay)
        z = -1.0

        v = om.MVector(x, y, z)
        v.normalize()
        return v

    def _camera_ray_in_world(self, pixel):
        """이제 angle_x, angle_y 안 쓰고 pixel 기반으로 직접 local dir을 구해도 됨."""
        camera_sel = om.MSelectionList()
        camera_sel.add(self.camera_name)
        camera_dag = camera_sel.getDagPath(0)
        camera_matrix = camera_dag.inclusiveMatrix()

        tm = om.MTransformationMatrix(camera_matrix)
        origin = tm.translation(om.MSpace.kWorld)

        # angle_x, angle_y 대신 self.pixel 사용 (또는 인자로 pixel 넘기기)
        local_dir = self._pixel_to_camera_direction(pixel, self.camera_name)
        world_dir = local_dir * camera_matrix
        world_dir.normalize()

        return origin, world_dir

    def raycast_pixel(self, pixel, mesh_list=None):
        """Creates a world-space ray from pixel angulation and tests against meshes."""

        origin, direction = self._camera_ray_in_world(pixel)

        if mesh_list is None:
            mesh_list = cmds.ls(type="mesh", long=True) or []

        closest_hit = None
        max_dist = 9999
        closest_dist = max_dist

        for mesh_shape in mesh_list:
            try:
                dag = om.MSelectionList().add(mesh_shape).getDagPath(0)
            except RuntimeError:
                continue

            mesh_fn = om.MFnMesh(dag)

            try:
                hit = mesh_fn.closestIntersection(
                    om.MFloatPoint(origin),
                    om.MFloatVector(direction),
                    om.MSpace.kWorld,
                    max_dist,
                    False  # closest only
                )
            except RuntimeError:
                continue

            if hit:
                hit_pos, hitParam, faceId, triId, u, v = hit
                hit_point = om.MPoint(hit_pos)
                dist = om.MPoint(origin).distanceTo(hit_point)

                if dist < closest_dist:
                    closest_dist = dist
                    closest_hit = hit_point

        return closest_hit
