from models.database import db

roles_permisos = db.Table('roles_permisos',
    db.Column('id_rol', db.Integer, db.ForeignKey('roles.id_rol', ondelete='CASCADE'), primary_key=True),
    db.Column('id_permiso', db.Integer, db.ForeignKey('permisos.id_permiso', ondelete='CASCADE'), primary_key=True)
)
