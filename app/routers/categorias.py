from fastapi import APIRouter, Depends, HTTPException, status # Importamos las herramientas necesarias de FastAPI para crear rutas, manejar dependencias, lanzar excepciones HTTP y definir códigos de estado.
from sqlalchemy.orm import Session # Importamos la clase Session de SQLAlchemy para manejar las sesiones de base de datos.

from app.db.session import get_db # Importamos la función get_db que definimos en session.py para obtener una sesión de base de datos.
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaRead   # Importamos los esquemas de Pydantic que definimos en categoria.py para validar los datos de entrada y salida de nuestras rutas.
from app.services import categoria_service # Importamos el módulo de servicios de categoría que definimos en categoria_service.py para manejar la lógica de negocio relacionada con las categorías, como la creación, actualización y eliminación de categorías, que se usará para obtener la lista de categorías, crear nuevas categorías, actualizar categorías existentes y eliminar categorías.
from app.core.deps import get_current_superadmin # Importamos la función get_current_superadmin que definimos en deps.py para obtener el superadmin actual a partir del token de acceso JWT, que se usará como dependencia en las rutas que requieren permisos de superadmin para protegerlas y obtener la información del superadmin autenticado.
from app.models.usuario import Usuario # Importamos el modelo Usuario que definimos en usuario.py para representar a los usuarios en la base de datos, que se usará como tipo de retorno en las funciones de nuestras rutas. Aunque estas rutas están relacionadas con las categorías, es importante tener acceso al modelo Usuario para poder usarlo como tipo de retorno en las funciones de nuestras rutas, especialmente cuando necesitamos verificar los permisos del usuario autenticado para realizar ciertas acciones, como crear, actualizar o eliminar categorías.

router = APIRouter(prefix="/api/categorias", tags=["categorias"]) # Aquí creamos un router de FastAPI con el prefijo "/api/categorias" para agrupar todas las rutas relacionadas con las categorías, y le asignamos la etiqueta "categorias" para documentarlas en la API. Este router se incluirá luego en el archivo main.py para que las rutas estén disponibles en la aplicación.


@router.get("", response_model=list[CategoriaRead]) # Aquí definimos una ruta GET para obtener todas las categorías, y especificamos que la respuesta será una lista de objetos CategoriaRead.
def listar_categorias(db: Session = Depends(get_db)): 
    return categoria_service.get_categorias(db)


@router.post("", response_model=CategoriaRead, status_code=status.HTTP_201_CREATED) # Aquí definimos una ruta POST para crear una nueva categoría, y especificamos que la respuesta será un objeto CategoriaRead y el código de estado será 201 Created.
def crear_categoria(
    categoria_in: CategoriaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superadmin),
):
    existente = categoria_service.get_categoria_by_nombre(db, categoria_in.nombre) # Antes de crear una nueva categoría, verificamos si ya existe una categoría con el mismo nombre usando la función get_categoria_by_nombre del servicio de categoría. Esto es importante para garantizar que el nombre de la categoría sea único en la base de datos y evitar conflictos o duplicados.
    if existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una categoria con ese nombre",
        )
    return categoria_service.create_categoria(db, categoria_in)


@router.put("/{categoria_id}", response_model=CategoriaRead) # Aquí definimos una ruta PUT para actualizar una categoría existente por su ID, y especificamos que la respuesta será un objeto CategoriaRead. Esta ruta permite actualizar los campos de una categoría, como su nombre, descripción o color, pero no permite cambiar el ID de la categoría, ya que el ID se usa como identificador único para buscar a la categoría en la base de datos.
def actualizar_categoria(
    categoria_id: int,
    categoria_in: CategoriaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superadmin),
):
    categoria = categoria_service.get_categoria_by_id(db, categoria_id)
    if categoria is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria no encontrada")
    return categoria_service.update_categoria(db, categoria, categoria_in)


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)   # Aquí definimos una ruta DELETE para eliminar una categoría por su ID, y especificamos que el código de estado será 204 No Content, lo que indica que la eliminación fue exitosa pero no se devuelve ningún contenido en la respuesta.
def eliminar_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superadmin),
):
    categoria = categoria_service.get_categoria_by_id(db, categoria_id)
    if categoria is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria no encontrada")
    categoria_service.delete_categoria(db, categoria)