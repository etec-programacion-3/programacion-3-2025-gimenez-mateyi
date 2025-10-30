from pymongo import MongoClient
from bson import ObjectId
import bcrypt as bcrypt_lib  # Cambiar el import
import logging

class VehiculoDB:
    def __init__(self, mongo_url):
        try:
            self.client = MongoClient(mongo_url)
            self.db = self.client['concesionaria']
            self.collection = self.db['vehiculos']
            self.usuarios = self.db['usuarios']
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
            
            # Hashear la contraseña usando bcrypt directamente
            password_hash = bcrypt_lib.hashpw(password.encode('utf-8'), bcrypt_lib.gensalt()).decode('utf-8')
            
            usuario = {
                "username": username,
                "password": password_hash,
                "email": email
            }
            
            resultado = self.usuarios.insert_one(usuario)
            logging.info(f"✅ Usuario {username} creado exitosamente")
            return str(resultado.inserted_id)
        except Exception as e:
            logging.error(f"Error al crear usuario: {e}")
            return None
    
    def verificar_usuario(self, username, password):
        """Verifica las credenciales del usuario"""
        if self.usuarios is None:
            logging.error("Colección de usuarios no disponible")
            return None
        try:
            usuario = self.usuarios.find_one({"username": username})
            
            if not usuario:
                logging.warning(f"Usuario {username} no encontrado")
                return None
            
            # Verificar contraseña usando bcrypt directamente
            password_match = bcrypt_lib.checkpw(password.encode('utf-8'), usuario['password'].encode('utf-8'))
            
            if password_match:
                usuario['_id'] = str(usuario['_id'])
                logging.info(f"✅ Login exitoso para {username}")
                return usuario
            else:
                logging.warning(f"❌ Contraseña incorrecta para {username}")
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
        
        # --- MÉTODOS DE MENSAJERÍA ---
    
    def crear_mensaje(self, nombre, email, mensaje):
        """Crea un nuevo mensaje de contacto"""
        if self.db is None:
            return None
        try:
            mensajes_collection = self.db['mensajes']
            
            from datetime import datetime
            mensaje_data = {
                "nombre": nombre,
                "email": email,
                "mensaje": mensaje,
                "fecha": datetime.now(),
                "leido": False
            }
            
            resultado = mensajes_collection.insert_one(mensaje_data)
            logging.info(f"✅ Mensaje creado de {nombre}")
            return str(resultado.inserted_id)
        except Exception as e:
            logging.error(f"Error al crear mensaje: {e}")
            return None
    
    def obtener_mensajes(self, solo_no_leidos=False):
        """Obtiene todos los mensajes o solo los no leídos"""
        if self.db is None:
            return []
        try:
            mensajes_collection = self.db['mensajes']
            
            filtro = {"leido": False} if solo_no_leidos else {}
            mensajes = list(mensajes_collection.find(filtro).sort("fecha", -1))
            
            for m in mensajes:
                m['_id'] = str(m['_id'])
            
            return mensajes
        except Exception as e:
            logging.error(f"Error al obtener mensajes: {e}")
            return []
    
    def obtener_mensaje(self, mensaje_id):
        """Obtiene un mensaje específico"""
        if self.db is None:
            return None
        try:
            mensajes_collection = self.db['mensajes']
            mensaje = mensajes_collection.find_one({"_id": ObjectId(mensaje_id)})
            
            if mensaje:
                mensaje['_id'] = str(mensaje['_id'])
            
            return mensaje
        except Exception as e:
            logging.error(f"Error al obtener mensaje: {e}")
            return None
    
    def marcar_mensaje_leido(self, mensaje_id, leido=True):
        """Marca un mensaje como leído o no leído"""
        if self.db is None:
            return False
        try:
            mensajes_collection = self.db['mensajes']
            resultado = mensajes_collection.update_one(
                {"_id": ObjectId(mensaje_id)},
                {"$set": {"leido": leido}}
            )
            return resultado.modified_count > 0
        except Exception as e:
            logging.error(f"Error al marcar mensaje: {e}")
            return False
    
    def eliminar_mensaje(self, mensaje_id):
        """Elimina un mensaje"""
        if self.db is None:
            return False
        try:
            mensajes_collection = self.db['mensajes']
            resultado = mensajes_collection.delete_one({"_id": ObjectId(mensaje_id)})
            return resultado.deleted_count > 0
        except Exception as e:
            logging.error(f"Error al eliminar mensaje: {e}")
            return False
    
    def contar_mensajes_no_leidos(self):
        """Cuenta los mensajes no leídos"""
        if self.db is None:
            return 0
        try:
            mensajes_collection = self.db['mensajes']
            return mensajes_collection.count_documents({"leido": False})
        except Exception as e:
            logging.error(f"Error al contar mensajes: {e}")
            return 0