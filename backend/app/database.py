# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


# Cargar variables de entorno desde el archivo .env
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
print(DATABASE_URL)

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL no está configurado en el archivo .env")

# Crear el engine de SQLAlchemy para conectarse a la base de datos
engine = create_engine(
    DATABASE_URL,
    pool_size=40,
    max_overflow=90,
    pool_timeout=30,
    pool_recycle=1800
)
# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos de la base de datos
Base = declarative_base()

# Función para obtener una sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


