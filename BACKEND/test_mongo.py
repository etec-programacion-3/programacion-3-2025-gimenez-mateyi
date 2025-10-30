from pymongo import MongoClient

MONGO_URL = "mongodb+srv://mateyi:Colon1339@cluster0.terwnab.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(MONGO_URL)
    dbs = client.list_database_names()
    print("✅ Conectado correctamente. Bases de datos:", dbs)
except Exception as e:
    print("❌ Error de conexión:", e)
