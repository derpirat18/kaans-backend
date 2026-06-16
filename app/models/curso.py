from sqlalchemy import Column, Integer, String, Text    # importamos las clases necesarias de SQLAlchemy para definir nuestras tablas y sus columnas.
from app.db.session import Base    # importamos la clase Base que definimos en session.py para usarla como base para nuestra tabla.
from sqlalchemy.orm import relationship # importamos la función relationship de SQLAlchemy para definir las relaciones entre nuestras tablas, lo que nos permitirá acceder a los módulos de un curso y a los temas de un módulo de manera más sencilla.

class Curso(Base):   # aquí definimos la clase Curso, que representa la tabla "cursos" en la base de datos.
    __tablename__ = "cursos"   # esta línea le dice a SQLAlchemy que el nombre de la tabla en la base de datos será "cursos".

    id = Column(Integer, primary_key=True, index=True) # aquí definimos la columna "id" como un entero que es la clave primaria de la tabla y se indexa para mejorar el rendimiento de las consultas.
    slug = Column(String(150), unique=True, index=True, nullable=False) # aquí definimos la columna "slug" como una cadena de texto de hasta 150 caracteres, que debe ser única, se indexa para mejorar el rendimiento de las consultas y no puede ser nula.
    titulo = Column(String(200), nullable=False) # aquí definimos la columna "titulo" como una cadena de texto de hasta 200 caracteres, y no puede ser nula.
    categoria = Column(String(100), nullable=False) # aquí definimos la columna "categoria" como una cadena de texto de hasta 100 caracteres, y no puede ser nula.
    descripcion = Column(Text, nullable=True) # aquí definimos la columna "descripcion" como un texto largo, y puede ser nula.
    duracion_horas = Column(Integer, nullable=True) # aquí definimos la columna "duracion_horas" como un entero, y puede ser nula.
    nivel = Column(String(100), nullable=True) # aquí definimos la columna "nivel" como una cadena de texto de hasta 100 caracteres, y puede ser nula.
    modalidad = Column(String(150), nullable=True) # aquí definimos la columna "modalidad" como una cadena de texto de hasta 150 caracteres, y puede ser nula.
    modulos = relationship("Modulo", back_populates="curso", cascade="all, delete-orphan", order_by="Modulo.orden") # aquí definimos la relación entre la tabla "cursos" y la tabla "modulos". Esto nos permitirá acceder a los módulos de un curso de manera más sencilla. La opción cascade="all, delete-orphan" asegura que cuando se elimine un curso, también se eliminen sus módulos asociados, y order_by="Modulo.orden" asegura que los módulos se ordenen por su campo "orden".