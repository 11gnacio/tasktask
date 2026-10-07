from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Categoria:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.usuario_id = data['usuario_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.cantidad_tareas = data.get('cantidad_tareas', 0)

    @classmethod
    def guardar(cls, data):
        query = "INSERT INTO categorias (nombre, usuario_id) VALUES (%(nombre)s, %(usuario_id)s);"
        return connectToMySQL().query_db(query, data)

    @classmethod
    def obtener_por_usuario(cls, usuario_id):
        query = """
            SELECT c.*, COUNT(t.id) as cantidad_tareas
            FROM categorias c
            LEFT JOIN tareas t ON c.id = t.categoria_id
            WHERE c.usuario_id = %(usuario_id)s
            GROUP BY c.id;
        """
        results = connectToMySQL().query_db(query, {'usuario_id': usuario_id})
        categorias = []
        if results:
            for row in results:
                categorias.append(cls(row))
        return categorias

    @classmethod
    def eliminar(cls, data):
        query = "DELETE FROM categorias WHERE id = %(id)s AND usuario_id = %(usuario_id)s;"
        return connectToMySQL().query_db(query, data)

    @staticmethod
    def validar(data):
        es_valido = True
        if len(data['nombre'].strip()) < 3:
            flash("El nombre de la categoría debe tener al menos 3 caracteres.", "categoria")
            es_valido = False
        
        # Validar duplicados por usuario
        query = "SELECT * FROM categorias WHERE nombre = %(nombre)s AND usuario_id = %(usuario_id)s;"
        res = connectToMySQL().query_db(query, data)
        if res:
            flash("El nombre de la categoría debe ser único.", "categoria")
            es_valido = False

        return es_valido
