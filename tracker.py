from head import Head
from tracker_camera import TrackerCameraCreator
from samplerate import SampleRate


class Tracker:
    def __init__(self):
        self._head = Head()
        self._camera_creator = TrackerCameraCreator()
        self._camera_limit = {"x": (-20, 20), "y": (-60, 60)}
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
        self._camera_creator.create(
            target=self.head.bbox,
            group_position=self.head.transition)

    

