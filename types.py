from typing import Any, List, Optional, NamedTuple, Dict
from dataclasses import dataclass

class FunctionInfo(NamedTuple):
    function_name: str
    filenames: Optional[List[str]]
    args: Optional[List[Any]]

@dataclass
class CorrosiveTaskData:
    task_id: str
    run: int
    name: str
    func = FunctionInfo
    meta_data: Dict 

    result: Optional[Any]
    t0: Optional[int] = None
    t1: Optional[int] = None

    succes: Optional[bool] = False
