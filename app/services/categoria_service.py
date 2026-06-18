from sqlalchemy.orm import Session # importamos la clase Session de SQLAlchemy para interactuar con la base de datos.

from app.models.categoria import Categoria # importamos el modelo Categoria para poder usarlo en nuestras funciones de servicio.
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate  # importamos los esquemas de Pydantic para validar los datos de entrada en nuestras funciones de servicio.


def get_categorias(db: Session) -> list[Categoria]: # esta función recibe una sesión de base de datos y devuelve una lista de categorías.
    return db.query(Categoria).all()


def get_categoria_by_id(db: Session, categoria_id: int) -> Categoria | None: # esta función recibe una sesión de base de datos y un ID de categoría, y devuelve una categoría o None si no se encuentra.
    return db.query(Categoria).filter(Categoria.id == categoria_id).first()


def get_categoria_by_nombre(db: Session, nombre: str) -> Categoria | None: # esta función recibe una sesión de base de datos y un nombre de categoría, y devuelve una categoría o None si no se encuentra. Esta función es útil para verificar si ya existe una categoría con el mismo nombre antes de crear una nueva categoría, ya que el nombre de la categoría debe ser único.
    return db.query(Categoria).filter(Categoria.nombre == nombre).first()


def create_categoria(db: Session, categoria_in: CategoriaCreate) -> Categoria: # esta función recibe una sesión de base de datos y un objeto CategoriaCreate, y devuelve la categoría creada. Primero creamos una nueva instancia del modelo Categoria con los datos del objeto CategoriaCreate, luego agregamos la nueva categoría a la sesión de base de datos, guardamos los cambios en la base de datos y finalmente refrescamos la categoría para obtener los datos actualizados, incluyendo el ID generado automáticamente.
    nueva_categoria = Categoria(
        nombre=categoria_in.nombre,
        descripcion=categoria_in.descripcion,
        color=categoria_in.color,
    )
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return nueva_categoria


def update_categoria(db: Session, categoria: Categoria, categoria_in: CategoriaUpdate) -> Categoria: # esta función recibe una sesión de base de datos, una categoría existente y un objeto CategoriaUpdate con los campos a actualizar, y devuelve la categoría actualizada. Primero convertimos el objeto CategoriaUpdate en un diccionario, excluyendo los campos que no se han establecido (exclude_unset=True), y luego iteramos sobre los campos y valores del diccionario para actualizar la categoría existente usando setattr. Finalmente, guardamos los cambios en la base de datos y refrescamos la categoría para obtener los datos actualizados.
    datos = categoria_in.model_dump(exclude_unset=True)
    for campo, valor in datos.items():
        setattr(categoria, campo, valor)
    db.commit()
    db.refresh(categoria)
    return categoria


def delete_categoria(db: Session, categoria: Categoria) -> None: # esta función recibe una sesión de base de datos y una categoría existente, y no devuelve nada. Esta función elimina la categoría de la base de datos usando db.delete() y luego guarda los cambios en la base de datos con db.commit(). Ten en cuenta que esta función eliminará completamente la categoría de la base de datos, por lo que si quieres mantener un registro de las categorías eliminadas, podrías considerar agregar un campo "activo" a la categoría y marcarla como inactiva en lugar de eliminarla.
    db.delete(categoria)
    db.commit()