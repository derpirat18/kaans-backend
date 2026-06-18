from fastapi import APIRouter, Depends, HTTPException, status # Importamos las herramientas necesarias de FastAPI para crear rutas, manejar dependencias, lanzar excepciones HTTP y definir códigos de estado.
from sqlalchemy.orm import Session # Importamos la clase Session de SQLAlchemy para manejar las sesiones de base de datos.

from app.db.session import get_db # Importamos la función get_db que definimos en session.py para obtener una sesión de base de datos.
from app.schemas.usuario import UsuarioCreate, UsuarioRead, UsuarioUpdate # Importamos los esquemas de Pydantic que definimos en usuario.py para validar los datos de entrada y salida de nuestras rutas.
from app.services import usuario_service # Importamos el módulo de servicios de usuario que definimos en usuario_service.py para manejar la lógica de negocio relacionada con los usuarios, como la autenticación y creación de usuarios, que se usará para obtener la lista de usuarios, crear nuevos usuarios y desactivar usuarios existentes.
from app.core.deps import get_current_superadmin # Importamos la función get_current_superadmin que definimos en deps.py para obtener el superadmin actual a partir del token de acceso JWT, que se usará como dependencia en las rutas que requieren permisos de superadmin para protegerlas y obtener la información del superadmin autenticado.
from app.models.usuario import Usuario # Importamos el modelo Usuario que definimos en usuario.py para representar a los usuarios en la base de datos, que se usará como tipo de retorno en las funciones de nuestras rutas.

router = APIRouter(prefix="/api/usuarios", tags=["usuarios"]) # Aquí creamos un router de FastAPI con el prefijo "/api/usuarios" para agrupar todas las rutas relacionadas con los usuarios, y le asignamos la etiqueta "usuarios" para documentarlas en la API. Este router se incluirá luego en el archivo main.py para que las rutas estén disponibles en la aplicación.


@router.get("", response_model=list[UsuarioRead]) # Aquí definimos una ruta GET para obtener todos los usuarios, y especificamos que la respuesta será una lista de objetos UsuarioRead.
def listar_usuarios(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superadmin),
):
    return usuario_service.get_usuarios(db)


@router.post("", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED) # Aquí definimos una ruta POST para crear un nuevo usuario, y especificamos que la respuesta será un objeto UsuarioRead y el código de estado será 201 Created.
def crear_usuario(
    usuario_in: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superadmin),
):
    existente = usuario_service.get_usuario_by_email(db, usuario_in.email)
    if existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese email",
        )
    return usuario_service.create_usuario(db, usuario_in)

@router.put("/{email}", response_model=UsuarioRead) # Aquí definimos una ruta PUT para actualizar un usuario existente por su email, y especificamos que la respuesta será un objeto UsuarioRead. Esta ruta permite actualizar los campos de un usuario, como su nombre, rol o estado activo, pero no permite cambiar el email del usuario, ya que el email se usa como identificador único para buscar al usuario en la base de datos.
def actualizar_usuario(
    email: str,
    usuario_in: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superadmin),
):
    usuario = usuario_service.get_usuario_by_email(db, email)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario_service.update_usuario(db, usuario, usuario_in)


@router.delete("/{email}", response_model=UsuarioRead) # Aquí definimos una ruta DELETE para desactivar un usuario por su email, y especificamos que la respuesta será un objeto UsuarioRead. En lugar de eliminar el usuario de la base de datos, esta ruta marcará al usuario como inactivo para mantener un registro de los usuarios desactivados.
def desactivar_usuario(
    email: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_superadmin),
):
    if email == current_user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes desactivar tu propia cuenta",
        )
    usuario = usuario_service.get_usuario_by_email(db, email)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return usuario_service.desactivar_usuario(db, usuario)