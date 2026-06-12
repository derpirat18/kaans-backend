from fastapi import FastAPI
# Importamos la clase FastAPI desde la librería que instalaste. 
# Es el "molde" con el que se construye una aplicación. 
# Importar es traer una herramienta de su caja para usarla aquí.

app = FastAPI(title="Kaans API", description="Sera nuestra API de Kaans", version="1.0.0")
# Creamos una instancia de la clase FastAPI y la asignamos a la variable "app". 
# Esta variable es lo que usaremos para definir nuestras rutas y manejar las solicitudes.
# Es como crear un nuevo proyecto o aplicación usando el molde que importamos.

@app.get("/health")
# Decorador que indica que esta función manejará las solicitudes GET a la ruta "/health".

def health_check():
# Esta función se ejecutará cuando alguien haga una solicitud GET a "/health".
    return {"status": "ok"}
# La función devuelve un diccionario con el estado "Ok".
# Esto es útil para verificar que la API está funcionando correctamente.