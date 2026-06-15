from sqlalchemy import create_engine # importamos la función que crea el "motor": la conexión real y física a la base de datos

# importamos sessionmaker, que es una función que nos ayuda a crear sesiones para interactuar con la base de datos,
# # y declarative_base, que es una función que nos ayuda a definir nuestras tablas como clases de Python.
from sqlalchemy.orm import sessionmaker, declarative_base 

from app.core.config import settings # importamos la configuración que definimos en config.py para obtener la URL de la base de datos.

engine = create_engine(
    settings.DATABASE_URL, # aquí usamos la URL de la base de datos que definimos en la configuración.
    connect_args={"check_same_thread": False}   # esta opción es necesaria para SQLite para permitir conexiones desde múltiples hilos. 
                                                # nota al migrar a otra base de datos, esta opción no es necesaria. y tenemos que eliminarla.
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)    # aquí creamos una fábrica de sesiones que se conectará a la base de datos 
                                                                                # usando el motor que acabamos de crear.
Base = declarative_base()   # aquí creamos una clase base para nuestras tablas, lo que nos permitirá definir nuestras tablas como clases de Python.

def get_db():
    db = SessionLocal()   # aquí creamos una nueva sesión de base de datos usando la fábrica que definimos antes.
    try:
        yield db  # esta función es un generador que devuelve la sesión de base de datos. 
                   # Esto es útil para usarlo como una dependencia en FastAPI, lo que nos permitirá obtener una sesión de base de datos en nuestras rutas y asegurarnos de que se
                   # cierre correctamente después de usarla.
    finally:
        db.close() # aquí nos aseguramos de cerrar la sesión de base de datos después de usarla, para liberar los recursos.