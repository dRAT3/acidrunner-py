from typing import Any, List, Optional, NamedTuple, Dict
from dataclasses import dataclass

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
    t0: Optional[int] = None
    t1: Optional[int] = None

    succes: bool = False

