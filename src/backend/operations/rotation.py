from src.backend.exceptions import EmptyJob, InvalidDelimeter, InvalidAxis, InvalidToken
from parse import parse
from .operation import Operation

class Rotation(Operation):    
    def __init__(self, axis:str, angle:int) -> None:
        self._axis = axis
        self._angle = angle
        self._rotations = []

    @property
    def axis(self):
        return self._axis
    
    @property
    def angle(self):
        return self._angle

    @property
    def rotations(self):
        return self._rotations
    
    def run(self):
        print(f'running rotation axis:{self._axis}, angle{self._angle}')
    
    @classmethod
    def Create(self, job_str):
        if not job_str:
            raise EmptyJob('Empty job string not allowed')

        if ',' in job_str:
            tokens = job_str.split(',')
        else:
            raise InvalidDelimeter('Missing comma as delimeter in job string')
        
        #TODO: Make this parsing more bullet-proof and test border conditions.
        rotations=[]
        for token in tokens:
            try:
                res = parse('{:l}({:d})', token.strip())
                axis, rotation = res[0], res[1]
                if axis == 'X' or axis == 'Y':
                    rotations.append(Rotation(axis, rotation))
                else:
                    raise InvalidAxis(f'Unknown axis:{axis} extracted from {job_str}')
            except TypeError as ex:
                raise InvalidToken(f"Token extraction failed:{ex}")
        return rotations
    