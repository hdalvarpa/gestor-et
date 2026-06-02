from models.database import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column('id_usuario', db.Integer, primary_key=True)
    id_persona = db.Column(db.Integer, nullable=False, default=1)
    username = db.Column(db.String(50), unique=True, nullable=False)
    correo_electronico = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column('contrasena_hash', db.String(255), nullable=False)
    
    # Relación con la tabla Personas
    persona = db.relationship('Persona', backref='usuario', lazy=True, primaryjoin="Usuario.id_persona == Persona.id_persona", foreign_keys=[id_persona])
    
    def __repr__(self):
        return f'<Usuario {self.username}>'
