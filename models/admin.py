from models.database import db

class Admin(db.Model):
    __tablename__ = 'admin'
    
    id = db.Column('id_admin', db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    correo_electronico = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column('contrasena_hash', db.String(255), nullable=False)
    estado = db.Column(db.String(20), default='ACTIVO', nullable=False)
    
    def __repr__(self):
        return f'<Admin {self.username}>'
