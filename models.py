from pymongo import MongoClient
from bson import ObjectId
from flask_bcrypt import Bcrypt
import logging

bcrypt = Bcrypt()

class VehiculoDB:
    def __init__(self, mongo_url):
        try:
            self.client = MongoClient(mongo_url)
            self.db = self.client['concesionaria']
            self.collection = self.db['vehiculos']
            self.usuarios = self.db['usuarios']  # Nueva colección para usuarios
            logging.info("✅ Conectado a MongoDB Atlas")
        except Exception as e:
            logging.error(f"❌ Error al conectar a MongoDB: {e}")
            self.client = self.db = self.collection = self.usuarios = None
    
    def crear_vehiculo(self, datos):
        """Crea un nuevo vehículo"""
        if self.collection is None:
            return None
        try:
            resultado = self.collection.insert_one(datos)
            return str(resultado.inserted_id)
        except Exception as e:
            logging.error(f"Error al crear vehículo: {e}")
            return None
    
    def obtener_vehiculos(self):
        """Obtiene todos los vehículos"""
        if self.collection is None:
            return []
        try:
            vehiculos = list(self.collection.find())
            for v in vehiculos:
                v['_id'] = str(v['_id'])
            return vehiculos
        except Exception as e:
            logging.error(f"Error al obtener vehículos: {e}")
            return []
    
    def obtener_vehiculo(self, vehiculo_id):
        """Obtiene un vehículo por ID"""
        if self.collection is None:
            return None
        try:
            vehiculo = self.collection.find_one({"_id": ObjectId(vehiculo_id)})
            if vehiculo:
                vehiculo['_id'] = str(vehiculo['_id'])
            return vehiculo
        except Exception as e:
            logging.error(f"Error al obtener vehículo: {e}")
            return None
    
    def actualizar_vehiculo(self, vehiculo_id, datos):
        """Actualiza un vehículo existente"""
        if self.collection is None:
            return False
        try:
            resultado = self.collection.update_one(
                {"_id": ObjectId(vehiculo_id)},
                {"$set": datos}
            )
            return resultado.modified_count > 0
        except Exception as e:
            logging.error(f"Error al actualizar vehículo: {e}")
            return False
    
    def eliminar_vehiculo(self, vehiculo_id):
        """Elimina un vehículo"""
        if self.collection is None:
            return False
        try:
            resultado = self.collection.delete_one({"_id": ObjectId(vehiculo_id)})
            return resultado.deleted_count > 0
        except Exception as e:
            logging.error(f"Error al eliminar vehículo: {e}")
            return False
    
    # --- MÉTODOS DE AUTENTICACIÓN ---
    
    def crear_usuario(self, username, password, email):
        """Crea un nuevo usuario con contraseña hasheada"""
        if self.usuarios is None:
            return None
        try:
            # Verificar si el usuario ya existe
            if self.usuarios.find_one({"username": username}):
                logging.warning(f"Usuario {username} ya existe")
                return None
            
            # Hashear la contraseña
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            
            usuario = {
                "username": username,
                "password": password_hash,
                "email": email
            }
            
            resultado = self.usuarios.insert_one(usuario)
            return str(resultado.inserted_id)
        except Exception as e:
            logging.error(f"Error al crear usuario: {e}")
            return None
    
    def verificar_usuario(self, username, password):
        """Verifica las credenciales del usuario"""
        if self.usuarios is None:
            return None
        try:
            usuario = self.usuarios.find_one({"username": username})
            if usuario and bcrypt.check_password_hash(usuario['password'], password):
                usuario['_id'] = str(usuario['_id'])
                return usuario
            return None
        except Exception as e:
            logging.error(f"Error al verificar usuario: {e}")
            return None
    
    def obtener_usuario_por_id(self, usuario_id):
        """Obtiene un usuario por su ID"""
        if self.usuarios is None:
            return None
        try:
            usuario = self.usuarios.find_one({"_id": ObjectId(usuario_id)})
            if usuario:
                usuario['_id'] = str(usuario['_id'])
            return usuario
        except Exception as e:
            logging.error(f"Error al obtener usuario: {e}")
            return None
    
    def obtener_usuario_por_username(self, username):
        """Obtiene un usuario por su username"""
        if self.usuarios is None:
            return None
        try:
            usuario = self.usuarios.find_one({"username": username})
            if usuario:
                usuario['_id'] = str(usuario['_id'])
            return usuario
        except Exception as e:
            logging.error(f"Error al obtener usuario: {e}")
            return None