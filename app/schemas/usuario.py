from pydantic import BaseModel, EmailStr, ConfigDict # Importamos BaseModel para crear modelos de datos, EmailStr para validar que el campo email sea una dirección de correo electrónico válida, y ConfigDict para configurar los modelos.


class UsuarioBase(BaseModel): # esta clase es la base para los esquemas de usuario, y define los campos comunes que se van a usar en los diferentes esquemas de usuario.
    email: EmailStr
    nombre: str


class UsuarioCreate(UsuarioBase): # esta clase hereda de UsuarioBase y se usa para crear un nuevo usuario, tiene un campo adicional password que es necesario para crear un usuario, y un campo rol que tiene un valor por defecto de "editor".
    password: str
    rol: str = "editor"


class UsuarioRead(UsuarioBase): # esta clase hereda de UsuarioBase y se usa para leer un usuario existente, tiene campos adicionales id, rol y activo que son necesarios para mostrar la información del usuario, pero no se incluyen en el esquema de creación porque se generan automáticamente o tienen valores por defecto.
    id: int
    rol: str
    activo: bool

    model_config = ConfigDict(from_attributes=True)


class UsuarioLogin(BaseModel): # esta clase se usa para el esquema de login, y solo tiene los campos email y password que son necesarios para autenticar a un usuario.
    email: EmailStr
    password: str

class UsuarioUpdate(BaseModel): # esta clase se usa para el esquema de actualización de usuario, y tiene campos opcionales que se pueden actualizar, como email, nombre, rol y activo. Estos campos son opcionales porque no es necesario actualizar todos los campos de un usuario, solo los que se quieran cambiar.
    nombre: str | None = None
    rol: str | None = None
    activo: bool | None = None