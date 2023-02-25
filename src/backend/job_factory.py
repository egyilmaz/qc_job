from .operations.rotation import Rotation
from .job import Job

from enum import Enum

class OperationType(Enum):
    ROTATION = 1

"""
    JobFactory uses 'ident' to delegate the job creation to relevant class by passing on the 'job_str'
"""
class JobFactory:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def Create(self, op_ident:OperationType, job_str:str):
        match op_ident:
            case OperationType.ROTATION:
                operations = Rotation.Create(job_str)
                if len(operations):
                    return Job(operations)
                else:
                    return ValueError(f"Job creation failed for type {op_ident}")
            case _:
                return ValueError(f"Unknown operation ident:{op_ident}, cannot create job.")
