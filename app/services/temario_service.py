from sqlalchemy.orm import Session # importamos la clase Session de SQLAlchemy para interactuar con la base de datos.

from app.models.modulo import Modulo # importamos el modelo Modulo para poder usarlo en nuestras funciones de servicio.
from app.models.tema import Tema # importamos el modelo Tema para poder usarlo en nuestras funciones de servicio.
from app.schemas.modulo import ModuloCreate # importamos el esquema de Pydantic para validar los datos de entrada en nuestras funciones de servicio, este esquema se usa para crear un nuevo módulo.
from app.schemas.tema import TemaCreate # importamos el esquema de Pydantic para validar los datos de entrada en nuestras funciones de servicio, este esquema se usa para crear un nuevo tema.


def get_modulo_by_id(db: Session, modulo_id: int) -> Modulo | None: # esta función recibe una sesión de base de datos y un id de módulo, y devuelve un módulo o None si no se encuentra.
    return db.query(Modulo).filter(Modulo.id == modulo_id).first()


def create_modulo(db: Session, curso_id: int, modulo_in: ModuloCreate) -> Modulo: # esta función recibe una sesión de base de datos, un id de curso y un objeto ModuloCreate, y devuelve el módulo creado. El id de curso se usa para asociar el nuevo módulo al curso correspondiente en la base de datos.
    nuevo_modulo = Modulo(
        curso_id=curso_id,
        numero=modulo_in.numero,
        titulo=modulo_in.titulo,
        orden=modulo_in.orden,
    )
    db.add(nuevo_modulo)
    db.commit()
    db.refresh(nuevo_modulo)
    return nuevo_modulo


def create_tema(db: Session, modulo_id: int, tema_in: TemaCreate) -> Tema: # esta función recibe una sesión de base de datos, un id de módulo y un objeto TemaCreate, y devuelve el tema creado. El id de módulo se usa para asociar el nuevo tema al módulo correspondiente en la base de datos.
    nuevo_tema = Tema(
        modulo_id=modulo_id,
        texto=tema_in.texto,
        orden=tema_in.orden,
    )
    db.add(nuevo_tema)
    db.commit()
    db.refresh(nuevo_tema)
    return nuevo_tema