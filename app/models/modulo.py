from sqlalchemy import Column, Integer, String, ForeignKey # importamos las clases necesarias de SQLAlchemy para definir nuestras tablas y sus columnas, incluyendo ForeignKey para establecer relaciones entre tablas.
from sqlalchemy.orm import relationship # importamos la función relationship de SQLAlchemy para definir las relaciones entre nuestras tablas, lo que nos permitirá acceder a los módulos de un curso y a los temas de un módulo de manera más sencilla.

from app.db.session import Base # importamos la clase Base que definimos en session.py para usarla como base para nuestra tabla. Esto nos permitirá definir nuestra tabla como una clase de Python que hereda de Base, lo que es necesario para que SQLAlchemy pueda mapearla a la base de datos.


class Modulo(Base): # aquí definimos la clase Modulo, que representa la tabla "modulos" en la base de datos.
    __tablename__ = "modulos"

    id = Column(Integer, primary_key=True, index=True)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False, index=True)
    numero = Column(String(10), nullable=False)
    titulo = Column(String(200), nullable=False)
    orden = Column(Integer, nullable=False, default=0)

    curso = relationship("Curso", back_populates="modulos")
    temas = relationship("Tema", back_populates="modulo", cascade="all, delete-orphan")