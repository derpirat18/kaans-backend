from app.db.session import SessionLocal # importamos la clase SessionLocal que definimos en session.py para crear una sesión de base de datos y poder interactuar con ella.
from app.schemas.usuario import UsuarioCreate # importamos el esquema de Pydantic para validar los datos de entrada al crear un nuevo usuario, que se encuentra en el módulo usuario.py dentro del paquete schemas.
from app.services import usuario_service # importamos el módulo de servicios de usuario que definimos en usuario_service.py para manejar la lógica de negocio relacionada con los usuarios, como la autenticación y creación de usuarios.

EMAIL_ADMIN = "admin@kaans.mx"
NOMBRE_ADMIN = "Super Admin"
PASSWORD_ADMIN = "CambiaEstaPassword123"


def crear_superadmin(): # esta función se encarga de crear un superadmin en la base de datos si no existe uno con el mismo email. Se puede ejecutar este script manualmente para asegurarse de que siempre haya un superadmin disponible para administrar la aplicación.
    db = SessionLocal()
    try:
        existente = usuario_service.get_usuario_by_email(db, EMAIL_ADMIN)
        if existente is not None:
            print(f"Ya existe un usuario con el email {EMAIL_ADMIN}. No se hace nada.")
            return

        admin_in = UsuarioCreate(
            email=EMAIL_ADMIN,
            nombre=NOMBRE_ADMIN,
            password=PASSWORD_ADMIN,
            rol="superadmin",
        )
        admin = usuario_service.create_usuario(db, admin_in)
        print(f"Superadmin creado correctamente: {admin.email} (rol: {admin.rol})")
    finally:
        db.close()


if __name__ == "__main__":
    crear_superadmin()