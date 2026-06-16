# Importamos la clase FastAPI desde la librería que instalaste. 
# Es el "molde" con el que se construye una aplicación. 
# Importar es traer una herramienta de su caja para usarla aquí.
from fastapi import FastAPI

# Importamos el middleware de CORS (Cross-Origin Resource Sharing) que nos ayudará a manejar
# las solicitudes de diferentes orígenes, como el frontend que podría estar en localhost:5173.
from fastapi.middleware.cors import CORSMiddleware

# Importamos la configuración que definimos en el archivo config.py.
from app.core.config import settings

from app.routers import cursos, auth  # Importamos el router de cursos que definimos en routers/cursos.py para incluirlo en nuestra aplicación.


# Aquí estamos creando una instancia de FastAPI y configurándola con el nombre 
# del proyecto y la versión que definimos en settings.
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # Permitimos los orígenes definidos en la configuración.
    allow_credentials=True,  # Permitimos el uso de cookies y credenciales en las solicitudes.
    allow_methods=["*"],  # Permitimos todos los métodos HTTP (GET, POST, etc.).
    allow_headers=["*"],  # Permitimos todos los encabezados en las solicitudes.
)

# Decorador que indica que esta función manejará las solicitudes GET a la ruta "/health".
@app.get("/health")

# Esta función se ejecutará cuando alguien haga una solicitud GET a "/health".
def health_check():
    
    # La función devuelve un diccionario con el estado "Ok".
    # Esto es útil para verificar que la API está funcionando correctamente.
    return {"status": "ok"}

app.include_router(cursos.router) # Aquí incluimos el router de cursos en nuestra aplicación, lo que hace que todas las rutas definidas en ese router estén disponibles en la API.
app.include_router(auth.router) # Aquí incluimos el router de autenticación en nuestra aplicación, lo que hace que todas las rutas definidas en ese router estén disponibles en la API.