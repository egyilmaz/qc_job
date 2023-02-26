import uuid
from enum import Enum

class JobState(Enum):
    CREATED = 1
    WAITING = 2
    SUBMITTED = 3
    COMPLETED = 4
    FAILED = 5

"""
    Job class provides a unique uuid for each job, which is a set of operations.
"""

class Job:
    def __init__(self, operations) -> None:
        self._ident = uuid.uuid4()
        self._operations = operations
        self._state = JobState.CREATED

    @property
    def operations(self):
        return self._operations
    
    @property
    def ident(self):
        return self._ident
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        self._state = value
