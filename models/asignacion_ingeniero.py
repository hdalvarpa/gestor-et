from .database import db
from datetime import datetime

class AsignacionIngeniero(db.Model):
    __tablename__ = 'asignacion_ingenieros'
    
    id_asignacion = db.Column(db.Integer, primary_key=True)
    id_entidad_tecnica = db.Column(db.Integer, db.ForeignKey('entidades_tecnicas.id_entidad_tecnica'), nullable=False)
    id_ingeniero = db.Column(db.Integer, db.ForeignKey('ingenieros.id_ingeniero'), nullable=False)
    estado = db.Column(db.String(20), default='VIGENTE')
    fecha_asignacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones para acceder al objeto completo
    ingeniero = db.relationship('Ingeniero', backref=db.backref('asignaciones', lazy=True))
    
    def __repr__(self):
        return f'<AsignacionIngeniero ET={self.id_entidad_tecnica} ING={self.id_ingeniero} ({self.estado})>'
