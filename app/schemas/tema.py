from pydantic import BaseModel, ConfigDict # Importamos BaseModel para crear modelos de datos y ConfigDict para configurar los modelos.


class TemaBase(BaseModel): # esta clase es la base para los esquemas de tema, y define los campos comunes que se van a usar en los diferentes esquemas de tema. El campo orden tiene un valor por defecto de 0 para que los temas se ordenen por defecto en el orden en que se crean, pero se puede cambiar si se quiere establecer un orden específico.
    texto: str
    orden: int = 0


class TemaCreate(TemaBase): # esta clase hereda de TemaBase y se usa para crear un nuevo tema, no tiene campos adicionales por ahora pero se puede extender en el futuro si es necesario.
    pass


class TemaRead(TemaBase): # esta clase hereda de TemaBase y se usa para leer un tema existente, tiene un campo adicional id que es el identificador único del tema en la base de datos.
    id: int

    model_config = ConfigDict(from_attributes=True) # esta configuración le dice a Pydantic que al crear una instancia de este modelo a partir de un objeto (como una instancia de SQLAlchemy),
                                                    # tome los valores de los atributos del objeto en lugar de esperar un diccionario con los mismos nombres.