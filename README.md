# Track QC Job
A web service for submitting jobs to a quantum computer

## General Design
Please refer to the `design` folder for my initial understanding of how the components will look like. I havent implemented most of it, as it would deviate from the description of the task

### Submitting a Job
* A POST request containing the payload (JobStr + runtime)
* payload is verified upon receipt, then compiled
* any error is returned as response
* successful compilation will register the content into DB for backend to fetch at a convenient time. 
    * Return a job descriptor to the user if submission is successful

### Requesting the state of a Job
* A GET request with job descriptor
* check the DB and fetch the status, return it as the response.

### Fetching a Job and submitting to Quantum Computer
* Get the highest ranked job in the DB and submit it to QC
* When QC is done, at a later time, listen to QC and store result/update in DB with the job descriptor

## Installation
We are relying on virtualenv to keep things tidy and isolated from system installed python versions.
```
sudo apt install virtualenv python3 python3-pip
``` 
Once necessary system-wide dependencies are in place, clone the code and setup the virtualenv. Once virtualenv is ready, install the app related dependencies.
```
git clone https://github.com/egyilmaz/qc_job.git
cd qc_job
virtualenv -p python3 ./venv
source venv/bin/activate
pip install -r requirements.txt
```
### Running the tests:
Type `pytest` at the root level of the project
```
cd qc_job
pytest
```

## BDD Tests
I will try using `behave` to implement BDD tests if time permits.

## Example usage of backend service
The `submit()` and `query()` are the two interfaces to interact with the Quantum computer. The `BackendService` starts a thread which simulates the Quantum Computer. The backend service keeps a list of jobs and updates their state. In a production setting, a DB will replace the job list kept in `BackendService`
```
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
```


## Thoughts on "What else we need for a minimal viable product and beyond"
Following should be included for a production system but its not in the scope of this test.

1. User authentication, authorization
2. Encryption of payload via pre-shared (out-of-band) secret
3. Get the services running in K8s, with a load_balancer + ingres at the front
4. Rank the submitted jobs using requesting customer's privileges
5. Logging implementation for internal troubleshooting
6. Mocking in unit tests, for better code-coverage
7. BDD tests for end-to-end functionality check.
