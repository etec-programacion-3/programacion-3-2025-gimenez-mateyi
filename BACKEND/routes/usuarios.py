"""
Blueprint de funcionalidades para usuarios registrados
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import logging

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuario')

db_instance = None

def init_usuarios_routes(db):
    """Inicializa las rutas de usuarios"""
    global db_instance
    db_instance = db
    logging.info("✅ Rutas de usuarios inicializadas")

# ==================== FAVORITOS ====================

@usuarios_bp.route('/favoritos')
@login_required
def mis_favoritos():
    """Muestra los vehículos favoritos del usuario"""
    try:
        favoritos = db_instance.obtener_favoritos(current_user.id)
        return render_template('usuario/favoritos.html', favoritos=favoritos)
    except Exception as e:
        logging.error(f"Error al cargar favoritos: {e}")
        flash('Error al cargar favoritos', 'error')
        return redirect(url_for('home'))

@usuarios_bp.route('/favorito/agregar/<vehiculo_id>', methods=['POST'])
@login_required
def agregar_favorito(vehiculo_id):
    """Agrega un vehículo a favoritos"""
    try:
        resultado = db_instance.agregar_favorito(current_user.id, vehiculo_id)
        
        if resultado:
            return jsonify({'success': True, 'mensaje': 'Agregado a favoritos'})
        else:
            return jsonify({'success': False, 'mensaje': 'Ya está en favoritos'})
    except Exception as e:
        logging.error(f"Error al agregar favorito: {e}")
        return jsonify({'success': False, 'mensaje': 'Error al agregar'})

@usuarios_bp.route('/favorito/eliminar/<vehiculo_id>', methods=['POST'])
@login_required
def eliminar_favorito(vehiculo_id):
    """Elimina un vehículo de favoritos"""
    try:
        resultado = db_instance.eliminar_favorito(current_user.id, vehiculo_id)
        
        if resultado:
            return jsonify({'success': True, 'mensaje': 'Eliminado de favoritos'})
        else:
            return jsonify({'success': False, 'mensaje': 'No se pudo eliminar'})
    except Exception as e:
        logging.error(f"Error al eliminar favorito: {e}")
        return jsonify({'success': False, 'mensaje': 'Error al eliminar'})

@usuarios_bp.route('/favorito/verificar/<vehiculo_id>', methods=['GET'])
@login_required
def verificar_favorito(vehiculo_id):
    """Verifica si un vehículo está en favoritos"""
    try:
        es_favorito = db_instance.es_favorito(current_user.id, vehiculo_id)
        return jsonify({'es_favorito': es_favorito})
    except Exception as e:
        logging.error(f"Error al verificar favorito: {e}")
        return jsonify({'es_favorito': False})

# ==================== COTIZACIONES ====================

@usuarios_bp.route('/cotizaciones')
@login_required
def mis_cotizaciones():
    """Muestra el historial de cotizaciones"""
    try:
        cotizaciones = db_instance.obtener_cotizaciones(current_user.id)
        return render_template('usuario/cotizaciones.html', cotizaciones=cotizaciones)
    except Exception as e:
        logging.error(f"Error al cargar cotizaciones: {e}")
        flash('Error al cargar cotizaciones', 'error')
        return redirect(url_for('home'))

@usuarios_bp.route('/cotizacion/crear', methods=['POST'])
@login_required
def crear_cotizacion():
    """Crea una nueva cotización"""
    try:
        datos = request.json
        
        cotizacion_id = db_instance.crear_cotizacion(current_user.id, datos)
        
        if cotizacion_id:
            return jsonify({'success': True, 'cotizacion_id': cotizacion_id})
        else:
            return jsonify({'success': False, 'mensaje': 'Error al crear cotización'})
    except Exception as e:
        logging.error(f"Error al crear cotización: {e}")
        return jsonify({'success': False, 'mensaje': str(e)})

# ==================== TURNOS TEST DRIVE ====================

@usuarios_bp.route('/turnos')
@login_required
def mis_turnos():
    """Muestra los turnos agendados"""
    try:
        turnos = db_instance.obtener_turnos(current_user.id)
        return render_template('usuario/turnos.html', turnos=turnos)
    except Exception as e:
        logging.error(f"Error al cargar turnos: {e}")
        flash('Error al cargar turnos', 'error')
        return redirect(url_for('home'))

@usuarios_bp.route('/turno/agendar', methods=['GET', 'POST'])
@login_required
def agendar_turno():
    """Agenda un nuevo turno para test drive"""
    if request.method == 'POST':
        try:
            vehiculo_id = request.form.get('vehiculo_id')
            fecha_str = request.form.get('fecha')
            hora = request.form.get('hora')
            comentarios = request.form.get('comentarios', '')
            
            # Combinar fecha y hora
            fecha_hora = datetime.strptime(f"{fecha_str} {hora}", "%Y-%m-%d %H:%M")
            
            turno_id = db_instance.crear_turno(
                current_user.id,
                vehiculo_id,
                fecha_hora,
                comentarios
            )
            
            if turno_id:
                flash('Turno agendado exitosamente', 'success')
                return redirect(url_for('usuarios.mis_turnos'))
            else:
                flash('Error al agendar turno', 'error')
        except Exception as e:
            logging.error(f"Error al agendar turno: {e}")
            flash('Error al procesar el turno', 'error')
    
    # GET: Mostrar formulario
    vehiculos = db_instance.obtener_vehiculos()
    return render_template('usuario/agendar_turno.html', vehiculos=vehiculos)

@usuarios_bp.route('/turno/cancelar/<turno_id>', methods=['POST'])
@login_required
def cancelar_turno(turno_id):
    """Cancela un turno"""
    try:
        resultado = db_instance.cancelar_turno(turno_id, current_user.id)
        
        if resultado:
            return jsonify({'success': True, 'mensaje': 'Turno cancelado'})
        else:
            return jsonify({'success': False, 'mensaje': 'No se pudo cancelar'})
    except Exception as e:
        logging.error(f"Error al cancelar turno: {e}")
        return jsonify({'success': False, 'mensaje': str(e)})

# ==================== ALERTAS ====================

@usuarios_bp.route('/alertas')
@login_required
def mis_alertas():
    """Muestra las alertas configuradas"""
    try:
        alertas = db_instance.obtener_alertas(current_user.id)
        return render_template('usuario/alertas.html', alertas=alertas)
    except Exception as e:
        logging.error(f"Error al cargar alertas: {e}")
        flash('Error al cargar alertas', 'error')
        return redirect(url_for('home'))

@usuarios_bp.route('/alerta/crear', methods=['GET', 'POST'])
@login_required
def crear_alerta():
    """Crea una nueva alerta"""
    if request.method == 'POST':
        try:
            criterios = {
                'marca': request.form.get('marca'),
                'modelo': request.form.get('modelo'),
                'precio_max': int(request.form.get('precio_max')) if request.form.get('precio_max') else None,
                'anio_min': int(request.form.get('anio_min')) if request.form.get('anio_min') else None
            }
            
            alerta_id = db_instance.crear_alerta(current_user.id, criterios)
            
            if alerta_id:
                flash('Alerta creada exitosamente', 'success')
                return redirect(url_for('usuarios.mis_alertas'))
            else:
                flash('Error al crear alerta', 'error')
        except Exception as e:
            logging.error(f"Error al crear alerta: {e}")
            flash('Error al procesar la alerta', 'error')
    
    return render_template('usuario/crear_alerta.html')

@usuarios_bp.route('/alerta/eliminar/<alerta_id>', methods=['POST'])
@login_required
def eliminar_alerta(alerta_id):
    """Elimina una alerta"""
    try:
        resultado = db_instance.eliminar_alerta(alerta_id, current_user.id)
        
        if resultado:
            return jsonify({'success': True, 'mensaje': 'Alerta eliminada'})
        else:
            return jsonify({'success': False, 'mensaje': 'No se pudo eliminar'})
    except Exception as e:
        logging.error(f"Error al eliminar alerta: {e}")
        return jsonify({'success': False, 'mensaje': str(e)})

@usuarios_bp.route('/alerta/toggle/<alerta_id>', methods=['POST'])
@login_required
def toggle_alerta(alerta_id):
    """Activa/desactiva una alerta"""
    try:
        resultado = db_instance.toggle_alerta(alerta_id, current_user.id)
        
        if resultado:
            return jsonify({'success': True, 'mensaje': 'Estado actualizado'})
        else:
            return jsonify({'success': False, 'mensaje': 'No se pudo actualizar'})
    except Exception as e:
        logging.error(f"Error al toggle alerta: {e}")
        return jsonify({'success': False, 'mensaje': str(e)})

# ==================== DASHBOARD ====================

@usuarios_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal del usuario"""
    try:
        # Obtener resumen de todo
        favoritos = db_instance.obtener_favoritos(current_user.id)
        cotizaciones = db_instance.obtener_cotizaciones(current_user.id)
        turnos = db_instance.obtener_turnos(current_user.id)
        alertas = db_instance.obtener_alertas(current_user.id)
        
        return render_template('usuario/dashboard.html',
                             favoritos_count=len(favoritos),
                             cotizaciones_count=len(cotizaciones),
                             turnos_count=len([t for t in turnos if t['estado'] == 'pendiente']),
                             alertas_count=len([a for a in alertas if a.get('activa', True)]))
    except Exception as e:
        logging.error(f"Error al cargar dashboard: {e}")
        flash('Error al cargar dashboard', 'error')
        return redirect(url_for('home'))