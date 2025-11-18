import maya.cmds as cmds

from TurntableGenerator.anim_camera_creator import AnimCameraCreator

class TrackerCameraCreator(AnimCameraCreator):
    def __init__(self, 
                 target,
                 padding=1.3,
                 limit_x=(-30, 30), 
                 limit_y=(-50, 50),
                 group_position=(0, 0, 0),
                 camera_name="ai_tracker_camera1",
                 group_name="grp_ai_tracker_camera1"):
        super().__init__(camera_name=camera_name, group_name=group_name)
        
        self._target = target
        self._padding = padding
        self._group_position = group_position

        if not self._validate_limit(limit_x):
            raise ValueError("X limit[0] must be less than limit[1]")
        if not self._validate_limit(limit_y):
            raise ValueError("Y limit[0] must be less than limit[1]")
        
        self._limit_x = limit_x
        self._limit_y = limit_y
        self._sample_rate = 10
        

    @property
    def limit_x(self):
        return self._limit_x
    
    @limit_x.setter
    def limit_x(self, limit_x):
        if not self._validate_limit(limit_x):
            raise ValueError("X limit[0] must be less than limit[1]")
        self._limit_x = limit_x

    @property
    def limit_y(self):
        return self._limit_y
    
    @limit_y.setter
    def limit_y(self, limit_y):
        if not self._validate_limit(limit_y):
            raise ValueError("Y limit[0] must be less than limit[1]")
        self._limit_y = limit_y

    @property
    def sample_rate(self):
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, sample_rate):
        if sample_rate < 1:
            raise ValueError("Sample rate must be at least 1")
        if sample_rate % 1 != 0:
            raise ValueError("Sample rate must be an integer")
        self._sample_rate = int(sample_rate)
    
    @property
    def frame_range(self):
        return (1, 1+len(self.calculate_angle(self._limit_x,
                                              self._limit_y,
                                              self._sample_rate)))
    
    def create_camera(self):
        current_visibility = cmds.getAttr(f"{self._target}.visibility")
        if current_visibility == 0:
            cmds.setAttr(f"{self._target}.visibility", 1)
        super().create_camera()
        self.autoframing(self.camera, self._target, self._padding)
        if current_visibility == 0:
            cmds.setAttr(f"{self._target}.visibility", 0)
    
    def _validate_limit(self, limit):
        if limit[0] > limit[1]:
            raise ValueError("limit[0] must be less than limit[1]")
        return True

    @staticmethod
    def calculate_angle(limit_x, limit_y, sample_rate):
        min_x, max_x = limit_x
        min_y, max_y = limit_y

        angle_x = (max_x - min_x) / sample_rate
        angle_y = (max_y - min_y) / sample_rate
        
        angles = []
        x = min_x
        y = min_y
        while x <= max_x:
            while y <= max_y:
                angles.append((x, y))
                y += angle_y
            x += angle_x
            y = min_y
        return angles
    
    def create_group(self):
        self._group = cmds.group(name=self._group, empty=True)
        cmds.xform(self._group, ws=True, t=self._group_position)
        cmds.parent(self._camera, self._group)

    def animate_group(self):
        angles = self.calculate_angle(self._limit_x, 
                                      self._limit_y, 
                                      self._sample_rate)

        for i, angle in enumerate(angles):
            frame = i + 1
            cmds.setKeyframe(self._group, attribute="rotateX", value=angle[0], time=frame)
            cmds.setKeyframe(self._group, attribute="rotateY", value=angle[1], time=frame)
