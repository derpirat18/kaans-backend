from fastapi import Depends, HTTPException, status # Importamos las herramientas necesarias de FastAPI para manejar dependencias, lanzar excepciones HTTP y definir códigos de estado.
from fastapi.security import OAuth2PasswordBearer # Importamos OAuth2PasswordBearer para manejar la autenticación basada en tokens JWT, que se usará para proteger las rutas que requieren autenticación.
from sqlalchemy.orm import Session # Importamos la clase Session de SQLAlchemy para manejar las sesiones de base de datos.

from app.db.session import get_db  # Importamos la función get_db que definimos en session.py para obtener una sesión de base de datos, que se usará como dependencia en las rutas que requieren acceso a la base de datos.
from app.core.security import decode_access_token # Importamos la función decode_access_token que definimos en security.py para decodificar los tokens de acceso JWT y obtener la información del usuario autenticado, que se usará para proteger las rutas y obtener el usuario actual.
from app.services import usuario_service # Importamos el módulo de servicios de usuario que definimos en usuario_service.py para manejar la lógica de negocio relacionada con los usuarios, como la autenticación y creación de usuarios, que se usará para obtener el usuario actual a partir del token de acceso.
from app.models.usuario import Usuario # Importamos el modelo Usuario que definimos en usuario.py para representar a los usuarios en la base de datos, que se usará como tipo de retorno en la función get_current_user.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login") # Aquí creamos una instancia de OAuth2PasswordBearer que se usará para manejar la autenticación basada en tokens JWT. El parámetro tokenUrl indica la URL del endpoint de login donde los usuarios pueden obtener un token de acceso enviando sus credenciales. FastAPI se encargará de extraer el token de acceso de las solicitudes que lo requieran y pasarlo a las funciones que lo necesiten como una dependencia.


def get_current_user( # esta función se encargará de obtener el usuario actual a partir del token de acceso JWT que se envía en las solicitudes. Se usará como una dependencia en las rutas que requieren autenticación para obtener la información del usuario autenticado.
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autenticado o token invalido",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token) # Aquí llamamos a la función decode_access_token para decodificar el token de acceso JWT y obtener la información del usuario autenticado. Si el token es inválido o ha expirado, esta función lanzará una excepción HTTP 401 Unauthorized con un mensaje de error y un encabezado WWW-Authenticate para indicar que se requiere autenticación.
    if payload is None:
        raise credenciales_invalidas

    email = payload.get("sub")
    if email is None:
        raise credenciales_invalidas

    usuario = usuario_service.get_usuario_by_email(db, email)
    if usuario is None:
        raise credenciales_invalidas

    return usuario