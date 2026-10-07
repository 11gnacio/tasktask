from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.tarea import Tarea
from flask_app.models.categoria import Categoria
from flask_app.models.usuario import Usuario
from datetime import datetime

@app.route('/tareas')
def mis_tareas():
    if 'usuario_id' not in session:
        return redirect('/')
    
    usuario = Usuario.obtener_por_id(session['usuario_id'])
    busqueda = request.args.get('q', '')
    cat_filter = request.args.get('categoria_id', '')
    est_filter = request.args.get('estado', '')
    prio_filter = request.args.get('prioridad', '')

    tareas = Tarea.obtener_por_usuario(session['usuario_id'], busqueda, cat_filter, est_filter, prio_filter)
    categorias = Categoria.obtener_por_usuario(session['usuario_id'])
    resumen = Tarea.obtener_resumen(session['usuario_id'])

    # Calcular días restantes para la sección de "Próximas tareas"
    hoy = datetime.now().date()
    proximas = []
    for t in tareas:
        dias = (t.fecha_limite - hoy).days
        proximas.append({
            'titulo': t.titulo,
            'fecha_limite': t.fecha_limite,
            'dias_restantes': dias
        })

    return render_template('mis_tareas.html', usuario=usuario, tareas=tareas, categorias=categorias, resumen=resumen, proximas=proximas)

@app.route('/tareas/nueva')
def nueva_tarea():
    if 'usuario_id' not in session:
        return redirect('/')
    usuario = Usuario.obtener_por_id(session['usuario_id'])
    categorias = Categoria.obtener_por_usuario(session['usuario_id'])
    return render_template('nueva_tarea.html', usuario=usuario, categorias=categorias)

@app.route('/tareas/crear', methods=['POST'])
def crear_tarea():
    if 'usuario_id' not in session:
        return redirect('/')
    
    data = {
        'titulo': request.form['titulo'],
        'categoria_id': request.form.get('categoria_id'),
        'prioridad': request.form.get('prioridad'),
        'fecha_limite': request.form['fecha_limite'],
        'descripcion': request.form['descripcion'],
        'usuario_id': session['usuario_id']
    }

    if not Tarea.validar(data):
        return redirect('/tareas/nueva')

    Tarea.guardar(data)
    return redirect('/tareas')

@app.route('/tareas/<int:id>')
def detalle_tarea(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    tarea = Tarea.obtener_por_id(id)
    if not tarea or tarea.usuario_id != session['usuario_id']:
        return redirect('/tareas')

    usuario = Usuario.obtener_por_id(session['usuario_id'])
    return render_template('detalle_tarea.html', usuario=usuario, tarea=tarea)

@app.route('/tareas/editar/<int:id>')
def editar_tarea(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    tarea = Tarea.obtener_por_id(id)
    if not tarea or tarea.usuario_id != session['usuario_id']:
        return redirect('/tareas')

    usuario = Usuario.obtener_por_id(session['usuario_id'])
    categorias = Categoria.obtener_por_usuario(session['usuario_id'])
    return render_template('editar_tarea.html', usuario=usuario, tarea=tarea, categorias=categorias)

@app.route('/tareas/actualizar/<int:id>', methods=['POST'])
def actualizar_tarea(id):
    if 'usuario_id' not in session:
        return redirect('/')

    data = {
        'id': id,
        'titulo': request.form['titulo'],
        'categoria_id': request.form.get('categoria_id'),
        'prioridad': request.form.get('prioridad'),
        'fecha_limite': request.form['fecha_limite'],
        'descripcion': request.form['descripcion'],
        'usuario_id': session['usuario_id']
    }

    if not Tarea.validar(data):
        return redirect(f'/tareas/editar/{id}')

    Tarea.actualizar(data)
    return redirect(f'/tareas/{id}')

@app.route('/tareas/completar/<int:id>')
def completar_tarea(id):
    if 'usuario_id' not in session:
        return redirect('/')
    Tarea.cambiar_estado(id, 'Completada')
    return redirect(f'/tareas/{id}')

@app.route('/tareas/borrar/<int:id>')
def borrar_tarea(id):
    if 'usuario_id' not in session:
        return redirect('/')
    Tarea.eliminar({'id': id, 'usuario_id': session['usuario_id']})
    return redirect('/tareas')
