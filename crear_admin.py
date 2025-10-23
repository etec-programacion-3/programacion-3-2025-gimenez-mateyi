import bcrypt
from pymongo import MongoClient

# Conexión a MongoDB
MONGO_URL = "mongodb+srv://mateyi2:Colon1339@cluster0.terwnab.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URL)
db = client['concesionaria']
usuarios = db['usuarios']

# Eliminar usuario admin si existe (para empezar limpio)
usuarios.delete_one({"username": "admin"})
print("🗑️ Usuario admin anterior eliminado (si existía)")

# Crear nuevo usuario admin
username = "admin"
password = "admin123"
email = "admin@gimenez.com"

# Hashear contraseña
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

usuario = {
    "username": username,
    "password": password_hash,
    "email": email
}

resultado = usuarios.insert_one(usuario)
print(f"✅ Usuario admin creado con ID: {resultado.inserted_id}")
print(f"   Username: {username}")
print(f"   Password: {password}")
print(f"   Email: {email}")

# Verificar que se creó correctamente
admin = usuarios.find_one({"username": "admin"})
if admin:
    print(f"\n✅ Verificación: Usuario encontrado en DB")
    print(f"   ID: {admin['_id']}")
    print(f"   Username: {admin['username']}")
    
    # Probar que la contraseña funciona
    password_match = bcrypt.checkpw(password.encode('utf-8'), admin['password'].encode('utf-8'))
    print(f"   Contraseña válida: {password_match}")
else:
    print("❌ Error: No se encontró el usuario")

client.close()