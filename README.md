# Track QC Job
A web service for submitting jobs to a quantum computer

## General Design
Following should be included for a production system but its not in the scope of this test.

1. User authentication, authorization
2. Encryption of payload via pre-shared (out-of-band) secret
3. Get the services running in K8s, with a load_balancer + ingres at the front

### Submitting a Job
* A POST request containing the payload
* payload is verified upon receipt, then compiled
* any error is returned as response
* successful compilation will register the content into DB for backend to fetch at a convenient time. Return a job descriptor to the user as successful response
* Possibly rank the job, using requester's customer_id


### Requesting the state of a Job
* A GET request with job descriptor
* check the DB and fetch the status, return it as the response.

### Fetching a Job and submitting to Quantum Computer
* Get the highest ranked job in the DB and submit it to QC
* When QC is done, at a later time, listen to QC and store result/update in DB with the job descriptor

## Test
I will try `behave` to implement BDD tests if time permits.
There will be unit tests with `pytest`


