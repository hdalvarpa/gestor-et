from models.database import db

class EntidadTecnica(db.Model):
    __tablename__ = 'entidades_tecnicas'
    
    id_entidad_tecnica = db.Column(db.Integer, primary_key=True)
    ruc = db.Column(db.String(11), unique=True, nullable=False)
    razon_social = db.Column(db.String(150), nullable=False)
    direccion = db.Column(db.String(255))
    id_representante_legal = db.Column(db.Integer, db.ForeignKey('personas.id_persona'), nullable=False)
    
    # Relationships
    representante_legal = db.relationship('Persona', backref=db.backref('entidades_representadas', lazy=True))
    registros = db.relationship('RegistroET', backref='entidad_tecnica', cascade="all, delete-orphan")
    asignaciones_ingenieros = db.relationship('AsignacionIngeniero', backref='entidad_tecnica', cascade="all, delete-orphan", order_by="desc(AsignacionIngeniero.id_asignacion)")

    @property
    def ingeniero_actual(self):
        # Devuelve el objeto AsignacionIngeniero vigente (o el objeto Ingeniero directamente, lo que sea más fácil)
        # Vamos a devolver el objeto Ingeniero, o None si no tiene asignación vigente
        for asig in self.asignaciones_ingenieros:
            if asig.estado == 'VIGENTE':
                return asig.ingeniero
        return None
    
    def __repr__(self):
        return f'<EntidadTecnica {self.razon_social}>'
