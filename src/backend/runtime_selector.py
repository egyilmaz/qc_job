from enum import Enum
from .runtimes.runtime_verbatim import RuntimeVerbatim
from .runtimes.runtime_simulated import RuntimeSimulated
from .runtimes.runtime_echo import RuntimeEcho

class RuntimeType(Enum):
    VERBATIM = 1   # submits the job to QC process as a future
    SIMULATED = 2  # submits the job to simulation
    ECHO = 3 # returns random fake results (success or error codes)

class RuntimeSelector:
    def __init__(self) -> None:
        pass

    def select(runtime_type:RuntimeType):
        match runtime_type:
            case RuntimeType.VERBATIM:
                return RuntimeVerbatim()
            case RuntimeType.SIMULATED:
                return RuntimeSimulated()
            case RuntimeType.ECHO:
                return RuntimeEcho()
            case _:
                return ValueError(f"Unknown runtime type:{runtime_type}")
        