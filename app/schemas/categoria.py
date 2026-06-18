from pydantic import BaseModel, ConfigDict # Importamos BaseModel para crear modelos de datos y ConfigDict para configurar los modelos.


class CategoriaBase(BaseModel): # esta clase es la base para los esquemas de categoría, y define los campos comunes que se van a usar en los diferentes esquemas de categoría.
    nombre: str
    descripcion: str | None = None
    color: str | None = None


class CategoriaCreate(CategoriaBase): # esta clase hereda de CategoriaBase y se usa para crear una nueva categoría, no tiene campos adicionales porque todos los campos necesarios para crear una categoría ya están definidos en la clase base CategoriaBase.
    pass


class CategoriaUpdate(BaseModel): # esta clase se usa para el esquema de actualización de categoría, y tiene campos opcionales que se pueden actualizar, como nombre, descripcion y color. Estos campos son opcionales porque no es necesario actualizar todos los campos de una categoría, solo los que se quieran cambiar.
    nombre: str | None = None
    descripcion: str | None = None
    color: str | None = None


class CategoriaRead(CategoriaBase): # esta clase hereda de CategoriaBase y se usa para leer una categoría existente, tiene un campo adicional id que es necesario para mostrar la información de la categoría, pero no se incluye en el esquema de creación porque se genera automáticamente.
    id: int

    model_config = ConfigDict(from_attributes=True)