import time
from enum import Enum
from queue import Empty, Queue
from threading import Thread, Lock

from .job import Job, JobState
from .job_result import JobResultType
from .service_response import ServiceResponse
from .runtimes.runtime import Runtime

class ServiceResponseType(Enum):
    SUBMIT_SUCCESS = 1
    QUERY_SUCCESS = 2
    FAILED_ON_SUBMISSION = 5
    FAILED_DURING_EXECUTION = 6
    JOB_NOT_FOUND = 7

"""
This thread is just a place holder for Quantum Computer service
"""
def qc_thread_func(runtime:Runtime, qc_in:Queue, qc_out:Queue):
    print('qc_thread started')
    #TODO: exit condition must be implemented for this thread
    while True:
        try:
            print('qc_thread: polling input queue')
            job = qc_in.get(timeout=0.1)
            print('qc_thread: job available, execute via runtime')
            resp = runtime.execute(job)
            qc_in.task_done()
            print('qc_thread: job executed, sending result')
            qc_out.put(resp)
        except Empty:
            pass # input queue is empty
            print('qc_thread: input queue empty, sleeping')
            time.sleep(1)
    
"""
In a production setup, the qc_thread_func would be replaced with a service that serves jobs to Quantum Computer
"""

class BackendService:
    def __init__(self, runtime:Runtime) -> None:
        # the job list "jobs" will be a DB in a production setting, hence making lock() obsolete
        self._jobs=[]
        self._runtime = runtime
        self._lock = Lock() # query/submit/run can be called from different threads/tasks, hence protect the job list
        self._qcq_in = Queue(10)
        self._qcq_out = Queue(10)
        self._qc_t = None

    def start_qc_thread(self):
        self._qc_t = Thread(target=qc_thread_func, args=(self._runtime, self._qcq_in, self._qcq_out,))
        self._qc_t.setDaemon(True) # detached thread
        self._qc_t.start()

    """
    submit() method will send the jobs that are in WAITING state to the Quantum Computer and update
             the state of the job accordingly.
             Returns the job_id and submission state.
    """
    def submit(self, job:Job):
        self._lock.acquire()  # exclusive access to jobs list
        #TODO: What about the failure to submit and relevant response
        job.state = JobState.WAITING
        self._jobs.append(job)
        resp = ServiceResponse(ServiceResponseType.SUBMIT_SUCCESS, {"job_ident":job.ident})
        self._lock.release()
        return resp

    """
    query() method will check the job list for given job ident
            Returns the job state
    """
    def query(self, job_id):
        self._lock.acquire() # exclusive access to jobs list
        # start by assuming job_id not found in jobs list
        resp = ServiceResponse(ServiceResponseType.JOB_NOT_FOUND)
        for job in self._jobs:
            if job.ident == job_id:
                resp = ServiceResponse(ServiceResponseType.QUERY_SUCCESS, {"job":job})
                break
        self._lock.release()
        return resp
    
    """
    run() method will submit the waiting jobs to Quantum Computer
          and then collect the responses. Job list is updated upon 
          submission and when a response is retrieved
    """
    def run(self):
        self._lock.acquire() # exclusive access to jobs list
        for job in self._jobs:
            if job.state == JobState.WAITING:
                print('service: found job waiting, submitting to qc')
                job.state = JobState.SUBMITTED
                self._qcq_in.put(job)
        self._lock.release()

        try:
            resp = self._qcq_out.get()
            self._lock.acquire() # exclusive access to jobs list
            for job in self._jobs:
                if resp.data['job_id'] == job.ident:   #TODO pass in job in response, job_id, job_ident keys are getting entangled.
                    if resp.result_type == JobResultType.SUCCESS:
                        job.state = JobState.COMPLETED
                    else:
                        job.state = JobState.FAILED
            self._lock.release()
        except Empty:
            pass # qc output queue is empty, either idle or current job is still running
