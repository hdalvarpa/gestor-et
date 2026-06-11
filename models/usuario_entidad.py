from models.database import db

# Tabla de asociación (Muchos a Muchos) entre Usuarios y Entidades Técnicas
usuarios_entidades = db.Table('usuarios_entidades',
    db.Column('id_usuario', db.Integer, db.ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), primary_key=True),
    db.Column('id_entidad_tecnica', db.Integer, db.ForeignKey('entidades_tecnicas.id_entidad_tecnica', ondelete='CASCADE'), primary_key=True),
    db.Column('fecha_asignacion', db.DateTime, default=db.func.current_timestamp())
)
