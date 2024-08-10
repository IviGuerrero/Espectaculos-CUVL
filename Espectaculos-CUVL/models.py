from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Espectaculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(300), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    sala = db.Column(db.String(100), nullable=False)

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    espectaculo_id = db.Column(db.Integer, db.ForeignKey('espectaculo.id'), nullable=False)
    fecha_reserva = db.Column(db.DateTime, nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('reservas', lazy=True))
    espectaculo = db.relationship('Espectaculo', backref=db.backref('reservas', lazy=True))