from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TestBase(BaseModel):
    id_ubicacion: Optional[int] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    timestamp: Optional[datetime] = None

class RequestTestBase(BaseModel):
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    timestamp: Optional[datetime] = None
    