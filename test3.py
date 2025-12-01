import maya.cmds as cmds
import maya.api.OpenMaya as om

# -----------------------------------------------------------
# Scene Setup (Uncomment and run these lines if objects don't exist)
# -----------------------------------------------------------
# cube = cmds.polyCube(width=1, height=1, depth=1, name="test_cube")[0]
# camera = cmds.camera(name="test_camera1")[0]
# cmds.xform("test_camera1", ws=True, t=(0, 0, 5)) 

# -----------------------------------------------------------
# Define object names
# -----------------------------------------------------------
camera_name = "ai_tracker_camera1"
# Ensure you are using the Shape node name for MFnMesh
mesh_name = "head_lod0_mesh" 

# -----------------------------------------------------------
# 1. Extract Camera Information (Origin and Direction)
# -----------------------------------------------------------

# Get the camera's DAG path
cam_dag = om.MSelectionList().add(camera_name).getDagPath(0)
# Get the camera's world space inclusive matrix
cam_mtx = cam_dag.inclusiveMatrix()

# Create a Transformation Matrix object
cam_tm = om.MTransformationMatrix(cam_mtx)

# Camera Position (Ray Start Point/Origin)
cam_pos = cam_tm.translation(om.MSpace.kWorld) 

# Camera Direction Vector (Ray Direction) - CRITICAL FIX
# In Maya, cameras typically look down their local -Z axis.
# The MMatrix stores the local X, Y, Z axes in its columns (indices 0-2, 4-6, 8-10).
# The Z-axis vector is at indices [8], [9], [10].
cam_z_vec = om.MVector(cam_mtx[8], cam_mtx[9], cam_mtx[10])

# The Forward Vector is the negative of the Z-axis vector
cam_vec = -cam_z_vec

# -----------------------------------------------------------
# 2. Extract Mesh Information
# -----------------------------------------------------------

# Get the mesh shape's DAG path
mesh_dag = om.MSelectionList().add(mesh_name).getDagPath(0)
# Initialize the MFnMesh function set
fn_mesh = om.MFnMesh(mesh_dag)

# -----------------------------------------------------------
# 3. Perform Intersection Test
# -----------------------------------------------------------

# The function requires MFloatPoint and MFloatVector
hit = fn_mesh.closestIntersection(
    om.MFloatPoint(cam_pos),       # Ray Origin (Camera position)
    om.MFloatVector(cam_vec),      # Ray Direction (Camera forward vector)
    om.MSpace.kWorld,              # Perform the check in World Space
    9999,                          # Ray length (max distance)
    False                          # Find the closest single hit
)

# Print the result. It will contain the hit point, face index, etc., upon success.
print(hit)