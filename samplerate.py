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

