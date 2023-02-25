class RuntimeEcho:
    def __init__(self) -> None:
        pass

    def execute(self, job):
        operations = job.operations
        print(f'executing job id:{job.ident} ops:{len(operations)}')    
        for op in operations:
            op.run()
    