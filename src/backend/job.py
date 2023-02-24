from .exceptions import EmptyJob, InvalidDelimeter
from .rotations import Rotations
from parse import parse

class Job:
    def __init__(self, job_str) -> None:
        if not job_str:
            raise EmptyJob('EmptyJob not allowed')
        self._rotations = self._createJob(job_str)
    
    def _createJob(self, job_str):
        if ',' in job_str:
            tokens = job_str.split(',')
        else:
            raise InvalidDelimeter('Missing comma as delimeter in job string')
            
        #TODO: replace this logic with regex
        rotations=[]
        for token in tokens:
            token = token.strip()
            x_or_y = token[0]
            rotation = parse('({:d})', token[1:])[0]
            rotations.append(Rotations(x_or_y, rotation))
        return rotations
    
    def rotations(self):
        return self._rotations