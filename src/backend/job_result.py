from enum import Enum

class JobResultType(Enum):
    SUCCESS = 1
    OP_FAILED = 2


class JobResult:
    def __init__(self, result_type:JobResultType, msg:str=None) -> None:
        self._result_type = result_type
        self._msg = msg

    @property
    def result_type(self):
        return self._result_type
    
    @property
    def msg(self):
        return self._msg