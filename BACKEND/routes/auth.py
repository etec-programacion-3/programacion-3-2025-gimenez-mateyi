from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
import logging

auth_bp = Blueprint('auth', __name__)

# Variable global para la base de datos
db = None

def init_auth_routes(vehiculos_db):
    """Inicializa las rutas de autenticación con la instancia de la base de datos"""
    global db
    db = vehiculos_db

class User:
    """Clase User para Flask-Login"""
    def __init__(self, usuario_data):
        self.id = usuario_data['_id']
        self.username = usuario_data['username']
        self.email = usuario_data.get('email', '')
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if current_user.is_authenticated:
        logging.info("Usuario ya autenticado, redirigiendo...")
        return redirect(url_for('vehiculos.admin_vehiculos'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        logging.info(f"🔍 Intento de login - Usuario: {username}")
        
        if not username or not password:
            logging.warning("Campos vacíos")
            flash('Por favor completa todos los campos', 'danger')
            return render_template('login.html')
        
        # Verificar que db esté disponible
        if db is None:
            logging.error("❌ Base de datos no disponible")
            flash('Error del servidor. Intenta más tarde.', 'danger')
            return render_template('login.html')
        
        # Verificar credenciales
        logging.info(f"Verificando credenciales para: {username}")
        usuario = db.verificar_usuario(username, password)
        
        if usuario:
            logging.info(f"✅ Credenciales correctas para: {username}")
            user_obj = User(usuario)
            login_user(user_obj)
            flash(f'¡Bienvenido {username}!', 'success')
            
            # Redirigir a la página solicitada o al admin
            next_page = request.args.get('next')
            logging.info(f"Redirigiendo a: {next_page or '/admin/vehiculos'}")
            return redirect(next_page or url_for('vehiculos.admin_vehiculos'))
        else:
            logging.warning(f"❌ Credenciales incorrectas para: {username}")
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    username = current_user.username
    logout_user()
    logging.info(f"Usuario {username} cerró sesión")
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('home'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro (opcional, puedes deshabilitarla en producción)"""
    if current_user.is_authenticated:
        return redirect(url_for('vehiculos.admin_vehiculos'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        
        if not all([username, email, password, password2]):
            flash('Por favor completa todos los campos', 'danger')
            return render_template('register.html')
        
        if password != password2:
            flash('Las contraseñas no coinciden', 'danger')
            return render_template('register.html')
        
        # Crear usuario
        usuario_id = db.crear_usuario(username, password, email)
        
        if usuario_id:
            flash('Usuario creado exitosamente. Por favor inicia sesión.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('El usuario ya existe', 'danger')
    
    return render_template('register.html')