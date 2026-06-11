from app import app
from models.database import db
from sqlalchemy import text

with app.app_context():
    with open('scriptbd/migracion_rbac.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # Executing the SQL file
    try:
        db.session.execute(text(sql))
        db.session.commit()
        print("Migración completada con éxito.")
    except Exception as e:
        db.session.rollback()
        print("Error en migración:", e)
