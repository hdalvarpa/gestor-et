from models.database import db

class FichaCarga(db.Model):
    __tablename__ = 'fichas_cargas'

    id_carga = db.Column(db.Integer, primary_key=True)
    id_ficha = db.Column(db.Integer, db.ForeignKey('fichas_inscripcion.id_ficha', ondelete='CASCADE'), nullable=False)

    nombres = db.Column(db.String(150))
    dni = db.Column(db.String(20))
    nacimiento = db.Column(db.String(20))
    vinculo = db.Column(db.String(50))
    instruccion = db.Column(db.String(100))
    discapacidad = db.Column(db.String(50))

    def __repr__(self):
        return f'<FichaCarga {self.dni}>'
