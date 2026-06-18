from models.database import db

class InformeTecnico(db.Model):
    __tablename__ = 'informes_tecnicos'
    
    id_informe = db.Column(db.Integer, primary_key=True)
    id_ficha = db.Column(db.Integer, db.ForeignKey('fichas_inscripcion.id_ficha', ondelete='CASCADE'), nullable=False, unique=True)
    
    medida_frente = db.Column(db.Float)
    colindante_frente = db.Column(db.String(150))
    
    medida_derecha = db.Column(db.Float)
    colindante_derecha = db.Column(db.String(150))
    
    medida_izquierda = db.Column(db.Float)
    colindante_izquierda = db.Column(db.String(150))
    
    medida_fondo = db.Column(db.Float)
    colindante_fondo = db.Column(db.String(150))
    
    area_terreno = db.Column(db.Float)
    descripcion = db.Column(db.Text)
    
    def __repr__(self):
        return f'<InformeTecnico Ficha {self.id_ficha}>'
