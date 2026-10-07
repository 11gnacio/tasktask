from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime

class Tarea:
    def __init__(self, data):
        self.id = data['id']
        self.titulo = data['titulo']
        self.prioridad = data['prioridad']
        self.fecha_limite = data['fecha_limite']
        self.estado = data['estado']
        self.descripcion = data['descripcion']
        self.usuario_id = data['usuario_id']
        self.categoria_id = data['categoria_id']
        self.categoria_nombre = data.get('categoria_nombre', '')
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO tareas (titulo, prioridad, fecha_limite, descripcion, usuario_id, categoria_id)
            VALUES (%(titulo)s, %(prioridad)s, %(fecha_limite)s, %(descripcion)s, %(usuario_id)s, %(categoria_id)s);
        """
        return connectToMySQL().query_db(query, data)

    @classmethod
    def obtener_por_usuario(cls, usuario_id, busqueda="", categoria_id="", estado="", prioridad=""):
        query = """
            SELECT t.*, c.nombre as categoria_nombre 
            FROM tareas t
            JOIN categorias c ON t.categoria_id = c.id
            WHERE t.usuario_id = %(usuario_id)s
        """
        params = {'usuario_id': usuario_id}

        if busqueda:
            query += " AND t.titulo LIKE %(busqueda)s"
            params['busqueda'] = f"%{busqueda}%"
        if categoria_id:
            query += " AND t.categoria_id = %(categoria_id)s"
            params['categoria_id'] = categoria_id
        if estado:
            query += " AND t.estado = %(estado)s"
            params['estado'] = estado
        if prioridad:
            query += " AND t.prioridad = %(prioridad)s"
            params['prioridad'] = prioridad

        query += " ORDER BY t.fecha_limite ASC;"
        results = connectToMySQL().query_db(query, params)
        return [cls(row) for row in results] if results else []

    @classmethod
    def obtener_por_id(cls, tarea_id):
        query = """
            SELECT t.*, c.nombre as categoria_nombre 
            FROM tareas t
            JOIN categorias c ON t.categoria_id = c.id
            WHERE t.id = %(id)s;
        """
        results = connectToMySQL().query_db(query, {'id': tarea_id})
        return cls(results[0]) if results else None

    @classmethod
    def actualizar(cls, data):
        query = """
            UPDATE tareas SET titulo=%(titulo)s, prioridad=%(prioridad)s, fecha_limite=%(fecha_limite)s,
            descripcion=%(descripcion)s, categoria_id=%(categoria_id)s WHERE id=%(id)s AND usuario_id=%(usuario_id)s;
        """
        return connectToMySQL().query_db(query, data)

    @classmethod
    def cambiar_estado(cls, tarea_id, estado):
        query = "UPDATE tareas SET estado = %(estado)s WHERE id = %(id)s;"
        return connectToMySQL().query_db(query, {'id': tarea_id, 'estado': estado})

    @classmethod
    def eliminar(cls, data):
        query = "DELETE FROM tareas WHERE id = %(id)s AND usuario_id = %(usuario_id)s;"
        return connectToMySQL().query_db(query, data)

    @classmethod
    def obtener_resumen(cls, usuario_id):
        query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN estado = 'Pendiente' THEN 1 ELSE 0 END) as pendientes,
                SUM(CASE WHEN estado = 'En progreso' THEN 1 ELSE 0 END) as en_progreso,
                SUM(CASE WHEN estado = 'Completada' THEN 1 ELSE 0 END) as completadas
            FROM tareas WHERE usuario_id = %(usuario_id)s;
        """
        res = connectToMySQL().query_db(query, {'usuario_id': usuario_id})
        return res[0] if res else {'total': 0, 'pendientes': 0, 'en_progreso': 0, 'completadas': 0}

    @staticmethod
    def validar(data):
        es_valido = True
        if len(data['titulo'].strip()) < 3:
            flash("El título debe tener al menos 3 caracteres.", "tarea")
            es_valido = False
        if not data.get('categoria_id'):
            flash("Debe seleccionar una categoría.", "tarea")
            es_valido = False
        if not data.get('fecha_limite'):
            flash("Debe ingresar una fecha límite.", "tarea")
            es_valido = False
        else:
            try:
                fecha_ingresada = datetime.strptime(data['fecha_limite'], '%Y-%m-%d').date()
                if fecha_ingresada < datetime.now().date():
                    flash("La fecha no puede ser pasada.", "tarea")
                    es_valido = False
            except ValueError:
                flash("Formato de fecha inválido.", "tarea")
                es_valido = False
        if len(data['descripcion'].strip()) < 10:
            flash("La descripción debe tener al menos 10 caracteres.", "tarea")
            es_valido = False
        return es_valido
