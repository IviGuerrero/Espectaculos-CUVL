from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Usuario, Espectaculo, Reserva
from datetime import datetime
from validations import validate_usuario, validate_espectaculo, validate_reserva
from error_handlers import handle_db_error, handle_404_error
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proyecto_final.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def inicio():
    return render_template ('inicio.html')

@app.route('/usuarios')
def usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html')

@app.route('/usuarios/crear', methods=['POST'])
def crear_usuario():
    nombre = request.form['nombre']
    email = request.form['email']
    error = validate_usuario(nombre, email)
    if error:
        flash(error, 'error')
        return redirect(url_for('usuarios'))
    nuevo_usuario = Usuario(nombre=nombre, email=email)
    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario creado exitosamente.', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('El correo ya está registrado.', 'error')
        return redirect(url_for('usuarios'))
    return redirect(url_for('usuarios'))

@app.route('/usuarios/eliminar/<int:id>')
def eliminar_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario is None:
        return handle_404_error(404)  
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuarios'))

@app.route('/espectaculos')
def espectaculos():
    espectaculos = Espectaculo.query.all()
    return render_template('espectaculos.html', espectaculos=espectaculos)

@app.route('/espectaculos/crear', methods=['POST'])
def crear_espectaculo():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']
    sala = request.form['sala']
    try:
        fecha = datetime.strptime(fecha, '%Y-%m-%d')
    except ValueError:
        flash('Formato de fecha incorrecto.', 'error')
        return redirect(url_for('espectaculos'))
    error = validate_espectaculo(nombre, descripcion, fecha, sala)
    if error:
        flash(error, 'error')
        return redirect(url_for('espectaculos'))
    nuevo_espectaculo = Espectaculo(nombre=nombre, descripcion=descripcion, fecha=fecha, sala=sala)
    db.session.add(nuevo_espectaculo)
    db.session.commit()
    flash('Espectáculo creado exitosamente.', 'success')
    return redirect(url_for('espectaculos'))

@app.route('/espectaculos/eliminar/<int:id>')
def eliminar_espectaculo(id):
    espectaculo = Espectaculo.query.get(id)
    if espectaculo is None:
        return handle_404_error(404)  
    db.session.delete(espectaculo)
    db.session.commit()
    return redirect(url_for('espectaculos'))

@app.route('/reservas')
def reservas():
    reservas = Reserva.query.all()
    return render_template('reservas.html', reservas=reservas)

@app.route('/reservas/crear', methods=['POST'])
def crear_reserva():
    usuario_id = request.form['usuario_id']
    espectaculo_id = request.form['espectaculo_id']
    error = validate_reserva(usuario_id, espectaculo_id)
    if error:
        flash(error, 'error')
        return redirect(url_for('reservas'))
    nueva_reserva = Reserva(usuario_id=usuario_id, espectaculo_id=espectaculo_id, fecha_reserva=datetime.now())
    db.session.add(nueva_reserva)
    db.session.commit()
    flash('Reserva creada exitosamente.', 'success')
    return redirect(url_for('reservas'))

@app.route('/reservas/eliminar/<int:id>')
def eliminar_reserva(id):
    reserva = Reserva.query.get(id)
    if reserva is None:
        return handle_404_error(404)  
    db.session.delete(reserva)
    db.session.commit()
    return redirect(url_for('reservas'))

@app.errorhandler(404)
def not_found_error(e):
    return handle_404_error(e)

@app.errorhandler(500)
def internal_error(e):
    return handle_db_error(e)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)