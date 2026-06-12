from models.database import db

class FichaPredio(db.Model):
    __tablename__ = 'fichas_predio'

    id_predio = db.Column(db.Integer, primary_key=True)
    id_ficha = db.Column(db.Integer, db.ForeignKey('fichas_inscripcion.id_ficha', ondelete='CASCADE'), nullable=False, unique=True)

    direccion = db.Column(db.String(255))
    departamento = db.Column(db.String(50))
    provincia = db.Column(db.String(50))
    distrito = db.Column(db.String(50))
    manzana = db.Column(db.String(10))
    lote = db.Column(db.String(10))
    sublote = db.Column(db.String(10))
    centro_poblado = db.Column(db.String(150))
    referencia = db.Column(db.String(255))

    def __repr__(self):
        return f'<FichaPredio {self.direccion}>'
