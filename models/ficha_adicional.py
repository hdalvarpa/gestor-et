from models.database import db

class FichaAdicional(db.Model):
    __tablename__ = 'fichas_adicionales'

    id_adicional = db.Column(db.Integer, primary_key=True)
    id_ficha = db.Column(db.Integer, db.ForeignKey('fichas_inscripcion.id_ficha', ondelete='CASCADE'), nullable=False)

    nombres = db.Column(db.String(100))
    ap_paterno = db.Column(db.String(50))
    ap_materno = db.Column(db.String(50))
    dni = db.Column(db.String(20))
    vinculo = db.Column(db.String(50))

    def __repr__(self):
        return f'<FichaAdicional {self.dni}>'
