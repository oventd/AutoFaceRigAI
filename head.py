import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om


class Head(object):
    def __init__(self):
        self._head_dag = None
        self._transition = None
        self._bbox = "geo_headBbox"
        self._bbox_group = "grp_headBbox"

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
    @property
    def bbox(self):
        return self._bbox
    @property
    def bbox_group(self):
        return self._bbox_group
    
    def delete_bbox(self):
        if cmds.objExists(self._bbox_group):
            try:
                cmds.delete(self._bbox_group)
            except Exception:
                pass
        if cmds.objExists(self._bbox):
            try:
                cmds.delete(self._bbox)
            except Exception:
                pass

    def create_bbox(self):
        #clean up any existing nodes with the same names
        self.delete_bbox()

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
        self._bbox, shape = cmds.polyCube(w=width, h=height, d=depth, name=self._bbox)
        cmds.xform(self._bbox, ws=True, t=(cx, cy, cz), ro=(0, 0, 0))

        # Freeze transforms (optional, keeps size baked into shape)
        cmds.makeIdentity(self._bbox, apply=True, t=True, r=True, s=True, n=False)

        self._bbox_group = cmds.group(name=self._bbox_group, em=True)
        cmds.parent(self._bbox, self._bbox_group)

    def hide_bbox(self):
        cmds.hide(self._bbox_group)