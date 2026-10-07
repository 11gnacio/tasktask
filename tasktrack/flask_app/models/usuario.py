from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def guardar(cls, data):
        query = "INSERT INTO usuarios (nombre, apellido, email, password) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);"
        return connectToMySQL().query_db(query, data)

    @classmethod
    def obtener_por_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connectToMySQL().query_db(query, {'email': email})
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def obtener_por_id(cls, user_id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        results = connectToMySQL().query_db(query, {'id': user_id})
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validar_registro(user):
        es_valido = True
        if len(user['nombre'].strip()) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            es_valido = False
        if len(user['apellido'].strip()) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "registro")
            es_valido = False
        if not EMAIL_REGEX.match(user['email']):
            flash("El email no tiene un formato válido.", "registro")
            es_valido = False
        else:
            if Usuario.obtener_por_email(user['email']):
                flash("El email ya se encuentra registrado.", "registro")
                es_valido = False
        if len(user['password']) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "registro")
            es_valido = False
        if user['password'] != user['confirm_password']:
            flash("Las contraseñas no coinciden.", "registro")
            es_valido = False
        return es_valido
