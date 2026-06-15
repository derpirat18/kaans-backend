from sqlalchemy.orm import Session # importamos la clase Session de SQLAlchemy para interactuar con la base de datos.
from app.models.curso import Curso # importamos el modelo Curso para poder usarlo en nuestras funciones de servicio.
from app.schemas.curso import CursoCreate, CursoUpdate # importamos los esquemas de Pydantic para validar los datos de entrada en nuestras funciones de servicio.

def get_cursos(db: Session) -> list[Curso]: # esta función recibe una sesión de base de datos y devuelve una lista de cursos.
    return db.query(Curso).all()  # esta función devuelve una lista de cursos de la base de datos.

def get_curso_by_slug(db: Session, slug: str) -> Curso | None:  # esta función recibe una sesión de base de datos y un slug, y devuelve un curso o None si no se encuentra.
    return db.query(Curso).filter(Curso.slug == slug).first()   # esta función busca un curso en la base de datos que tenga el mismo slug que el que se le pasó como argumento,
                                                                # y devuelve el primer resultado o None si no se encuentra.

def create_curso(db: Session, curso_in: CursoCreate) -> Curso:  # esta función recibe una sesión de base de datos y un objeto CursoCreate, y devuelve el curso creado.
    nuevo_curso = Curso(**curso_in.model_dump()) # aquí creamos una nueva instancia de la clase Curso usando los datos del objeto CursoCreate que se le pasó como argumento.
    db.add(nuevo_curso) # aquí agregamos el nuevo curso a la sesión de base de datos.
    db.commit() # aquí confirmamos los cambios en la base de datos para guardar el nuevo curso.
    db.refresh(nuevo_curso) # aquí refrescamos el objeto curso para obtener su id generado automáticamente por la base de datos.
    return nuevo_curso # aquí devolvemos el curso creado.

def update_curso(db: Session, curso: Curso, curso_in: CursoUpdate) -> Curso:    # esta función recibe una sesión de base de datos, un curso existente y un objeto CursoUpdate, 
                                                                                # y devuelve el curso actualizado.
    datos_a_actualizar = curso_in.model_dump(exclude_unset=True)    # aquí obtenemos un diccionario con los datos del objeto CursoUpdate que se le pasó como argumento, 
                                                                    # excluyendo los campos que no se actualizaron.
    for campo, valor in datos_a_actualizar.items(): # aquí iteramos sobre los campos y valores que se van a actualizar.
        setattr(curso, campo, valor) # aquí actualizamos el campo del curso con el nuevo valor usando la función setattr.
    db.commit() # aquí confirmamos los cambios en la base de datos para guardar el curso actualizado.
    db.refresh(curso) # aquí refrescamos el objeto curso para obtener los datos actualizados de la base de datos.
    return curso # aquí devolvemos el curso actualizado.

def delete_curso(db: Session, curso: Curso) -> None: # esta función recibe una sesión de base de datos y un curso existente, y no devuelve nada.
    db.delete(curso) # aquí eliminamos el curso de la sesión de base de datos.
    db.commit() # aquí confirmamos los cambios en la base de datos para eliminar el curso.