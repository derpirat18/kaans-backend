from fastapi import APIRouter, Depends, HTTPException, status # Importamos las herramientas necesarias de FastAPI para crear rutas, manejar dependencias, lanzar excepciones HTTP y definir códigos de estado.
from sqlalchemy.orm import Session # Importamos la clase Session de SQLAlchemy para manejar las sesiones de base de datos.

from app.db.session import get_db # Importamos la función get_db que definimos en session.py para obtener una sesión de base de datos.
from app.schemas.curso import CursoCreate, CursoUpdate, CursoRead # Importamos los esquemas de Pydantic que definimos en curso.py para validar los datos de entrada y salida de nuestras rutas.
from app.services import curso_service # Importamos el módulo de servicios de curso que definimos en curso_service.py para manejar la lógica de negocio relacionada con los cursos.

router = APIRouter(prefix="/api/cursos", tags=["cursos"]) # Aquí creamos un router de FastAPI con el prefijo "/api/cursos" para agrupar todas las rutas relacionadas con los cursos, y le asignamos la etiqueta "cursos" para documentarlas en la API.

@router.get("", response_model=list[CursoRead]) # Aquí definimos una ruta GET para obtener todos los cursos, y especificamos que la respuesta será una lista de objetos CursoRead.
def listar_cursos(db: Session = Depends(get_db)): # Esta función se ejecutará cuando  alguien haga una solicitud GET a "/api/cursos". Recibe una sesión de base de datos como dependencia usando Depends(get_db).
    return curso_service.get_cursos(db) # Aquí llamamos a la función get_cursos del servicio de curso para obtener la lista de cursos de la base de datos, y la devolvemos como respuesta.

@router.get("/{slug}", response_model=CursoRead) # Aquí definimos una ruta GET para obtener un curso por su slug, y especificamos que la respuesta será un objeto CursoRead.
def obtener_curso(slug: str, db: Session = Depends(get_db)): # Esta función se ejecutará cuando alguien haga una solicitud GET a "/api/cursos/{slug}". Recibe el slug del curso como parámetro de ruta y una sesión de base de datos como dependencia.
    curso = curso_service.get_curso_by_slug(db, slug) # Aquí llamamos a la función get_curso_by_slug del servicio de curso para buscar el curso en la base de datos usando el slug.
    if curso is None: # Si no se encuentra el curso, lanzamos una excepción HTTP 404 Not Found con un mensaje de error.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado")
    return curso # Si se encuentra el curso, lo devolvemos como respuesta.

@router.post("", response_model=CursoRead, status_code=status.HTTP_201_CREATED) # Aquí definimos una ruta POST para crear un nuevo curso, y especificamos que la respuesta será un objeto CursoRead y el código de estado será 201 Created.
def crear_curso(curso_in: CursoCreate, db: Session = Depends(get_db)): # Esta función se ejecutará cuando alguien haga una solicitud POST a "/api/cursos". Recibe un objeto CursoCreate con los datos del nuevo curso y una sesión de base de datos como dependencia.
    existente = curso_service.get_curso_by_slug(db, curso_in.slug) # Aquí llamamos a la función get_curso_by_slug del servicio de curso para verificar si ya existe un curso con el mismo slug en la base de datos.
    if existente is not None: # Si ya existe un curso con ese slug, lanzamos una excepción HTTP 409 Conflict con un mensaje de error.
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un curso con ese slug") # Esto evita que se creen cursos con slugs duplicados, lo que podría causar problemas de identificación y acceso a los cursos.
    return curso_service.create_curso(db, curso_in) # Si no existe un curso con ese slug, llamamos a la función create_curso del servicio de curso para crear el nuevo curso en la base de datos, y lo devolvemos como respuesta.

@router.put("/{slug}", response_model=CursoRead) # Aquí definimos una ruta PUT para actualizar un curso existente por su slug, y especificamos que la respuesta será un objeto CursoRead.
def actualizar_curso(slug: str, curso_in: CursoUpdate, db: Session = Depends(get_db)): # Esta función se ejecutará cuando alguien haga una solicitud PUT a "/api/cursos/{slug}". Recibe el slug del curso a actualizar como parámetro de ruta, un objeto CursoUpdate con los datos a actualizar y una sesión de base de datos como dependencia.
    curso = curso_service.get_curso_by_slug(db, slug) # Aquí llamamos a la función get_curso_by_slug del servicio de curso para buscar el curso en la base de datos usando el slug.
    if curso is None: # Si no se encuentra el curso, lanzamos una excepción HTTP 404 Not Found con un mensaje de error.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado")
    return curso_service.update_curso(db, curso, curso_in) # Si se encuentra el curso, llamamos a la función update_curso del servicio de curso para actualizar el curso en la base de datos con los nuevos datos, y lo devolvemos como respuesta.

@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT) # Aquí definimos una ruta DELETE para eliminar un curso por su slug, y especificamos que el código de estado será 204 No Content (sin contenido en la respuesta).
def eliminar_curso(slug: str, db: Session = Depends(get_db)): # Esta función se ejecutará cuando alguien haga una solicitud DELETE a "/api/cursos/{slug}". Recibe el slug del curso a eliminar como parámetro de ruta y una sesión de base de datos como dependencia.
    curso = curso_service.get_curso_by_slug(db, slug) # Aquí llamamos a la función get_curso_by_slug del servicio de curso para buscar el curso en la base de datos usando el slug.
    if curso is None: # Si no se encuentra el curso, lanzamos una excepción HTTP 404 Not Found con un mensaje de error.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado")
    curso_service.delete_curso(db, curso) # Si se encuentra el curso, llamamos a la función delete_curso del servicio de curso para eliminar el curso de la base de datos. No devolvemos nada en la respuesta, ya que el código de estado 204 indica que la operación fue exitosa pero no hay contenido que devolver.