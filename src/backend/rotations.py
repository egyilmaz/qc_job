class Rotations:
    def __init__(self, axis:str, angle:int) -> None:
        self._axis = axis
        self._angle = angle

    def axis(self):
        return self._axis
    
    def angle(self):
        return self._angle