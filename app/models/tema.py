from sqlalchemy import Column, Integer, String, Text, ForeignKey # importamos las clases necesarias de SQLAlchemy para definir nuestras tablas y sus columnas, incluyendo ForeignKey para establecer relaciones entre tablas.
from sqlalchemy.orm import relationship # importamos la función relationship de SQLAlchemy para definir las relaciones entre nuestras tablas, lo que nos permitirá acceder a los módulos de un curso y a los temas de un módulo de manera más sencilla.

from app.db.session import Base # importamos la clase Base que definimos en session.py para usarla como base para nuestra tabla. Esto nos permitirá definir nuestra tabla como una clase de Python que hereda de Base, lo que es necesario para que SQLAlchemy pueda mapearla a la base de datos.


class Tema(Base): # aquí definimos la clase Tema, que representa la tabla "temas" en la base de datos.
    __tablename__ = "temas"

    id = Column(Integer, primary_key=True, index=True)
    modulo_id = Column(Integer, ForeignKey("modulos.id"), nullable=False, index=True)
    texto = Column(Text, nullable=False)
    orden = Column(Integer, nullable=False, default=0)

    modulo = relationship("Modulo", back_populates="temas")