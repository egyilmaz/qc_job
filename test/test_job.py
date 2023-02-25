import pytest
from src.backend.exceptions import EmptyJob, InvalidAxis, InvalidDelimeter, InvalidToken
from src.backend.job_factory import JobFactory

def test_job_ctor_success():
    job = JobFactory.create("rotation", 'X(90), Y(180), X(90)')
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
        job = JobFactory.create("rotation", '')

    with pytest.raises(EmptyJob) as e_info:
        job = JobFactory.create("rotation", None)

def test_job_ctor_invalid_axis():
    with pytest.raises(InvalidAxis) as e_info:
        job = JobFactory.create("rotation", 'Z(90), X(90)')

def test_job_ctor_invalid_delimeter():
    with pytest.raises(InvalidDelimeter) as e_info:
        job = JobFactory.create("rotation",'X(90) Y(90)')

def test_job_ctor_single_delimeter():
    with pytest.raises(InvalidToken) as e_info:
        job = JobFactory.create("rotation",'X(90) Y(90), X(180)')

#TODO: There are might be more errornous strings, parsing should be checked further
