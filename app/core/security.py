from datetime import datetime, timedelta, timezone # Importamos las clases necesarias para manejar fechas y tiempos, especialmente para la creación y validación de tokens JWT.
import jwt # Importamos la librería PyJWT para crear y verificar tokens JWT.

from pwdlib import PasswordHash # Importamos PasswordHash de pwdlib para manejar el hashing de contraseñas de manera segura.
from app.core.config import settings # Importamos la configuración para acceder a las variables de configuración como SECRET_KEY, ALGORITHM y ACCESS_TOKEN_EXPIRE_MINUTES.

password_hash = PasswordHash.recommended() # Creamos una instancia de PasswordHash que usaremos para hashear y verificar contraseñas.

def hash_password(password: str) -> str: 
    return password_hash.hash(password) # Esta función toma una contraseña en texto plano y devuelve su hash seguro usando pwdlib.

def verify_password(plain_password: str, hashed_password: str) -> bool: # Esta función toma una contraseña en texto plano y un hash de contraseña, y verifica si la contraseña coincide con el hash usando pwdlib.
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str: # Esta función toma un diccionario de datos (que generalmente incluirá información del usuario) y crea un token JWT que incluye esos datos y una fecha de expiración.
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict | None: # Esta función toma un token JWT y lo decodifica para obtener los datos que contiene. Si el token es válido, devuelve los datos; si no, devuelve None.
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        return None