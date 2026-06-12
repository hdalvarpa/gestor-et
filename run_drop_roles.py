from app import app
from models.database import db
from sqlalchemy import text

def run_migration():
    with app.app_context():
        with open('scriptbd/drop_roles.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
            db.session.execute(text(sql))
            db.session.commit()
            print("Tablas de roles y permisos eliminadas con éxito.")

if __name__ == '__main__':
    run_migration()
