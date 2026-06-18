from models.database import db
from datetime import datetime

class FichaInscripcion(db.Model):
    __tablename__ = 'fichas_inscripcion'

    id_ficha = db.Column(db.Integer, primary_key=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Entidad Técnica a cargo
    id_entidad_tecnica = db.Column(db.Integer, db.ForeignKey('entidades_tecnicas.id_entidad_tecnica'), nullable=False)

    # 6. Contacto directo (se puede quedar en la ficha principal por ser metadato general)
    correo_contacto = db.Column(db.String(150))
    telefono_contacto = db.Column(db.String(50))

    # Relaciones 1 a 1 (usando uselist=False)
    predio = db.relationship('FichaPredio', backref='ficha', uselist=False, cascade='all, delete-orphan')
    jefe = db.relationship('FichaJefe', backref='ficha', uselist=False, cascade='all, delete-orphan')
    conyuge = db.relationship('FichaConyuge', backref='ficha', uselist=False, cascade='all, delete-orphan')
    
    # Nuevas Relaciones de la Matriz (Constatacin e Informe Tcnico)
    constatacion = db.relationship('Constatacion', backref='ficha_rel', uselist=False, cascade='all, delete-orphan')
    informe = db.relationship('InformeTecnico', backref='ficha_rel', uselist=False, cascade='all, delete-orphan')
    
    # Relaciones 1 a N
    cargas = db.relationship('FichaCarga', backref='ficha', cascade='all, delete-orphan')
    adicionales = db.relationship('FichaAdicional', backref='ficha', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<FichaInscripcion {self.id_ficha}>'
