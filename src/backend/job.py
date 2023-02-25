import uuid

"""
    Job class provides a unique uuid for each job, which is a set of operations.
"""

class Job:
    def __init__(self, operations) -> None:
        self._ident = uuid.uuid4()
        self._operations = operations

    @property
    def operations(self):
        return self._operations
    
    @property
    def ident(self):
        return self._ident