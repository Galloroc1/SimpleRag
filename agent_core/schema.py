from typing import List, Dict, Any
from pydantic import BaseModel, ValidationError
from typing import Type, List, TypeVar

from pydantic import BaseModel, ValidationError, create_model
from typing import Type, List, TypeVar


import dataclasses


@dataclasses.dataclass
class Messages:
    messages: dict = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class SystemErrorInformation:
    error_messages: dict = dataclasses.field(default_factory=dict)
    # dtype and reason


@dataclasses.dataclass
class Params:
    description: str = "name"
    dtype: type = "type of this params"
    default: str = "default value"
    is_must: bool = True
    param_range: List[Any] = dataclasses.field(default_factory=list)

    def __str__(self):
        return str(self.__dict__)


T = TypeVar('T')

class ListOfTypeModel(BaseModel):
    data: List[T]
