from ..job_result import JobResult, JobResultType
from ..job import Job
from .runtime import Runtime

class RuntimeVerbatim(Runtime):
    def __init__(self) -> None:
        pass

    def execute(self, job:Job):
        operations = job.operations
        print(f'executing job id:{job.ident} ops:{len(operations)}')    
        for op in operations:
            try:
                op.run()
            except Exception as ex:  #TODO: replace the exception with our own
                #TODO: we need a logger for internal logs
                return JobResult(JobResultType.OP_FAILED, data={"job_id":job.ident},  msg=f"Exception happened during operation of {op}")
        # if we havent thrown yet, it must be success
        return JobResult(JobResultType.SUCCESS, data={"job_id":job.ident})
    