from typing import Any, List, Optional, NamedTuple, Dict, Tuple
from dataclasses import dataclass

@dataclass
class AcidCosineResult:
    buffer1: List[float]
    buffer2: List[float]
    a_range: Optional[Tuple[float, float]] = (0.0, 0.0)
    meta_data: Dict = {}

@dataclass
class AcidBoolResult:
    result: bool
    meta_data: Dict = {}

@dataclass
class AcidFloatResult:
    result: float 
    a_range: Tuple[float, float] = (0.0, 0.0)
    meta_data: Dict = {}

class FunctionInfo(NamedTuple):
    function_name: str
    filenames: List[str]
    args: Optional[List[Any]]

class CorrosiveTaskDataImmutable(NamedTuple):
    task_id: str
    name: str
    func: FunctionInfo
    args: Optional[List[str]]
    sut_name: str

@dataclass
class CorrosiveTaskData:
    immutable: CorrosiveTaskDataImmutable
    meta_data: Dict 
    result: Optional[Any]
    elapsed: Optional[int] = None

    executed: bool = False
    succes: bool = False

