from .operations.rotation import Rotation
from .job import Job

"""
    JobFactory uses 'ident' to delegate the job creation to relevant class by passing on the 'job_str'
"""
class JobFactory:
    def __init__(self) -> None:
        pass

    def create(op_ident, job_str):
        #TODO: make op_ident an enum, not text based.
        if op_ident == "rotation":
            operations = Rotation.Create(job_str)
            if len(operations):
                return Job(operations)
            else:
                return ValueError(f"Job creation failed for type {op_ident}")
        else:
            return ValueError(f"Unknown operation ident:{op_ident}, cannot create job.")
