from models.database import db

class Ingeniero(db.Model):
    __tablename__ = 'ingenieros'
    
    id_ingeniero = db.Column(db.Integer, primary_key=True)
    id_persona = db.Column(db.Integer, db.ForeignKey('personas.id_persona'), nullable=False)
    cip = db.Column(db.String(20), unique=True, nullable=False)
    
    # Relationships
    persona = db.relationship('Persona', foreign_keys=[id_persona], backref='ingeniero_profile', lazy=True)
    
    def __repr__(self):
        return f'<Ingeniero CIP:{self.cip}>'
