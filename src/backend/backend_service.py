from enum import Enum
from .job import Job
from .service_response import ServiceResponse
from .runtimes.runtime import Runtime

class ServiceResponseType(Enum):
    SUBMITTED = 1
    WAITING = 2
    COMPLETED = 3
    FAILED_ON_SUBMISSION = 4
    FAILED_DURING_EXECUTION = 5
    JOB_NOT_FOUND = 6

class BackendService:
    def __init__(self) -> None:
        self._jobs=[]

    def submit(self, job:Job, runtime:Runtime):
        status = ServiceResponse(ServiceResponseType.WAITING, {"job_ident":job.ident})
        self._jobs.append((job, status))
        return ServiceResponse(ServiceResponseType.SUBMITTED, {"job_ident":job.ident})

    def query(self, job_id):
        for job,status in self._jobs:
            if job.ident == job_id:
                return status
        return ServiceResponse(ServiceResponseType.JOB_NOT_FOUND)
    
    def run(self):
        self._jobs = [(job, ServiceResponse(ServiceResponseType.COMPLETED, {"pi":3.141519})) for (job,status) in self._jobs]
