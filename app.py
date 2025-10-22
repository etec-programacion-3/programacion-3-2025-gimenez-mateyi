from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user
from models import VehiculoDB
from dotenv import load_dotenv
import logging
import os

# Cargar variables de entorno
load_dotenv()

# Configuración de logs
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, template_folder='templates')
app.static_folder = 'static'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave_secreta_por_defecto')

# --- Configurar Flask-Login ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'

# --- Conexión a MongoDB ---
MONGO_URL = os.getenv('MONGO_URL')
vehiculos_db = VehiculoDB(MONGO_URL)

# --- User Loader para Flask-Login ---
from routes.auth import User

@login_manager.user_loader
def load_user(user_id):
    usuario_data = vehiculos_db.obtener_usuario_por_id(user_id)
    if usuario_data:
        return User(usuario_data)
    return None

# --- Registrar Blueprints ---
from routes.vehiculos import vehiculos_bp, init_vehiculos_routes
from routes.auth import auth_bp, init_auth_routes

init_vehiculos_routes(vehiculos_db)
init_auth_routes(vehiculos_db)

app.register_blueprint(vehiculos_bp)
app.register_blueprint(auth_bp)

# --- Rutas principales ---
@app.route('/')
def home():
    destacados = vehiculos_db.obtener_vehiculos()[:3]
    return render_template('index.html', destacados=destacados)

@app.route('/quienes-somos')
def quienes_somos():
    return render_template('quienes_somos.html')

@app.route('/catalogo')
def catalogo():
    vehiculos = vehiculos_db.obtener_vehiculos()
    return render_template('catalogo.html', vehiculos=vehiculos)

@app.route('/planes')
def planes():
    return render_template('planes.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        mensaje = request.form['mensaje']
        print(f"📩 Formulario recibido: {nombre} ({email}) - {mensaje}")
        return render_template('contacto.html', exito=True)
    return render_template('contacto.html', exito=False)

@app.route('/cotizador', methods=['GET', 'POST'])
def cotizador():
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        anio = int(request.form['anio'])
        estado = request.form['estado']
        
        base_precio = 10000000
        anio_factor = max(0.8, 1.0 - (2025 - anio) * 0.1)
        estado_factor = {'excelente': 1.0, 'bueno': 0.8, 'regular': 0.6}.get(estado, 0.6)
        precio_estimado = base_precio * anio_factor * estado_factor
        
        return render_template('cotizador.html', precio=precio_estimado, datos=request.form)
    return render_template('cotizador.html', precio=None)

# --- Script para crear usuario admin inicial ---
@app.cli.command()
def crear_admin():
    """Crea un usuario administrador"""
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")
    
    usuario_id = vehiculos_db.crear_usuario(username, password, email)
    if usuario_id:
        print(f"✅ Usuario '{username}' creado exitosamente")
    else:
        print("❌ Error al crear usuario o ya existe")

if __name__ == '__main__':
    app.run(debug=True, port=5002)