from dataclasses import dataclass
from enum import Enum
from typing import Callable, List, Optional


class FunctionBindType(Enum):
    FROM_PYTHON = "python"
    FROM_JS = "js"


@dataclass
class FunctionBind:
    bind_type: FunctionBindType
    is_async: bool = False
    func: Optional[Callable] = None
    params: Optional[List[str]] = None
