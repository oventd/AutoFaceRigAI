import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om

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
    def position(self):
        return self._transition

class AITracker:
    def __init__(self):
        self._head = Head()

    @property
    def head(self):
        return self._head
    