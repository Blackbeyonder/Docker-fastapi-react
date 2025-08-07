# app/models/__init__.py
from sqlalchemy.ext.declarative import declarative_base
# from .user import User  # Comentado porque no existe el archivo user.py


Base = declarative_base()

__all__ = ['Base']
# Solo importa los modelos de WMS en los módulos WMS, y los de OMS/TMS en los suyos