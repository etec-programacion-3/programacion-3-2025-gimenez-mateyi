from pymongo import MongoClient
from bson import ObjectId
import bcrypt
import logging
from datetime import datetime

class VehiculoDB:
    def __init__(self, mongo_url):
        try:
            self.client = MongoClient(mongo_url)
            self.db = self.client['concesionaria']
            self.collection = self.db['vehiculos']
            self.usuarios = self.db['usuarios']
            self.favoritos = self.db['favoritos']
            self.cotizaciones = self.db['cotizaciones']
            self.turnos = self.db['turnos']
            self.alertas = self.db['alertas']
            logging.info("✅ Conectado a MongoDB Atlas")
        except Exception as e:
            logging.error(f"❌ Error al conectar a MongoDB: {e}")
            self.client = self.db = self.collection = self.usuarios = None
    
    # ==================== VEHÍCULOS ====================
    
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
    
    # ==================== AUTENTICACIÓN ====================
    
    def crear_usuario(self, username, password, email, role='usuario'):
        """Crea un nuevo usuario"""
        if self.usuarios is None:
            return None
        try:
            if self.usuarios.find_one({"username": username}):
                logging.warning(f"Usuario {username} ya existe")
                return None
            
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            usuario = {
                "username": username,
                "password": password_hash.decode('utf-8'),
                "email": email,
                "role": role,
                "fecha_registro": datetime.now()
            }
            
            resultado = self.usuarios.insert_one(usuario)
            logging.info(f"✅ Usuario {username} creado con rol: {role}")
            return str(resultado.inserted_id)
        except Exception as e:
            logging.error(f"Error al crear usuario: {e}")
            return None
    
    def verificar_usuario(self, username, password):
        """Verifica credenciales"""
        if self.usuarios is None:
            return None
        try:
            usuario = self.usuarios.find_one({"username": username})
            if not usuario:
                return None
            
            stored_hash = usuario['password']
            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode('utf-8')
            
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                usuario['_id'] = str(usuario['_id'])
                return usuario
            return None
        except Exception as e:
            logging.error(f"Error al verificar usuario: {e}")
            return None
    
    def obtener_usuario_por_id(self, usuario_id):
        """Obtiene usuario por ID"""
        if self.usuarios is None:
            return None
        try:
            usuario = self.usuarios.find_one({"_id": ObjectId(usuario_id)})
            if usuario:
                usuario['_id'] = str(usuario['_id'])
            return usuario
        except Exception as e:
            return None
    
    def obtener_usuario_por_username(self, username):
        """Obtiene usuario por username"""
        if self.usuarios is None:
            return None
        try:
            usuario = self.usuarios.find_one({"username": username})
            if usuario:
                usuario['_id'] = str(usuario['_id'])
            return usuario
        except Exception as e:
            return None
    
    # ==================== FAVORITOS ====================
    
    def agregar_favorito(self, usuario_id, vehiculo_id):
        """Agrega un vehículo a favoritos"""
        try:
            # Verificar si ya existe
            existente = self.favoritos.find_one({
                'usuario_id': usuario_id,
                'vehiculo_id': vehiculo_id
            })
            
            if existente:
                return None  # Ya está en favoritos
            
            favorito = {
                'usuario_id': usuario_id,
                'vehiculo_id': vehiculo_id,
                'fecha_agregado': datetime.now()
            }
            
            resultado = self.favoritos.insert_one(favorito)
            return str(resultado.inserted_id)
        except Exception as e:
            logging.error(f"Error al agregar favorito: {e}")
            return None
    
    def eliminar_favorito(self, usuario_id, vehiculo_id):
        """Elimina un vehículo de favoritos"""
        try:
            resultado = self.favoritos.delete_one({
                'usuario_id': usuario_id,
                'vehiculo_id': vehiculo_id
            })
            return resultado.deleted_count > 0
        except Exception as e:
            logging.error(f"Error al eliminar favorito: {e}")
            return False
    
    def obtener_favoritos(self, usuario_id):
        """Obtiene todos los favoritos de un usuario"""
        try:
            favoritos = list(self.favoritos.find({'usuario_id': usuario_id}))
            
            # Obtener información de cada vehículo
            vehiculos_favoritos = []
            for fav in favoritos:
                vehiculo = self.obtener_vehiculo(fav['vehiculo_id'])
                if vehiculo:
                    vehiculo['fecha_agregado'] = fav['fecha_agregado']
                    vehiculos_favoritos.append(vehiculo)
            
            return vehiculos_favoritos
        except Exception as e:
            logging.error(f"Error al obtener favoritos: {e}")
            return []
    
    def es_favorito(self, usuario_id, vehiculo_id):
        """Verifica si un vehículo está en favoritos"""
        try:
            favorito = self.favoritos.find_one({
                'usuario_id': usuario_id,
                'vehiculo_id': vehiculo_id
            })
            return favorito is not None
        except Exception as e:
            return False
    
    # ==================== COTIZACIONES ====================
    
    def crear_cotizacion(self, usuario_id, datos_cotizacion):
        """Crea una nueva cotización"""
        try:
            cotizacion = {
                'usuario_id': usuario_id,
                'vehiculo_id': datos_cotizacion.get('vehiculo_id'),
                'marca': datos_cotizacion.get('marca'),
                'modelo': datos_cotizacion.get('modelo'),
                'anio': datos_cotizacion.get('anio'),
                'precio_estimado': datos_cotizacion.get('precio_estimado'),
                'fecha': datetime.now(),
                'estado': 'pendiente'  # pendiente, aprobada, rechazada
            }
            
            resultado = self.cotizaciones.insert_one(cotizacion)
            return str(resultado.inserted_id)
        except Exception as e:
            logging.error(f"Error al crear cotización: {e}")
            return None
    
    def obtener_cotizaciones(self, usuario_id):
        """Obtiene todas las cotizaciones de un usuario"""
        try:
            cotizaciones = list(self.cotizaciones.find(
                {'usuario_id': usuario_id}
            ).sort('fecha', -1))
            
            for c in cotizaciones:
                c['_id'] = str(c['_id'])
            
            return cotizaciones
        except Exception as e:
            logging.error(f"Error al obtener cotizaciones: {e}")
            return []
    
    # ==================== TURNOS TEST DRIVE ====================
    
    def crear_turno(self, usuario_id, vehiculo_id, fecha_hora, comentarios=''):
        """Crea un turno para test drive"""
        try:
            turno = {
                'usuario_id': usuario_id,
                'vehiculo_id': vehiculo_id,
                'fecha_hora': fecha_hora,
                'comentarios': comentarios,
                'fecha_creacion': datetime.now(),
                'estado': 'pendiente'  # pendiente, confirmado, completado, cancelado
            }
            
            resultado = self.turnos.insert_one(turno)
            return str(resultado.inserted_id)
        except Exception as e:
            logging.error(f"Error al crear turno: {e}")
            return None
    
    def obtener_turnos(self, usuario_id):
        """Obtiene todos los turnos de un usuario"""
        try:
            turnos = list(self.turnos.find(
                {'usuario_id': usuario_id}
            ).sort('fecha_hora', -1))
            
            # Obtener información del vehículo
            for turno in turnos:
                turno['_id'] = str(turno['_id'])
                vehiculo = self.obtener_vehiculo(turno['vehiculo_id'])
                if vehiculo:
                    turno['vehiculo'] = vehiculo
            
            return turnos
        except Exception as e:
            logging.error(f"Error al obtener turnos: {e}")
            return []
    
    def actualizar_estado_turno(self, turno_id, nuevo_estado):
        """Actualiza el estado de un turno"""
        try:
            resultado = self.turnos.update_one(
                {'_id': ObjectId(turno_id)},
                {'$set': {'estado': nuevo_estado}}
            )
            return resultado.modified_count > 0
        except Exception as e:
            logging.error(f"Error al actualizar turno: {e}")
            return False
    
    def cancelar_turno(self, turno_id, usuario_id):
        """Cancela un turno"""
        try:
            resultado = self.turnos.update_one(
                {'_id': ObjectId(turno_id), 'usuario_id': usuario_id},
                {'$set': {'estado': 'cancelado'}}
            )
            return resultado.modified_count > 0
        except Exception as e:
            logging.error(f"Error al cancelar turno: {e}")
            return False
    
    # ==================== ALERTAS ====================
    
    def crear_alerta(self, usuario_id, criterios):
        """Crea una alerta personalizada"""
        try:
            alerta = {
                'usuario_id': usuario_id,
                'marca': criterios.get('marca'),
                'modelo': criterios.get('modelo'),
                'precio_max': criterios.get('precio_max'),
                'anio_min': criterios.get('anio_min'),
                'activa': True,
                'fecha_creacion': datetime.now()
            }
            
            resultado = self.alertas.insert_one(alerta)
            return str(resultado.inserted_id)
        except Exception as e:
            logging.error(f"Error al crear alerta: {e}")
            return None
    
    def obtener_alertas(self, usuario_id):
        """Obtiene todas las alertas de un usuario"""
        try:
            alertas = list(self.alertas.find({'usuario_id': usuario_id}))
            
            for a in alertas:
                a['_id'] = str(a['_id'])
            
            return alertas
        except Exception as e:
            logging.error(f"Error al obtener alertas: {e}")
            return []
    
    def eliminar_alerta(self, alerta_id, usuario_id):
        """Elimina una alerta"""
        try:
            resultado = self.alertas.delete_one({
                '_id': ObjectId(alerta_id),
                'usuario_id': usuario_id
            })
            return resultado.deleted_count > 0
        except Exception as e:
            logging.error(f"Error al eliminar alerta: {e}")
            return False
    
    def toggle_alerta(self, alerta_id, usuario_id):
        """Activa/desactiva una alerta"""
        try:
            alerta = self.alertas.find_one({
                '_id': ObjectId(alerta_id),
                'usuario_id': usuario_id
            })
            
            if not alerta:
                return False
            
            nuevo_estado = not alerta.get('activa', True)
            
            resultado = self.alertas.update_one(
                {'_id': ObjectId(alerta_id)},
                {'$set': {'activa': nuevo_estado}}
            )
            
            return resultado.modified_count > 0
        except Exception as e:
            logging.error(f"Error al toggle alerta: {e}")
            return False
    
    # ==================== MENSAJERÍA (para admin) ====================
    
    def crear_mensaje(self, nombre, email, mensaje):
        """Crea un mensaje de contacto"""
        if self.db is None:
            return None
        try:
            mensajes_collection = self.db['mensajes']
            
            mensaje_data = {
                "nombre": nombre,
                "email": email,
                "mensaje": mensaje,
                "fecha": datetime.now(),
                "leido": False
            }
            
            resultado = mensajes_collection.insert_one(mensaje_data)
            return str(resultado.inserted_id)
        except Exception as e:
            logging.error(f"Error al crear mensaje: {e}")
            return None
    
    def obtener_mensajes(self, solo_no_leidos=False):
        """Obtiene mensajes"""
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
            return []
    
    def marcar_mensaje_leido(self, mensaje_id, leido=True):
        """Marca mensaje como leído"""
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
            return False
    
    def contar_mensajes_no_leidos(self):
        """Cuenta mensajes no leídos"""
        if self.db is None:
            return 0
        try:
            mensajes_collection = self.db['mensajes']
            return mensajes_collection.count_documents({"leido": False})
        except Exception as e:
            return 0