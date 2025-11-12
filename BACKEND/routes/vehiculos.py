"""
Rutas para la gestión de vehículos
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from bson import ObjectId
from bson.errors import InvalidId
import logging

vehiculos_bp = Blueprint('vehiculos', __name__)

# Variable global para almacenar la instancia de VehiculoDB
db_instance = None

def init_vehiculos_routes(db):
    """
    Inicializa las rutas con la instancia de la base de datos
    """
    global db_instance
    db_instance = db
    logging.info("✅ Rutas de vehículos inicializadas correctamente")

# ==================== RUTAS PÚBLICAS ====================

@vehiculos_bp.route('/catalogo')
def catalogo():
    """Muestra el catálogo completo de vehículos disponibles"""
    try:
        vehiculos = db_instance.obtener_vehiculos()
        logging.info(f"📋 Catálogo cargado con {len(vehiculos)} vehículos")
        return render_template('catalogo.html', vehiculos=vehiculos)
    except Exception as e:
        logging.error(f"❌ Error al cargar catálogo: {e}")
        flash('Error al cargar el catálogo de vehículos', 'error')
        return redirect(url_for('home'))

@vehiculos_bp.route('/vehiculo/<id>')
def detalle_vehiculo(id):
    """Muestra el detalle completo de un vehículo específico"""
    try:
        logging.info(f"🔍 Intentando cargar vehículo con ID: {id}")
        vehiculo = db_instance.obtener_vehiculo(id)
        
        if not vehiculo:
            logging.warning(f"⚠️ Vehículo no encontrado con ID: {id}")
            flash('Vehículo no encontrado', 'warning')
            return redirect(url_for('vehiculos.catalogo'))
        
        logging.info(f"✅ Vehículo cargado exitosamente: {vehiculo.get('modelo', 'Sin modelo')}")
        return render_template('detalle_vehiculo.html', vehiculo=vehiculo)
        
    except InvalidId as e:
        logging.error(f"❌ ID inválido: {id} - Error: {e}")
        flash('ID de vehículo inválido', 'error')
        return redirect(url_for('vehiculos.catalogo'))
    except Exception as e:
        logging.error(f"❌ Error inesperado al cargar vehículo {id}: {e}")
        flash('Error al cargar el vehículo', 'error')
        return redirect(url_for('vehiculos.catalogo'))

# ==================== RUTAS DE ADMINISTRACIÓN ====================

@vehiculos_bp.route('/admin/vehiculos')
@login_required
def admin_vehiculos():
    """Panel de administración de vehículos"""
    try:
        vehiculos = db_instance.obtener_vehiculos()
        return render_template('admin_vehiculos.html', vehiculos=vehiculos)
    except Exception as e:
        logging.error(f"❌ Error al cargar admin de vehículos: {e}")
        flash('Error al cargar el panel de administración', 'error')
        return redirect(url_for('home'))

# ==================== API REST ====================

@vehiculos_bp.route('/api/vehiculos', methods=['GET'])
@login_required
def api_obtener_vehiculos():
    """GET - Obtener todos los vehículos"""
    try:
        vehiculos = db_instance.obtener_vehiculos()
        return jsonify(vehiculos), 200
    except Exception as e:
        logging.error(f"Error en API obtener vehículos: {e}")
        return jsonify({"error": "Error al obtener vehículos"}), 500

@vehiculos_bp.route('/api/vehiculos/<id>', methods=['GET'])
@login_required
def api_obtener_vehiculo(id):
    """GET - Obtener un vehículo específico"""
    try:
        vehiculo = db_instance.obtener_vehiculo(id)
        if vehiculo:
            return jsonify(vehiculo), 200
        return jsonify({"error": "Vehículo no encontrado"}), 404
    except Exception as e:
        logging.error(f"Error en API obtener vehículo: {e}")
        return jsonify({"error": "Error al obtener vehículo"}), 500

@vehiculos_bp.route('/api/vehiculos', methods=['POST'])
@login_required
def api_crear_vehiculo():
    """POST - Crear un nuevo vehículo"""
    try:
        datos = request.json
        
        # Validar datos requeridos
        campos_requeridos = ['modelo', 'descripcion', 'precio', 'imagen']
        for campo in campos_requeridos:
            if campo not in datos:
                return jsonify({"error": f"Falta el campo: {campo}"}), 400
        
        # Agregar campos por defecto
        if 'anio' not in datos:
            from datetime import datetime
            datos['anio'] = datetime.now().year
        if 'stock' not in datos:
            datos['stock'] = 1
        if 'categoria' not in datos:
            datos['categoria'] = 'sedan'
        
        vehiculo_id = db_instance.crear_vehiculo(datos)
        
        if vehiculo_id:
            return jsonify({"_id": vehiculo_id, "mensaje": "Vehículo creado"}), 201
        return jsonify({"error": "Error al crear vehículo"}), 500
        
    except Exception as e:
        logging.error(f"Error en API crear vehículo: {e}")
        return jsonify({"error": str(e)}), 500

@vehiculos_bp.route('/api/vehiculos/<id>', methods=['PUT'])
@login_required
def api_actualizar_vehiculo(id):
    """PUT - Actualizar un vehículo existente"""
    try:
        datos = request.json
        
        if db_instance.actualizar_vehiculo(id, datos):
            return jsonify({"mensaje": "Vehículo actualizado"}), 200
        return jsonify({"error": "Vehículo no encontrado"}), 404
        
    except Exception as e:
        logging.error(f"Error en API actualizar vehículo: {e}")
        return jsonify({"error": str(e)}), 500

@vehiculos_bp.route('/api/vehiculos/<id>', methods=['DELETE'])
@login_required
def api_eliminar_vehiculo(id):
    """DELETE - Eliminar un vehículo"""
    try:
        if db_instance.eliminar_vehiculo(id):
            return jsonify({"mensaje": "Vehículo eliminado"}), 200
        return jsonify({"error": "Vehículo no encontrado"}), 404
        
    except Exception as e:
        logging.error(f"Error en API eliminar vehículo: {e}")
        return jsonify({"error": str(e)}), 500