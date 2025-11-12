import certifi
from pymongo import MongoClient

MONGO_URL = "mongodb+srv://mateyi2:Colon1339@cluster0.terwnab.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(MONGO_URL, tls=True, tlsCAFile=certifi.where())
    print("✅ Conectado correctamente. Bases de datos:", client.list_database_names())
except Exception as e:
    print("❌ Error de conexión:", e)
