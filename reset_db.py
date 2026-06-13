from app import app
from models.database import db

def recrear_base_de_datos():
    with app.app_context():
        print("Borrando todas las tablas...")
        try:
            db.drop_all()
            print("Tablas conocidas por SQLAlchemy borradas con éxito.")
        except Exception as e:
            print(f"Advertencia al borrar con drop_all: {e}")
            
        print("Borrando tablas huérfanas mediante SQL directo...")
        try:
            from sqlalchemy import text
            # Cascading en PostgreSQL borrará las dependencias, en SQLite simplemente borra.
            db.session.execute(text("DROP TABLE IF EXISTS personas CASCADE;"))
            db.session.execute(text("DROP TABLE IF EXISTS expediente_grupo_familiar CASCADE;"))
            db.session.execute(text("DROP TABLE IF EXISTS grupo_familiar CASCADE;"))
            # En caso de SQLite (donde CASCADE no existe con drop table)
            # si falla lo ignoramos o intentamos sin cascade
            db.session.commit()
            print("Tablas huérfanas eliminadas exitosamente.")
        except Exception as e:
            db.session.rollback()
            try:
                # Fallback para SQLite
                db.session.execute(text("DROP TABLE IF EXISTS personas;"))
                db.session.execute(text("DROP TABLE IF EXISTS expediente_grupo_familiar;"))
                db.session.execute(text("DROP TABLE IF EXISTS grupo_familiar;"))
                db.session.commit()
                print("Tablas huérfanas eliminadas (modo SQLite).")
            except Exception as e2:
                print(f"Advertencia al borrar tablas huérfanas: {e2}")
        
        print("Creando nuevas tablas con la estructura actualizada...")
        db.create_all()
        
        print("Creando usuario administrador por defecto...")
        from models.usuario import Usuario
        from werkzeug.security import generate_password_hash
        
        # Crear usuario por defecto 'admin' con clave 'admin' si no existe
        if not Usuario.query.filter_by(username='admin').first():
            admin_user = Usuario(
                username='admin',
                correo_electronico='admin@admin.com',
                password_hash=generate_password_hash('4dm1n1str4d0r')
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Usuario 'admin' con contraseña '4dm1n1str4d0r' ha sido creado.")
            
        print("¡Base de datos regenerada exitosamente!")

if __name__ == '__main__':
    # ADVERTENCIA: ESTO BORRARÁ TODOS LOS DATOS
    recrear_base_de_datos()
