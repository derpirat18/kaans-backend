from sqlalchemy import Column, Integer, String # Importamos las clases Column, Integer y String de SQLAlchemy para definir las columnas de nuestra tabla de categorías en la base de datos.

from app.db.session import Base # Importamos la clase Base que definimos en session.py para crear nuestro modelo de categoría, que hereda de Base para que SQLAlchemy pueda mapearlo a una tabla en la base de datos.


class Categoria(Base): # Aquí definimos la clase Categoria que representa a las categorías en nuestra aplicación, y hereda de Base para que SQLAlchemy pueda mapearla a una tabla en la base de datos. Esta clase tiene los campos id, nombre, descripcion y color, que corresponden a las columnas de la tabla de categorías en la base de datos.
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True)
    descripcion = Column(String, nullable=True)
    color = Column(String, nullable=True)