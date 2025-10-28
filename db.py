"""
Módulo de configuración de la base de datos para la Tienda Online.
Usa SQLModel (basado en SQLAlchemy) y SQLite como motor local.
"""

from sqlmodel import SQLModel, create_engine, Session

# Nombre del archivo de base de datos local
DATABASE_URL = "sqlite:///tienda.db"

# Se crea el motor de conexión
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """
    Crea todas las tablas definidas en los modelos SQLModel.
    Se ejecutará al iniciar la aplicación.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Devuelve una sesión activa para interactuar con la base de datos.
    Se usa en los endpoints para CRUD.
    """
    with Session(engine) as session:
        yield session
