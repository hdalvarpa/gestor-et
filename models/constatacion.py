from models.database import db
from datetime import datetime

class Constatacion(db.Model):
    __tablename__ = 'constataciones'
    
    id_constatacion = db.Column(db.Integer, primary_key=True)
    id_ficha = db.Column(db.Integer, db.ForeignKey('fichas_inscripcion.id_ficha', ondelete='CASCADE'), nullable=False, unique=True)
    tiene_agua = db.Column(db.Boolean, default=False)
    tiene_saneamiento = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Constatacion Ficha {self.id_ficha}>'
