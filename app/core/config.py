# Importamos dos herramientas de la librería: 
# BaseSettings (el "molde" para crear configuraciones que pueden leerse del entorno) 
# y SettingsConfigDict (la que le dice de dónde leer, como el archivo .env).
from pydantic_settings import BaseSettings, SettingsConfigDict 

from pathlib import Path # Importamos Path para manejar rutas de archivos de manera más fácil y compatible con diferentes sistemas operativos.

class Settings(BaseSettings): # Esta clase es donde definimos todas las variables de configuración que nuestra aplicación va a usar.

    # Estas variables son parte de la configuración de nuestra aplicación.
    # Aquí definimos dos variables de configuración: project_name y api_version, con valores por defecto.
    PROJECT_NAME: str = "Kaans API"
    API_VERSION: str = "1.0.0"
    
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173"] # Lista de orígenes permitidos para CORS, en este caso solo el frontend local (http://localhost:5173).

    DATABASE_URL: str = "sqlite:///./kaans.db" # URL de conexión a la base de datos, en este caso una base de datos SQLite llamada kaans.db.

    SECRET_KEY: str #
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
    )   # Esta configuración le dice a Pydantic que lea las variables de entorno desde un archivo 
        # .env ubicado en la raíz del proyecto (tres niveles arriba de este archivo), y que el archivo esté codificado en UTF-8.       
settings = Settings()   # Aquí creamos una instancia de la clase Settings, 
                        # lo que hace que se lean las variables de configuración y estén disponibles para usar en toda la aplicación.
