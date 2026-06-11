from models.database import db

class Permiso(db.Model):
    __tablename__ = 'permisos'
    
    id_permiso = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    
    def __repr__(self):
        return f'<Permiso {self.nombre}>'
