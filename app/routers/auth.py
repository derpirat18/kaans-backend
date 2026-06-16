from fastapi import APIRouter, Depends, HTTPException, status # Importamos las herramientas necesarias de FastAPI para crear rutas, manejar dependencias, lanzar excepciones HTTP y definir códigos de estado.
from fastapi.security import OAuth2PasswordRequestForm # Importamos OAuth2PasswordRequestForm para manejar el formulario de autenticación que se envía al endpoint de login, que incluye el nombre de usuario (email) y la contraseña.
from sqlalchemy.orm import Session # Importamos la clase Session de SQLAlchemy para manejar las sesiones de base de datos.

from app.db.session import get_db # Importamos la función get_db que definimos en session.py para obtener una sesión de base de datos.
from app.services import usuario_service # Importamos el módulo de servicios de usuario que definimos en usuario_service.py para manejar la lógica de negocio relacionada con los usuarios, como la autenticación y creación de usuarios.
from app.core.security import create_access_token # Importamos la función create_access_token que definimos en security.py para crear tokens de acceso JWT, que se usarán para autenticar a los usuarios después de que inicien sesión correctamente.

router = APIRouter(prefix="/api/auth", tags=["auth"]) # Aquí creamos un router de FastAPI con el prefijo "/api/auth" para agrupar todas las rutas relacionadas con la autenticación, y le asignamos la etiqueta "auth" para documentarlas en la API.


@router.post("/login") # Aquí definimos una ruta POST para el login, que se ejecutará cuando alguien haga una solicitud POST a "/api/auth/login". Esta ruta se encargará de autenticar a los usuarios y devolver un token de acceso si las credenciales son válidas.
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), # Aquí usamos Depends() para indicar que esta función depende de un formulario de autenticación que se envía en la solicitud, y FastAPI se encargará de extraer los datos del formulario (username y password) y pasarlos a esta función como un objeto form_data.
    db: Session = Depends(get_db), 
):
    usuario = usuario_service.authenticate_usuario(
        db, email=form_data.username, password=form_data.password
    )
    if usuario is None: # Si la función authenticate_usuario devuelve None, significa que las credenciales son inválidas, por lo que lanzamos una excepción HTTP 401 Unauthorized con un mensaje de error y un encabezado WWW-Authenticate para indicar que se requiere autenticación.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": usuario.email, "rol": usuario.rol}) # Si las credenciales son válidas, llamamos a la función create_access_token para crear un token de acceso JWT que incluye el email del usuario como el sujeto (sub) y su rol como parte de los datos del token. Este token se usará para autenticar al usuario en las solicitudes futuras.
    return {"access_token": access_token, "token_type": "bearer"}