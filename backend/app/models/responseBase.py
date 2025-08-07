from pydantic import BaseModel
from typing import Any, Generic, TypeVar, Optional

T = TypeVar("T")

class ResponseBase(BaseModel, Generic[T]):
    status: int
    msg: str
    data: Optional[T] = None  # `data` es opcional por defecto
