# Importamos dos herramientas de la librería: 
# BaseSettings (el "molde" para crear configuraciones que pueden leerse del entorno) 
# y SettingsConfigDict (la que le dice de dónde leer, como el archivo .env).
from pydantic_settings import BaseSettings, SettingsConfigDict

# Creamos una clase llamada Settings que hereda de BaseSettings.
class Settings(BaseSettings):

    # Estas variables son parte de la configuración de nuestra aplicación.
    # Aquí definimos dos variables de configuración: project_name y api_version, con valores por defecto.
    PROJECT_NAME: str = "Kaans API"
    API_VERSION: str = "1.0.0"
    
    # Esta variable es una lista de orígenes permitidos para CORS (Cross-Origin Resource Sharing).
    # Esto es importante para permitir que el frontend (que podría estar en localhost:5173) 
    # se comunique con esta API sin problemas de seguridad.
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    # Aquí le decimos a Pydantic que lea las variables de configuración desde un archivo .env,
    # y que el archivo esté codificado en UTF-8.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Finalmente, creamos una instancia de la clase Settings y la asignamos a la variable "settings".
settings = Settings()
