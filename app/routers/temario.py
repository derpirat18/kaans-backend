from fastapi import APIRouter, Depends, HTTPException, status # Importamos las herramientas necesarias de FastAPI para crear rutas, manejar dependencias, lanzar excepciones HTTP y definir códigos de estado.
from sqlalchemy.orm import Session # Importamos la clase Session de SQLAlchemy para manejar las sesiones de base de datos.

from app.db.session import get_db   # Importamos la función get_db que definimos en session.py para obtener una sesión de base de datos, que se usará como dependencia en las rutas que requieren acceso a la base de datos.
from app.schemas.modulo import ModuloCreate, ModuloRead # Importamos los esquemas de Pydantic que definimos en modulo.py para validar los datos de entrada y salida de nuestras rutas relacionadas con los módulos.
from app.schemas.tema import TemaCreate, TemaRead # Importamos los esquemas de Pydantic que definimos en tema.py para validar los datos de entrada y salida de nuestras rutas relacionadas con los temas.
from app.services import curso_service, temario_service # Importamos los módulos de servicios de curso y temario que definimos en curso_service.py y temario_service.py para manejar la lógica de negocio relacionada con los cursos, módulos y temas, que se usará en nuestras rutas para crear módulos y temas asociados a cursos y módulos existentes.
from app.core.deps import get_current_user # Importamos la función get_current_user que definimos en deps.py para obtener el usuario actual a partir del token de acceso JWT, que se usará como dependencia en las rutas que requieren autenticación para protegerlas y obtener la información del usuario autenticado.
from app.models.usuario import Usuario  # Importamos el modelo Usuario que definimos en usuario.py para representar a los usuarios en la base de datos, que se usará para obtener el usuario actual en las rutas que requieren autenticación.

router = APIRouter(prefix="/api", tags=["temario"]) # Aquí creamos un router de FastAPI con el prefijo "/api" para agrupar todas las rutas relacionadas con el temario (módulos y temas), y le asignamos la etiqueta "temario" para documentarlas en la API. Las rutas específicas para módulos y temas se definirán a continuación, usando este router para organizarlas bajo el mismo prefijo y etiqueta.


@router.post("/cursos/{slug}/modulos", response_model=ModuloRead, status_code=status.HTTP_201_CREATED) # Aquí definimos una ruta POST para crear un nuevo módulo asociado a un curso existente, usando el slug del curso como parte de la URL para identificarlo. Especificamos que la respuesta será un objeto ModuloRead y el código de estado será 201 Created.
def crear_modulo(
    slug: str,
    modulo_in: ModuloCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    curso = curso_service.get_curso_by_slug(db, slug)
    if curso is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado")
    return temario_service.create_modulo(db, curso.id, modulo_in)


@router.post("/modulos/{modulo_id}/temas", response_model=TemaRead, status_code=status.HTTP_201_CREATED) # Aquí definimos una ruta POST para crear un nuevo tema asociado a un módulo existente, usando el id del módulo como parte de la URL para identificarlo. Especificamos que la respuesta será un objeto TemaRead y el código de estado será 201 Created.
def crear_tema(
    modulo_id: int,
    tema_in: TemaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    modulo = temario_service.get_modulo_by_id(db, modulo_id)
    if modulo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Modulo no encontrado")
    return temario_service.create_tema(db, modulo_id, tema_in)