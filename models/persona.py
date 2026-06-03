from models.database import db

class Persona(db.Model):
    __tablename__ = 'personas'
    
    id_persona = db.Column(db.Integer, primary_key=True)
    id_tipo_documento = db.Column(db.Integer, nullable=False, default=1) # 1 = DNI
    numero_documento = db.Column(db.String(20), unique=True, nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=True)
    apellido_materno = db.Column(db.String(100), nullable=True)
    fecha_nacimiento = db.Column(db.Date)
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(150))
    direccion_domicilio = db.Column(db.String(255))
    
    # Opcional: relación con Usuario si se necesita navegar de persona a usuario
    # usuarios = db.relationship('Usuario', backref='persona', lazy=True)
    
    def __repr__(self):
        return f'<Persona {self.nombres} {self.apellido_paterno} {self.apellido_materno}>'
