from pydantic import BaseModel, ConfigDict # Importamos BaseModel para crear modelos de datos y ConfigDict para configurar los modelos.

from app.schemas.tema import TemaRead # Importamos el esquema TemaRead para usarlo en el esquema ModuloRead, ya que un módulo puede tener varios temas asociados.


class ModuloBase(BaseModel): # esta clase es la base para los esquemas de módulo, y define los campos comunes que se van a usar en los diferentes esquemas de módulo. El campo orden tiene un valor por defecto de 0 para que los módulos se ordenen por defecto en el orden en que se crean, pero se puede cambiar si se quiere establecer un orden específico.
    numero: str
    titulo: str
    orden: int = 0


class ModuloCreate(ModuloBase): # esta clase hereda de ModuloBase y se usa para crear un nuevo módulo, no tiene campos adicionales por ahora pero se puede extender en el futuro si es necesario.
    pass


class ModuloRead(ModuloBase): # esta clase hereda de ModuloBase y se usa para leer un módulo existente, tiene un campo adicional id que es el identificador único del módulo en la base de datos, y un campo temas que es una lista de temas asociados al módulo, usando el esquema TemaRead para representar cada tema.
    id: int
    temas: list[TemaRead] = []

    model_config = ConfigDict(from_attributes=True)