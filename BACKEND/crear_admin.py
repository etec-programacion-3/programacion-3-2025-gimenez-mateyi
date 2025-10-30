import sys
import os

# Agregar el directorio BACKEND al path
sys.path.insert(0, os.path.dirname(__file__))

from models import VehiculoDB
import bcrypt

# Conexión a MongoDB
MONGO_URL = "mongodb+srv://mateyi2:Colon1339@cluster0.terwnab.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = VehiculoDB(MONGO_URL)

# Crear usuario admin
username = "admin"
password = "admin123"
email = "admin@gimenez.com"

usuario_id = client.crear_usuario(username, password, email)

if usuario_id:
    print(f"✅ Usuario '{username}' creado exitosamente")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    print(f"   Email: {email}")
else:
    print("ℹ️ El usuario admin ya existe")