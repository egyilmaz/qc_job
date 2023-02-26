from backend.job import JobState
from backend.runtime_selector import RuntimeSelector, RuntimeType
from backend.backend_service import BackendService, ServiceResponseType
from backend.job_factory import JobFactory, OperationType

def main():
    job = JobFactory.Create(OperationType.ROTATION,'X(90),Y(90), X(180)')
    runtime = RuntimeSelector.select(RuntimeType.VERBATIM)
    service = BackendService(runtime)
    service.start_qc_thread()

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


if __name__ == '__main__':
    main()