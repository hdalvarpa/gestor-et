from models.database import db

class EntidadTecnica(db.Model):
    __tablename__ = 'entidades_tecnicas'
    
    id_entidad_tecnica = db.Column(db.Integer, primary_key=True)
    ruc = db.Column(db.String(11), unique=True, nullable=False)
    razon_social = db.Column(db.String(150), nullable=False)
    direccion = db.Column(db.String(255))
    rep_dni = db.Column(db.String(20), nullable=False)
    rep_nombres = db.Column(db.String(100), nullable=False)
    rep_apellido_paterno = db.Column(db.String(100), nullable=True)
    rep_apellido_materno = db.Column(db.String(100), nullable=True)
    
    id_ingeniero_vigente = db.Column(db.Integer, db.ForeignKey('ingenieros.id_ingeniero'), nullable=True)
    
    # Relationships
    registros = db.relationship('RegistroET', backref='entidad_tecnica', cascade="all, delete-orphan")
    fichas = db.relationship('FichaInscripcion', backref='entidad_tecnica', cascade="all, delete-orphan")
    ingeniero_vigente = db.relationship('Ingeniero', foreign_keys=[id_ingeniero_vigente])

    @property
    def ingeniero_actual(self):
        return self.ingeniero_vigente
    
    def __repr__(self):
        return f'<EntidadTecnica {self.razon_social}>'
