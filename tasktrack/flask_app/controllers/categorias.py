from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.categoria import Categoria
from flask_app.models.usuario import Usuario

@app.route('/categorias')
def listar_categorias():
    if 'usuario_id' not in session:
        return redirect('/')
    usuario = Usuario.obtener_por_id(session['usuario_id'])
    categorias = Categoria.obtener_por_usuario(session['usuario_id'])
    return render_template('categorias.html', usuario=usuario, categorias=categorias)

@app.route('/categorias/nueva')
def nueva_categoria():
    if 'usuario_id' not in session:
        return redirect('/')
    usuario = Usuario.obtener_por_id(session['usuario_id'])
    return render_template('nueva_categoria.html', usuario=usuario)

@app.route('/categorias/crear', methods=['POST'])
def crear_categoria():
    if 'usuario_id' not in session:
        return redirect('/')
    data = {
        'nombre': request.form['nombre'],
        'usuario_id': session['usuario_id']
    }
    if not Categoria.validar(data):
        return redirect('/categorias/nueva')
    
    Categoria.guardar(data)
    return redirect('/categorias')

@app.route('/categorias/borrar/<int:id>')
def borrar_categoria(id):
    if 'usuario_id' not in session:
        return redirect('/')
    Categoria.eliminar({'id': id, 'usuario_id': session['usuario_id']})
    return redirect('/categorias')
