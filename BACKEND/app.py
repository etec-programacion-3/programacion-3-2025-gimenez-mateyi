from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_login import LoginManager, login_required
from models import VehiculoDB
from routes.auth import auth_bp, init_auth_routes, User
from routes.vehiculos import vehiculos_bp, init_vehiculos_routes
from routes.usuarios import usuarios_bp, init_usuarios_routes
from routes.mensajes import mensajes_bp, init_mensajes_routes
from routes.planes_cotizador import planes_cotizador_bp, init_planes_cotizador_routes
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()
MONGO_URL = os.getenv('MONGO_URL', "mongodb+srv://mateyi2:Colon1339@cluster0.terwnab.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

app = Flask(__name__, 
            template_folder='../FRONTEND/templates',
            static_folder='../FRONTEND/static')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'tu_clave_secreta_super_segura_cambiar_en_produccion')

db = VehiculoDB(MONGO_URL)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor iniciá sesión para acceder a esta página'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    usuario = db.obtener_usuario_por_id(user_id)
    if usuario:
        return User(usuario)
    return None

init_auth_routes(db)
init_vehiculos_routes(db)
init_usuarios_routes(db)
init_mensajes_routes(db)
init_planes_cotizador_routes(db)

app.register_blueprint(auth_bp)
app.register_blueprint(vehiculos_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(mensajes_bp)
app.register_blueprint(planes_cotizador_bp)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quienes-somos')
def quienes_somos():
    return render_template('quienes_somos.html')

@app.route('/planes')
def planes():
    return render_template('planes.html')

@app.route('/cotizador', methods=['GET', 'POST'])
def cotizador():
    """Cotizador de vehículos usados"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            marca = request.form.get('marca', '')
            modelo = request.form.get('modelo', '')
            anio = int(request.form.get('anio', 2020))
            kilometraje = int(request.form.get('kilometraje', 0))
            estado = request.form.get('estado', 'bueno')
            
            # Cálculo simple de cotización
            valor_base = 8000000  # Base de 8 millones
            
            # Depreciación por año
            anio_actual = 2025
            anos_uso = anio_actual - anio
            depreciacion_anual = 400000  # 400k por año
            depreciacion_total = anos_uso * depreciacion_anual
            
            # Depreciación por kilometraje
            depreciacion_km = (kilometraje / 10000) * 80000  # 80k cada 10k km
            
            # Multiplicador por estado
            multiplicadores = {
                'excelente': 1.15,
                'muy_bueno': 1.0,
                'bueno': 0.85,
                'regular': 0.65
            }
            multiplicador = multiplicadores.get(estado, 0.85)
            
            # Calcular valor final
            valor_estimado = (valor_base - depreciacion_total - depreciacion_km) * multiplicador
            valor_estimado = max(valor_estimado, 500000)  # Mínimo 500k
            
            flash(f'Cotización calculada exitosamente para {marca} {modelo}', 'success')
            
            return render_template('cotizador.html', 
                                   resultado={
                                       'valor_estimado': valor_estimado,
                                       'marca': marca,
                                       'modelo': modelo,
                                       'anio': anio
                                   })
        
        except Exception as e:
            logging.error(f"Error en cotizador: {e}")
            flash('Error al calcular la cotización. Verificá los datos ingresados.', 'danger')
            return render_template('cotizador.html')
    
    return render_template('cotizador.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    """Formulario de contacto"""
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '')
            email = request.form.get('email', '')
            telefono = request.form.get('telefono', '')
            mensaje = request.form.get('mensaje', '')
            
            if not nombre or not email or not mensaje:
                flash('Por favor completá todos los campos obligatorios', 'warning')
                return render_template('contacto.html')
            
            # Guardar mensaje en la base de datos
            mensaje_data = {
                'nombre': nombre,
                'email': email,
                'telefono': telefono,
                'mensaje': mensaje,
                'leido': False
            }
            
            resultado = db.db['mensajes'].insert_one(mensaje_data)
            
            if resultado.inserted_id:
                flash('¡Mensaje enviado exitosamente! Te responderemos a la brevedad.', 'success')
                logging.info(f"Mensaje de contacto recibido de {nombre} ({email})")
            else:
                flash('Error al enviar el mensaje. Intenta nuevamente.', 'danger')
        
        except Exception as e:
            logging.error(f"Error en contacto: {e}")
            flash('Error al procesar tu mensaje. Intenta nuevamente.', 'danger')
        
        return redirect(url_for('contacto'))
    
    return render_template('contacto.html')

@app.route('/api/vehiculos/destacados')
def vehiculos_destacados():
    """API para obtener vehículos destacados"""
    try:
        vehiculos = db.obtener_vehiculos()
        destacados = vehiculos[:3] if len(vehiculos) >= 3 else vehiculos
        return jsonify(destacados)
    except Exception as e:
        logging.error(f"Error al obtener destacados: {e}")
        return jsonify([]), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    logging.error(f"Error 500: {e}")
    return render_template('500.html'), 500

@app.context_processor
def inject_datetime():
    from datetime import datetime, timedelta
    return {
        'datetime': datetime,
        'timedelta': timedelta
    }

if __name__ == '__main__':
    logging.info("="*60)
    logging.info("🚗 GIMÉNEZ AUTOMOTORES - SERVIDOR INICIANDO")
    logging.info("="*60)
    logging.info(f"📍 URL: http://127.0.0.1:5002")
    logging.info(f"🔗 MongoDB: {'Conectado' if db.client else 'Error de conexión'}")
    logging.info(f"🔐 Login: http://127.0.0.1:5002/login")
    logging.info(f"📝 Registro: http://127.0.0.1:5002/register")
    logging.info("="*60)
    
    app.run(
        host='127.0.0.1',
        port=5002,
        debug=True
    )