from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from bson import ObjectId
import logging

# Crear el Blueprint
vehiculos_bp = Blueprint('vehiculos', __name__)

# Variable global para la base de datos (se inicializará desde app.py)
db = None

def init_vehiculos_routes(vehiculos_db):
    """Inicializa las rutas con la instancia de la base de datos"""
    global db
    db = vehiculos_db

# --- API REST endpoints ---

@vehiculos_bp.route('/api/vehiculos', methods=['GET'])
def api_obtener_vehiculos():
    """GET - Obtener todos los vehículos (público)"""
    if db is None:
        return jsonify({"error": "Base de datos no disponible"}), 500
    
    vehiculos = db.obtener_vehiculos()
    return jsonify(vehiculos), 200

@vehiculos_bp.route('/api/vehiculos/<vehiculo_id>', methods=['GET'])
def api_obtener_vehiculo(vehiculo_id):
    """GET - Obtener un vehículo específico (público)"""
    if db is None:
        return jsonify({"error": "Base de datos no disponible"}), 500
    
    vehiculo = db.obtener_vehiculo(vehiculo_id)
    if vehiculo:
        return jsonify(vehiculo), 200
    return jsonify({"error": "Vehículo no encontrado"}), 404

@vehiculos_bp.route('/api/vehiculos', methods=['POST'])
# @login_required  # ⚠️ COMENTADO TEMPORALMENTE PARA TESTING
def api_crear_vehiculo():
    """POST - Crear un nuevo vehículo"""
    if db is None:
        return jsonify({"error": "Base de datos no disponible"}), 500
    
    datos = request.json
    
    # Validación básica
    campos_requeridos = ['modelo', 'descripcion', 'precio', 'imagen']
    for campo in campos_requeridos:
        if campo not in datos:
            return jsonify({"error": f"Falta el campo: {campo}"}), 400
    
    vehiculo_id = db.crear_vehiculo(datos)
    if vehiculo_id:
        return jsonify({"mensaje": "Vehículo creado", "id": vehiculo_id}), 201
    return jsonify({"error": "Error al crear vehículo"}), 500

@vehiculos_bp.route('/api/vehiculos/<vehiculo_id>', methods=['PUT'])
# @login_required  # ⚠️ COMENTADO TEMPORALMENTE PARA TESTING
def api_actualizar_vehiculo(vehiculo_id):
    """PUT - Actualizar un vehículo"""
    if db is None:
        return jsonify({"error": "Base de datos no disponible"}), 500
    
    datos = request.json
    
    if db.actualizar_vehiculo(vehiculo_id, datos):
        return jsonify({"mensaje": "Vehículo actualizado"}), 200
    return jsonify({"error": "Error al actualizar vehículo"}), 500

@vehiculos_bp.route('/api/vehiculos/<vehiculo_id>', methods=['DELETE'])
# @login_required  # ⚠️ COMENTADO TEMPORALMENTE PARA TESTING
def api_eliminar_vehiculo(vehiculo_id):
    """DELETE - Eliminar un vehículo"""
    if db is None:
        return jsonify({"error": "Base de datos no disponible"}), 500
    
    if db.eliminar_vehiculo(vehiculo_id):
        return jsonify({"mensaje": "Vehículo eliminado"}), 200
    return jsonify({"error": "Error al eliminar vehículo"}), 500

# --- Ruta para el panel de administración (UI) ---

@vehiculos_bp.route('/admin/vehiculos')
# @login_required  # ⚠️ COMENTADO TEMPORALMENTE PARA TESTING
def admin_vehiculos():
    """Panel de administración de vehículos"""
    return render_template('admin_vehiculos.html')