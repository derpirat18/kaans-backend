from sqlalchemy.orm import Session # importamos la clase Session de SQLAlchemy para interactuar con la base de datos.

from app.models.usuario import Usuario # importamos el modelo Usuario para poder usarlo en nuestras funciones de servicio.
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate # importamos el esquema de Pydantic para validar los datos de entrada en nuestras funciones de servicio.
from app.core.security import hash_password, verify_password # importamos las funciones de seguridad para hashear y verificar contraseñas, que se encuentran en el módulo security.py dentro del paquete core.


def get_usuario_by_email(db: Session, email: str) -> Usuario | None: # esta función recibe una sesión de base de datos y un email, y devuelve un usuario o None si no se encuentra.
    return db.query(Usuario).filter(Usuario.email == email).first()


def create_usuario(db: Session, usuario_in: UsuarioCreate) -> Usuario: # esta función recibe una sesión de base de datos y un objeto UsuarioCreate, y devuelve el usuario creado.
    nuevo_usuario = Usuario(
        email=usuario_in.email,
        nombre=usuario_in.nombre,
        hashed_password=hash_password(usuario_in.password),
        rol=usuario_in.rol,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def authenticate_usuario(db: Session, email: str, password: str) -> Usuario | None: # esta función recibe una sesión de base de datos y un email y contraseña, y devuelve un usuario o None si las credenciales son inválidas.

    usuario = get_usuario_by_email(db, email)
    if usuario is None:
        return None
    if not verify_password(password, usuario.hashed_password):
        return None
    return usuario

def get_usuarios(db: Session) -> list[Usuario]: # esta función recibe una sesión de base de datos y devuelve una lista de usuarios.
    return db.query(Usuario).all()


def desactivar_usuario(db: Session, usuario: Usuario) -> Usuario: # esta función recibe una sesión de base de datos y un usuario existente, y devuelve el usuario desactivado. En lugar de eliminar el usuario de la base de datos, simplemente marcamos su campo "activo" como False para indicar que ya no está activo en la aplicación.
    usuario.activo = False
    db.commit()
    db.refresh(usuario)
    return usuario

def update_usuario(db: Session, usuario: Usuario, usuario_in: UsuarioUpdate) -> Usuario: # esta función recibe una sesión de base de datos, un usuario existente y un objeto UsuarioUpdate con los campos a actualizar, y devuelve el usuario actualizado. Primero convertimos el objeto UsuarioUpdate en un diccionario, excluyendo los campos que no se han establecido (exclude_unset=True), y luego iteramos sobre los campos y valores del diccionario para actualizar el usuario existente usando setattr. Finalmente, guardamos los cambios en la base de datos y refrescamos el usuario para obtener los datos actualizados.
    datos = usuario_in.model_dump(exclude_unset=True)
    for campo, valor in datos.items():
        setattr(usuario, campo, valor)
    db.commit()
    db.refresh(usuario)
    return usuario