"""
Rutas para la gestión de vehículos
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from bson import ObjectId
from bson.errors import InvalidId
import logging

vehiculos_bp = Blueprint('vehiculos', __name__)

# Variable global para almacenar la instancia de VehiculoDB
db_instance = None

def init_vehiculos_routes(db):
    """
    Inicializa las rutas con la instancia de la base de datos
    Debe ser llamado desde app.py después de crear la instancia de VehiculoDB
    
    Args:
        db: Instancia de VehiculoDB
    """
    global db_instance
    db_instance = db
    logging.info("✅ Rutas de vehículos inicializadas correctamente")

@vehiculos_bp.route('/catalogo')
def catalogo():
    """
    Muestra el catálogo completo de vehículos disponibles
    """
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
    """
    Muestra el detalle completo de un vehículo específico
    
    Args:
        id: ID del vehículo en MongoDB (puede ser string o ya ObjectId)
    """
    try:
        logging.info(f"🔍 Intentando cargar vehículo con ID: {id}")
        
        # Intentar obtener el vehículo directamente (tu método ya maneja la conversión)
        vehiculo = db_instance.obtener_vehiculo(id)
        
        if not vehiculo:
            logging.warning(f"⚠️ Vehículo no encontrado con ID: {id}")
            flash('Vehículo no encontrado', 'warning')
            return redirect(url_for('vehiculos.catalogo'))
        
        logging.info(f"✅ Vehículo cargado exitosamente: {vehiculo.get('modelo', 'Sin modelo')}")
        
        # Debug: mostrar qué datos tiene el vehículo
        logging.debug(f"📊 Datos del vehículo: {vehiculo}")
        
        return render_template('detalle_vehiculo.html', vehiculo=vehiculo)
        
    except InvalidId as e:
        logging.error(f"❌ ID inválido: {id} - Error: {e}")
        flash('ID de vehículo inválido', 'error')
        return redirect(url_for('vehiculos.catalogo'))
        
    except Exception as e:
        logging.error(f"❌ Error inesperado al cargar vehículo {id}: {e}")
        logging.exception("Traceback completo:")
        flash('Error al cargar el vehículo', 'error')
        return redirect(url_for('vehiculos.catalogo'))