from models.database import db

class FichaJefe(db.Model):
    __tablename__ = 'fichas_jefe'

    id_jefe = db.Column(db.Integer, primary_key=True)
    id_ficha = db.Column(db.Integer, db.ForeignKey('fichas_inscripcion.id_ficha', ondelete='CASCADE'), nullable=False, unique=True)

    nombres = db.Column(db.String(100))
    ap_paterno = db.Column(db.String(50))
    ap_materno = db.Column(db.String(50))
    dni = db.Column(db.String(20))
    nacimiento = db.Column(db.String(20))
    estado_civil = db.Column(db.String(20))
    grado_instruccion = db.Column(db.String(100))
    ocupacion = db.Column(db.String(100))
    discapacidad = db.Column(db.String(50))
    sit_laboral = db.Column(db.String(50))
    condicion_eco = db.Column(db.String(50))
    ingreso_mensual = db.Column(db.String(20))

    def __repr__(self):
        return f'<FichaJefe {self.dni}>'
