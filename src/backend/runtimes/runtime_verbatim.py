from src.backend.job_result import JobResult, JobResultType

class RuntimeVerbatim:
    def __init__(self) -> None:
        pass

    def execute(self, job):
        operations = job.operations
        print(f'executing job id:{job.ident} ops:{len(operations)}')    
        for op in operations:
            try:
                op.run()
            except Exception as ex:  #TODO: replace the exception with our own
                #TODO: we need a logger for internal logs
                return JobResult(JobResultType.OP_FAILED, f"Exception happened during operation of {op}")
        # if we havent thrown yet, it must be success
        return JobResult(JobResultType.SUCCESS)
    