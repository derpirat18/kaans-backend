from pydantic import BaseModel, ConfigDict # Importamos BaseModel para crear un modelo de datos y ConfigDict para configurar el modelo.

#schema 1 curso base con los campos que se van a usar para crear un nuevo curso, sin el id que se genera automáticamente.

class CursoBase(BaseModel):
    slug: str # el slug es un identificador único para cada curso, que se genera a partir del título y se usa en la URL para acceder al curso.
    titulo: str
    categoria: str
    descripcion: str | None = None # la descripción es opcional, por eso se define como str | None y se le asigna un valor por defecto de None.
    duracion_horas: int | None = None # la duración en horas también es opcional, por eso se define como int | None y se le asigna un valor por defecto de None.
    nivel: str | None = None # el nivel del curso también es opcional, por eso se define como str | None y se le asigna un valor por defecto de None.
    modalidad: str | None = None # la modalidad del curso también es opcional, por eso se define como str | None y se le asigna un valor por defecto de None.

# schema 2 CursoCreate que hereda de CursoBase, y se usa para crear un nuevo curso, no tiene campos adicionales por ahora pero se puede extender en el futuro si es necesario.
class CursoCreate(CursoBase):
    pass

# schema 3 CursoUpdate que hereda de BaseModel, y se usa para actualizar un curso existente, todos los campos son opcionales para permitir actualizaciones parciales.
class CursoUpdate(BaseModel):
    slug: str | None = None # el slug también es opcional en la actualización, para permitir que no se cambie si no se proporciona uno nuevo.
    titulo: str | None = None # el título también es opcional en la actualización, para permitir que no se cambie si no se proporciona uno nuevo.
    categoria: str | None = None # la categoría también es opcional en la actualización, para permitir que no se cambie si no se proporciona una nueva.
    descripcion: str | None = None # la descripción también es opcional en la actualización, para permitir que no se cambie si no se proporciona una nueva.
    duracion_horas: int | None = None # la duración en horas también es opcional en la actualización, para permitir que no se cambie si no se proporciona una nueva.
    nivel: str | None = None # el nivel también es opcional en la actualización, para permitir que no se cambie si no se proporciona uno nuevo.
    modalidad: str | None = None # la modalidad también es opcional en la actualización, para permitir que no se cambie si no se proporciona una nueva.

# schema 4 CursoRead que hereda de CursoBase, y se usa para leer un curso existente, tiene un campo adicional id que es el identificador único del curso en la base de datos.
class CursoRead(CursoBase): 
    id: int # el id es un entero que se genera automáticamente en la base de datos y se usa para identificar de manera única cada curso.

    model_config = ConfigDict(from_attributes=True) # esta configuración le dice a Pydantic que al crear una instancia de este modelo a partir de un objeto (como una instancia de SQLAlchemy), 
                                                    # tome los valores de los atributos del objeto en lugar de esperar un diccionario con los mismos nombres.