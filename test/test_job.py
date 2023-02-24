import pytest
from src.backend.exceptions import EmptyJob
from src.backend.job import Job

def test_job_ctor_empty_str():
    with pytest.raises(EmptyJob) as e_info:
        job = Job('')

def test_job_ctor_success():
    job = Job('X(90), Y(180), X(90)')
    rotations = job.rotations()
    assert len(rotations) == 3        
    assert rotations[0].axis() == 'X'
    assert rotations[0].angle() == 90 
    assert rotations[1].axis() == 'Y'
    assert rotations[1].angle() == 180 
    assert rotations[2].axis() == 'X'
    assert rotations[2].angle() == 90 
