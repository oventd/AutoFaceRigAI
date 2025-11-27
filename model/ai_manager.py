import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om


class RaycastManager:
    def __init__(self, camera_dag, targets_dag):
        # Store camera and target mesh dag paths
        self._camera_dag = camera_dag
        self._targets_dag = targets_dag
    
    @staticmethod
    def raycast_to_mesh(dag_path, ray_origin, ray_direction, max_distance=1000.0):
        """
        Perform a raycast against a single mesh.

        Args:
            dag_path (MDagPath): Mesh shape dag path.
            ray_origin (tuple): Ray start point in world space.
            ray_direction (tuple): Ray direction in world space (prefer normalized).
            max_distance (float): Maximum ray length.

        Returns:
            dict or None: Hit information if the ray intersects the mesh, otherwise None.
        """
        mesh_fn = om.MFnMesh(dag_path)

        # Build ray origin and direction
        ray_source = om.MFloatPoint(*ray_origin)
        ray_dir = om.MFloatVector(*ray_direction)

        # Generate acceleration structure for intersection tests
        accel_params = mesh_fn.autoUniformGridParams()

        try:
            # closestIntersection returns several values in API 2.0
            hit_point, hit_ray_param, hit_face, hit_triangle, hit_bary1, hit_bary2 = mesh_fn.closestIntersection(
                ray_source,         # Ray start position
                ray_dir,            # Ray direction vector
                None,               # Limit to specific face IDs (optional)
                None,               # Limit to specific triangle IDs (optional)
                False,              # Are IDs sorted?
                om.MSpace.kWorld,   # Intersection test in world space
                max_distance,       # Maximum parametric distance
                False,              # Test both directions along the ray?
                accel_params,       # Acceleration parameters
                False,              # Sort all hits?
                False               # Sort hits descending?
            )
        except RuntimeError:
            # No intersection found
            return None
        
        # Convert result into a clean dictionary
        return {
            "hitPoint": (hit_point.x, hit_point.y, hit_point.z),   # World-space intersection position
            "distance": hit_ray_param,                             # Ray distance from origin
            "faceIndex": hit_face,                                 # Hit polygon face index
            "triangleIndex": hit_triangle,                         # Triangle index within the face
            "barycentric": (hit_bary1, hit_bary2),                 # Barycentric coordinates on the triangle
            "dagPath": dag_path,                                   # Mesh that was hit
        }

    @staticmethod
    def raycast_to_meshes(mesh_dags, ray_origin, ray_direction, max_distance=1000.0):
        """
        Perform a raycast against multiple meshes and return the closest hit.

        Args:
            mesh_dags (list[MDagPath]): A list of mesh dag paths.
            ray_origin (tuple): Ray start point in world space.
            ray_direction (tuple): Ray direction in world space.
            max_distance (float): Max ray length.

        Returns:
            dict or None: Closest hit result, or None if no intersections occurred.
        """
        closest_hit = None
        closest_distance = max_distance

        for dag in mesh_dags:
            hit = RaycastManager.raycast_to_mesh(dag, ray_origin, ray_direction, max_distance)
            if not hit:
                continue

            if hit["distance"] < closest_distance:
                closest_distance = hit["distance"]
                closest_hit = hit
        
        return closest_hit

    def 