# models/operador.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Operador(Base):
    __tablename__ = 'operadores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    apellido_paterno = Column(String, nullable=False)
    apellido_materno = Column(String, nullable=False)
    RFC = Column(String, nullable=False)
    email = Column(String, nullable=False)
    NSS = Column(String, nullable=False)
    telefono = Column(Integer, nullable=False)
    licencia = Column(String, nullable=False)
    contrasena = Column(String, nullable=True)
    last_activity = Column(DateTime)
    token_fcm = Column(String)

    linea_transporte_id = Column(Integer, ForeignKey('linea_transporte.id'), nullable=False)

    linea_transporte = relationship("LineaTransporte", back_populates="operadores")
