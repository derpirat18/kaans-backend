from sqlalchemy import Column, Integer, String, Boolean # importamos las clases necesarias de SQLAlchemy para definir nuestras tablas y sus columnas.

from app.db.session import Base # importamos la clase Base que definimos en session.py para usarla como base para nuestra tabla.


class Usuario(Base): # aquí definimos la clase Usuario, que representa la tabla "usuarios" en la base de datos.
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    nombre = Column(String(150), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False, default="editor")
    activo = Column(Boolean, nullable=False, default=True)