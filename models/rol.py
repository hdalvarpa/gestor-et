from models.database import db
from models.rol_permiso import roles_permisos

class Rol(db.Model):
    __tablename__ = 'roles'
    
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relación con Permisos (Muchos a Muchos)
    permisos = db.relationship('Permiso', secondary=roles_permisos, backref=db.backref('roles', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Rol {self.nombre}>'
