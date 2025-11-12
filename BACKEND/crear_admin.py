"""
Script completo para crear/actualizar usuario admin con rol
Ejecutar: python setup_admin.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from models import VehiculoDB
from dotenv import load_dotenv
import bcrypt

load_dotenv()
MONGO_URL = os.getenv('MONGO_URL', "mongodb+srv://mateyi2:Colon1339@cluster0.terwnab.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

print("="*60)
print("👑 CONFIGURACIÓN DE ADMIN - GIMÉNEZ AUTOMOTORES")
print("="*60)

try:
    db = VehiculoDB(MONGO_URL)
    print("\n✅ Conexión a MongoDB exitosa")
except Exception as e:
    print(f"\n❌ Error de conexión: {e}")
    sys.exit(1)

# Configuración del admin
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
ADMIN_EMAIL = "admin@gimenez.com"

print(f"\n🔍 Buscando usuario '{ADMIN_USERNAME}'...")

# Verificar si existe el admin
admin_existente = db.db['usuarios'].find_one({'username': ADMIN_USERNAME})

if admin_existente:
    print(f"✅ Usuario '{ADMIN_USERNAME}' encontrado")
    
    # Verificar si tiene el rol correcto
    rol_actual = admin_existente.get('role', 'sin rol')
    
    if rol_actual != 'admin':
        print(f"⚠️  Rol actual: '{rol_actual}' → Actualizando a 'admin'")
        
        db.db['usuarios'].update_one(
            {'username': ADMIN_USERNAME},
            {'$set': {'role': 'admin'}}
        )
        print("✅ Rol actualizado correctamente")
    else:
        print("✅ Ya tiene el rol 'admin' asignado")
    
    # Opcional: Actualizar contraseña
    print(f"\n🔐 ¿Querés resetear la contraseña a '{ADMIN_PASSWORD}'? (por si olvidaste la actual)")
    respuesta = input("   Escribí 'si' para confirmar o presioná ENTER para omitir: ").strip().lower()
    
    if respuesta == 'si':
        nuevo_hash = bcrypt.hashpw(ADMIN_PASSWORD.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db.db['usuarios'].update_one(
            {'username': ADMIN_USERNAME},
            {'$set': {'password': nuevo_hash}}
        )
        print("✅ Contraseña reseteada")
    else:
        print("ℹ️  Contraseña no modificada")

else:
    print(f"⚠️  Usuario '{ADMIN_USERNAME}' NO existe, creando...")
    
    # Crear nuevo admin con rol
    nuevo_hash = bcrypt.hashpw(ADMIN_PASSWORD.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    db.db['usuarios'].insert_one({
        'username': ADMIN_USERNAME,
        'password': nuevo_hash,
        'email': ADMIN_EMAIL,
        'role': 'admin'
    })
    
    print(f"✅ Usuario '{ADMIN_USERNAME}' creado exitosamente con rol 'admin'")

# Actualizar otros usuarios sin rol
print("\n🔍 Buscando usuarios sin rol asignado...")

usuarios_sin_rol = list(db.db['usuarios'].find({'role': {'$exists': False}}))

if usuarios_sin_rol:
    print(f"📋 Encontrados {len(usuarios_sin_rol)} usuarios sin rol")
    
    for usuario in usuarios_sin_rol:
        db.db['usuarios'].update_one(
            {'_id': usuario['_id']},
            {'$set': {'role': 'usuario'}}
        )
        print(f"  ✅ '{usuario['username']}' → rol 'usuario'")
else:
    print("✅ Todos los usuarios tienen rol asignado")

# Resumen final
print("\n" + "="*60)
print("✅ CONFIGURACIÓN COMPLETADA")
print("="*60)

print("\n👥 USUARIOS EN EL SISTEMA:")
print("-"*60)

for usuario in db.db['usuarios'].find():
    rol = usuario.get('role', 'sin rol')
    emoji = "👑" if rol == 'admin' else "👤"
    
    print(f"  {emoji} {usuario['username']:15} | Rol: {rol:10} | Email: {usuario.get('email', 'N/A')}")

print("-"*60)

# Mostrar credenciales de admin
print("\n📝 CREDENCIALES DE ACCESO ADMIN:")
print(f"   URL:      http://127.0.0.1:5002/login")
print(f"   Username: {ADMIN_USERNAME}")
print(f"   Password: {ADMIN_PASSWORD}")

print("\n" + "="*60)