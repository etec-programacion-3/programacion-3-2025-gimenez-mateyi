from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
import logging
import re

auth_bp = Blueprint('auth', __name__)

db = None

def init_auth_routes(vehiculos_db):
    global db
    db = vehiculos_db

class User:
    """Clase User para Flask-Login con soporte de roles"""
    def __init__(self, usuario_data):
        self.id = usuario_data['_id']
        self.username = usuario_data['username']
        self.email = usuario_data.get('email', '')
        self.role = usuario_data.get('role', 'usuario')
        
        # LOG para debug
        logging.info(f"🔍 Usuario cargado: {self.username} | Rol: {self.role}")
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
    def is_admin(self):
        """Verifica si el usuario es administrador"""
        es_admin = self.role == 'admin'
        logging.info(f"🔍 Verificando admin para {self.username}: role={self.role}, is_admin={es_admin}")
        return es_admin

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('vehiculos.admin_vehiculos'))
        else:
            return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        logging.info(f"🔍 Intento de login - Usuario: {username}")
        
        if not username or not password:
            flash('Por favor completa todos los campos', 'danger')
            return render_template('login.html')
        
        if db is None:
            flash('Error del servidor. Intenta más tarde.', 'danger')
            return render_template('login.html')
        
        usuario = db.verificar_usuario(username, password)
        
        if usuario:
            logging.info(f"✅ Usuario encontrado: {usuario}")
            user_obj = User(usuario)
            login_user(user_obj)
            
            if user_obj.is_admin():
                logging.info(f"✅ Admin login exitoso: {username}")
                flash(f'¡Bienvenido Admin {username}!', 'success')
                return redirect(url_for('vehiculos.admin_vehiculos'))
            else:
                logging.info(f"✅ Usuario login exitoso: {username}")
                flash(f'¡Bienvenido {username}!', 'success')
                return redirect(url_for('home'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('home'))

def validar_username(username):
    if len(username) < 3:
        return False, "El nombre de usuario debe tener al menos 3 caracteres"
    if len(username) > 20:
        return False, "El nombre de usuario no puede tener más de 20 caracteres"
    if not re.match("^[a-zA-Z0-9_]+$", username):
        return False, "El nombre de usuario solo puede contener letras, números y guiones bajos"
    return True, ""

def validar_email(email):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(patron, email):
        return False, "El formato del email no es válido"
    return True, ""

def validar_password(password):
    if len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres"
    if len(password) > 50:
        return False, "La contraseña no puede tener más de 50 caracteres"
    return True, ""

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        password2 = request.form.get('password2', '')
        
        if not all([username, email, password, password2]):
            flash('Por favor completa todos los campos', 'danger')
            return render_template('register.html')
        
        valido, mensaje = validar_username(username)
        if not valido:
            flash(mensaje, 'danger')
            return render_template('register.html')
        
        valido, mensaje = validar_email(email)
        if not valido:
            flash(mensaje, 'danger')
            return render_template('register.html')
        
        valido, mensaje = validar_password(password)
        if not valido:
            flash(mensaje, 'danger')
            return render_template('register.html')
        
        if password != password2:
            flash('Las contraseñas no coinciden', 'danger')
            return render_template('register.html')
        
        if db.obtener_usuario_por_username(username):
            flash('El nombre de usuario ya está en uso', 'danger')
            return render_template('register.html')
        
        usuario_email = db.db['usuarios'].find_one({'email': email})
        if usuario_email:
            flash('El email ya está registrado', 'danger')
            return render_template('register.html')
        
        usuario_id = db.crear_usuario(username, password, email, role='usuario')
        
        if usuario_id:
            flash('¡Cuenta creada exitosamente! Ya podés iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Error al crear la cuenta. Intenta nuevamente.', 'danger')
    
    return render_template('register.html')