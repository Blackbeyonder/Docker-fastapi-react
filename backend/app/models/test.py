from sqlalchemy import Column, Float, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Test(Base):
    __tablename__ = "test"
    
    id_ubicacion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    latitud = Column(Float)
    longitud = Column(Float)
    timestamp = Column(DateTime)

    def to_dict(self):
        return {
            "id_ubicacion": self.id_ubicacion,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "timestamp": self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else None
        }




