from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect('/tareas')
    return render_template('login_registro.html')

@app.route('/registro', methods=['POST'])
def registro():
    if not Usuario.validar_registro(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = Usuario.guardar(data)
    session['usuario_id'] = user_id
    return redirect('/tareas')

@app.route('/login', methods=['POST'])
def login():
    usuario = Usuario.obtener_por_email(request.form['email'])
    if not usuario:
        flash("El email no está registrado.", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Contraseña incorrecta.", "login")
        return redirect('/')
    
    session['usuario_id'] = usuario.id
    return redirect('/tareas')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
