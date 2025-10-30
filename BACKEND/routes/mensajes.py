from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from bson import ObjectId
import logging

# Crear el Blueprint
mensajes_bp = Blueprint('mensajes', __name__)

# Variable global para la base de datos
db = None

def init_mensajes_routes(vehiculos_db):
    """Inicializa las rutas con la instancia de la base de datos"""
    global db
    db = vehiculos_db

# --- API REST endpoints ---

@mensajes_bp.route('/api/mensajes', methods=['GET'])
@login_required
def api_obtener_mensajes():
    """GET - Obtener todos los mensajes"""
    if db is None:
        return jsonify({"error": "Base de datos no disponible"}), 500
    
    solo_no_leidos = request.args.get('no_leidos', 'false').lower() == 'true'
    mensajes = db.obtener_mensajes(solo_no_leidos)
    
    # Convertir fechas a string para JSON
    for m in mensajes:
        if 'fecha' in m:
            m['fecha'] = m['fecha'].strftime('%Y-%m-%d %H:%M:%S')
    
    return jsonify(mensajes), 200

@mensajes_bp.route('/api/mensajes/<mensaje_id>', methods=['GET'])
@login_required
def api_obtener_mensaje(mensaje_id):
    """GET - Obtener un mensaje específico"""
    if db is None:
        return jsonify({"error": "Base de datos no disponible"}), 500
    
    mensaje = db.obtener_mensaje(mensaje_id)
    if mensaje:
        if 'fecha' in mensaje:
            mensaje['fecha'] = mensaje['fecha'].strftime('%Y-%m-%d %H:%M:%S')
        return jsonify(mensaje), 200
    return jsonify({"error": "Mensaje no encontrado"}), 404

@mensajes_bp.route('/api/mensajes/<mensaje_id>/leido', methods=['PUT'])
@login_required
def api_marcar_leido(mensaje_id):
    """PUT - Marcar mensaje como leído/no leído"""
    if db is None:
        return jsonify({"error": "Base de datos no disponible"}), 500
    
    datos = request.json
    leido = datos.get('leido', True)
    
    if db.marcar_mensaje_leido(mensaje_id, leido):
        return jsonify({"mensaje": "Estado actualizado"}), 200
    return jsonify({"error": "Error al actualizar"}), 500

@mensajes_bp.route('/api/mensajes/<mensaje_id>', methods=['DELETE'])
@login_required
def api_eliminar_mensaje(mensaje_id):
    """DELETE - Eliminar un mensaje"""
    if db is None:
        return jsonify({"error": "Base de datos no disponible"}), 500
    
    if db.eliminar_mensaje(mensaje_id):
        return jsonify({"mensaje": "Mensaje eliminado"}), 200
    return jsonify({"error": "Error al eliminar"}), 500

@mensajes_bp.route('/api/mensajes/stats', methods=['GET'])
@login_required
def api_stats_mensajes():
    """GET - Estadísticas de mensajes"""
    if db is None:
        return jsonify({"error": "Base de datos no disponible"}), 500
    
    total = len(db.obtener_mensajes())
    no_leidos = db.contar_mensajes_no_leidos()
    
    return jsonify({
        "total": total,
        "no_leidos": no_leidos,
        "leidos": total - no_leidos
    }), 200

# --- Interfaz de administración ---

@mensajes_bp.route('/admin/mensajes')
@login_required
def admin_mensajes():
    """Panel de administración de mensajes"""
    return render_template('admin_mensajes.html')