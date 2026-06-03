from models.database import db

class RegistroET(db.Model):
    __tablename__ = 'registros_et'
    
    id_registro_et = db.Column(db.Integer, primary_key=True)
    id_entidad_tecnica = db.Column(db.Integer, db.ForeignKey('entidades_tecnicas.id_entidad_tecnica'), nullable=True)
    codigo_registro = db.Column(db.String(50), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<RegistroET {self.codigo_registro} - {self.anio}>'
