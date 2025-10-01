import json
from pymongo import MongoClient

# Conexión a MongoDB Atlas
MONGO_URL = "mongodb+srv://mateyi:Colon1339@cluster0.terwnab.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URL)

db = client['concesionaria']
collection = db['vehiculos']

# Cargar el JSON local
with open("data/vehiculos.json", "r", encoding="utf-8") as f:
    vehiculos = json.load(f)

# Insertar en la colección
collection.insert_many(vehiculos)
print("✅ Vehículos importados a MongoDB Atlas correctamente!")
