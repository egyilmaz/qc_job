import pytest
from src.backend.exceptions import EmptyJob, InvalidAxis, InvalidDelimeter, InvalidToken
from src.backend.job_factory import JobFactory, OperationType
from src.backend.runtime_selector import RuntimeSelector, RuntimeType
from src.backend.job_result import JobResult, JobResultType
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

def test_job_ctor_empty_str():
    with pytest.raises(EmptyJob) as e_info:
        job = JobFactory.Create(OperationType.ROTATION, '')

    with pytest.raises(EmptyJob) as e_info:
        job = JobFactory.Create(OperationType.ROTATION, None)

def test_job_ctor_invalid_axis():
    with pytest.raises(InvalidAxis) as e_info:
        job = JobFactory.Create(OperationType.ROTATION, 'Z(90), X(90)')

def test_job_ctor_invalid_delimeter():
    with pytest.raises(InvalidDelimeter) as e_info:
        job = JobFactory.Create(OperationType.ROTATION,'X(90) Y(90)')

def test_job_ctor_single_delimeter():
    with pytest.raises(InvalidToken) as e_info:
        job = JobFactory.Create(OperationType.ROTATION,'X(90) Y(90), X(180)')

#TODO: There might be more errornous string cases, parsing should be checked further

def test_runtime_selector():
    job = JobFactory.Create(OperationType.ROTATION,'X(90),Y(90), X(180)')
    runtime = RuntimeSelector.select(RuntimeType.VERBATIM)
    result = runtime.execute(job)
    assert isinstance(result, JobResult)
    assert result.result_type == JobResultType.SUCCESS

def test_backend_service_success():
    job = JobFactory.Create(OperationType.ROTATION,'X(90),Y(90), X(180)')
    runtime = RuntimeSelector.select(RuntimeType.ECHO)
    service = BackendService(runtime)

    resp = service.submit(job)
    assert resp.status == ServiceResponseType.SUBMITTED
    job_id = resp.data['job_ident']

    resp = service.query(job_id)
    assert resp.status == ServiceResponseType.WAITING

    service.run()

    resp = service.query(job_id)
    assert resp.status == ServiceResponseType.COMPLETED
    assert resp.data == {"pi":3.141519} 

def test_backend_service_query_failed():
    runtime = RuntimeSelector.select(RuntimeType.ECHO)
    service = BackendService(runtime)
    resp = service.query("no such job exists")
    assert resp.status == ServiceResponseType.JOB_NOT_FOUND
