import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om

from TurntableGenerator.camera_creator import TurnTableCameraCreator


class Head(object):
    def __init__(self):
        self._head_dag = None
        self._transition = None

    def init(self):
        sel = cmds.ls(selection=True)[0]
        if not sel:
            cmds.warning("Nothing selected.")
            return
        if not cmds.objExists(sel):
            return
        
        msel = om.MSelectionList()
        msel.add(sel)
        self._head_dag = msel.getDagPath(0)
        self._transition = cmds.xform(sel, q=True, ws=True, t=True)

        ppn = self._head_dag.partialPathName()
        self._namespace = f"{ppn.split(':')[0]}:" if ":" in ppn else ""

        

        
    @property
    def name(self):
        return self._head_dag.partialPathName()
    @property
    def x(self):
        return self._transition[0]
    @property
    def y(self):
        return self._transition[1]
    @property
    def z(self):
        return self._transition[2]
    @property
    def transition(self):
        return self._transition
    
    def create_bbox(self):
        bbox_points = (
            cmds.xform(f"{self._namespace}FACIAL_L_HairC2", q=True, ws=True, t=True)[0],
            cmds.xform(f"{self._namespace}FACIAL_R_HairC2", q=True, ws=True, t=True)[0],
            cmds.xform(f"{self._namespace}FACIAL_C_Hair5", q=True, ws=True, t=True)[1],
            cmds.xform(f"{self._namespace}FACIAL_C_Jawline", q=True, ws=True, t=True)[1],
            cmds.xform(f"{self._namespace}FACIAL_C_12IPV_NoseTip2", q=True, ws=True, t=True)[2],
            cmds.xform(f"{self._namespace}FACIAL_C_12IPV_NeckBackA1", q=True, ws=True, t=True)[2],
        )
        left, right, up, down, front, back = bbox_points

        # 1) Normalize min/max per axis
        x_min, x_max = sorted([left, right])
        y_min, y_max = sorted([down, up])
        z_min, z_max = sorted([back, front])

        # 2) Compute size (width, height, depth)
        width  = float(x_max - x_min)
        height = float(y_max - y_min)
        depth  = float(z_max - z_min)

        # Safety: avoid zero-size creation (optional)
        eps = 1e-6
        if width < eps or height < eps or depth < eps:
            raise ValueError("One or more dimensions are ~zero. Check your plane values.")

        # 3) Compute center
        cx = 0
        cy = (y_min + y_max) * 0.5
        cz = (z_min + z_max) * 0.5

        # 4) Create and place cube
        self._bbox, shape = cmds.polyCube(w=width, h=height, d=depth, name="geo_headBbox")
        cmds.xform(self._bbox, ws=True, t=(cx, cy, cz), ro=(0, 0, 0))
        cmds.hide(self._bbox)

        # Freeze transforms (optional, keeps size baked into shape)
        cmds.makeIdentity(self._bbox, apply=True, t=True, r=True, s=True, n=False)

        self.grp_bbox = cmds.group(name="grp_headBbox", em=True)
        cmds.parent(self._bbox, self.grp_bbox)

class TrackerCameraCreator(TurnTableCameraCreator):
    def __init__(self, camera_name="AITracker_camera"):
        super().__init__(camera_name=camera_name)

    def create_group(self):
        # make camera group
        cmds.select(clear=True)
        grp_camera = cmds.group(name="grp_AITracker_camera", em=True)
        cmds.xform(grp_camera, t=self.head.transition)
        cmds.parent(self._camera, grp_camera)

class SampleRate:
    def __init__(self, value=10, x=None, y=None):
        self._x = value if x is None else x
        self._y = value if y is None else y
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        if not isinstance(value, int):
            Warning("Sample rate must be an integer.")
            return
        self._x = value
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        if not isinstance(value, int):
            Warning("Sample rate must be an integer.")
            return
        self._y = value
        
    
class AITracker:
    def __init__(self):
        self._head = Head()
        self._camera_creator = TrackerCameraCreator()
        self._camera_limit = {"x":(-20, 20), "y":(-60, 60)}
        self._sample_rate = SampleRate()
    
    @property
    def head(self):
        return self._head
    
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
    
    def create_camera(self):
        self._camera_creator.create()