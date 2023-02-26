import time
from enum import Enum
from queue import Empty, Queue
from multiprocessing import Process
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

def qc_thread(runtime:Runtime, qc_in:Queue, qc_out:Queue):
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
    
qc_in = Queue(10)
qc_out = Queue(10)

"""
Submit: will update jobs list and then put the job into Quantum Computer's queue
Query : will query the job list and return the state
"""
class BackendService:
    def __init__(self, runtime:Runtime) -> None:
        self._jobs=[]
        self._runtime = runtime
        self._lock = Lock()
        self._qc = None

    def start_qc_thread(self):
        global qc_in, qc_out
        self._qc = Thread(target=qc_thread, args=(self._runtime, qc_in, qc_out,))
        self._qc.setDaemon(True) # detached thread
        self._qc.start()

    def submit(self, job:Job):
        self._lock.acquire()  # exclusive access to jobs list
        #TODO: What about the failure to submit and relevant response
        job.state = JobState.WAITING
        self._jobs.append(job)
        resp = ServiceResponse(ServiceResponseType.SUBMIT_SUCCESS, {"job_ident":job.ident})
        self._lock.release()
        return resp

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
    
    def run(self):
        global qc_out, qc_in
        self._lock.acquire() # exclusive access to jobs list
        for job in self._jobs:
            if job.state == JobState.WAITING:
                print('service: found job waiting, submitting to qc')
                job.state = JobState.SUBMITTED
                qc_in.put(job)
        self._lock.release()

        try:
            resp = qc_out.get()
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
