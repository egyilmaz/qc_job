import pytest
from src.backend.exceptions import EmptyJob, InvalidAxis, InvalidDelimeter, InvalidToken
from src.backend.job_factory import JobFactory, OperationType
from src.backend.runtime_selector import RuntimeSelector, RuntimeType
from src.backend.job_result import JobResult, JobResultType
from src.backend.job import JobState
from src.backend.backend_service import BackendService, ServiceResponseType

def test_job_ctor_success():
    job = JobFactory.Create(OperationType.ROTATION, 'X(90), Y(180), X(90)')
    rotations = job.operations
    # Successful job creation should have defined number of operations and a job ident
    assert job.ident != None
    assert len(rotations) == 3        
    assert rotations[0].axis == 'X'
    assert rotations[0].angle == 90 
    assert rotations[1].axis == 'Y'
    assert rotations[1].angle == 180 
    assert rotations[2].axis == 'X'
    assert rotations[2].angle == 90 

def test_job_ctor_failures():
    #TODO: There might be more errornous string cases, parsing should be checked further
    test_inputs = [('', EmptyJob), 
                   (None, EmptyJob), 
                   ('Z(90), X(90)', InvalidAxis),
                   ('X(90) Y(90)', InvalidDelimeter),
                   ('X(90).Y(90)', InvalidDelimeter),
                   ('X(90) Y(90), X(180)', InvalidToken),
                   ('X(90).Y(90),X(180)', InvalidToken)]

    for job_str, expected_exception in test_inputs:
        with pytest.raises(expected_exception):
            JobFactory.Create(OperationType.ROTATION, job_str)

def test_runtime_selector():
    job = JobFactory.Create(OperationType.ROTATION,'X(90),Y(90), X(180)')
    runtime = RuntimeSelector.select(RuntimeType.VERBATIM)
    result = runtime.execute(job)
    assert isinstance(result, JobResult)
    assert result.result_type == JobResultType.SUCCESS

def test_backend_service_query_failed():
    runtime = RuntimeSelector.select(RuntimeType.ECHO)
    service = BackendService(runtime)
    resp = service.query("no such job exists")
    assert resp.status == ServiceResponseType.JOB_NOT_FOUND

def test_backend_service_success():

    job = JobFactory.Create(OperationType.ROTATION,'X(90),Y(90), X(180)')
    runtime = RuntimeSelector.select(RuntimeType.VERBATIM)
    service = BackendService(runtime)
    service.start_qc_thread() # start the Quantum Computer thread

    resp = service.submit(job)
    assert resp.status == ServiceResponseType.SUBMIT_SUCCESS
    job_id = resp.data['job_ident']

    resp = service.query(job_id)
    assert resp.status == ServiceResponseType.QUERY_SUCCESS
    assert resp.data['job'].state == JobState.WAITING

    service.run()

    resp = service.query(job_id)
    assert resp.status == ServiceResponseType.QUERY_SUCCESS
    assert resp.data['job'].state == JobState.COMPLETED
       

#TODO: Create multithreaded query, submit tests, to ensure correct concurrent operation

