from models.database import db

class Ingeniero(db.Model):
    __tablename__ = 'ingenieros'
    
    id_ingeniero = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(20), nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=True)
    apellido_materno = db.Column(db.String(100), nullable=True)
    cip = db.Column(db.String(20), unique=True, nullable=False)
    
    # Relationships
    
    def __repr__(self):
        return f'<Ingeniero CIP:{self.cip}>'
