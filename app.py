from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import logging
from bson import json_util

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__, template_folder='templates')
app.static_folder = 'static'

# ✅ Conexión correcta a MongoDB Atlas
MONGO_URL = "mongodb+srv://mateyi:Colon1339@cluster0.terwnab.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URL)

# Base de datos y colección
db = client['concesionaria']
collection = db['vehiculos']

# 📦 Función para cargar vehículos desde MongoDB
def cargar_vehiculos():
    try:
        vehiculos = list(collection.find())
        return [json_util.loads(json_util.dumps(vehiculo, default=json_util.default)) for vehiculo in vehiculos]
    except Exception as e:
        logging.error(f"Error al cargar vehículos de MongoDB: {e}")
        return []

# 🏠 Página de inicio con vehículos destacados
@app.route('/')
def home():
    vehiculos = cargar_vehiculos()
    destacados = [v for v in vehiculos if v.get('destacado', False)]
    return render_template('index.html', destacados=destacados)

@app.route('/quienes-somos')
def quienes_somos():
    return render_template('quienes_somos.html')

@app.route('/catalogo')
def catalogo():
    vehiculos = cargar_vehiculos()
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
        print(f"Formulario recibido: {nombre} ({email}) - {mensaje}")
        return render_template('contacto.html', exito=True)
    return render_template('contacto.html', exito=False)

@app.route('/cotizador', methods=['GET', 'POST'])
def cotizador():
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        anio = int(request.form['anio'])
        estado = request.form['estado']
        base_precio = 10000000  # Precio base en pesos
        anio_factor = max(0.8, 1.0 - (2025 - anio) * 0.1)  # Depreciación por año
        estado_factor = {'excelente': 1.0, 'bueno': 0.8, 'regular': 0.6}.get(estado, 0.6)
        precio_estimado = base_precio * anio_factor * estado_factor
        return render_template('cotizador.html', precio=precio_estimado, datos=request.form)
    return render_template('cotizador.html', precio=None)

@app.route('/modelo/<string:modelo>')
def modelo_detalle(modelo):
    vehiculos = cargar_vehiculos()
    vehiculo = next((v for v in vehiculos if v['modelo'].lower().replace(' ', '-') == modelo.lower()), None)
    if vehiculo:
        return render_template('modelo_detalle.html', vehiculo=vehiculo)
    return "Vehículo no encontrado", 404

# 🔍 Ruta de prueba de conexión a MongoDB
@app.route('/test-db')
def test_db():
    try:
        collection.insert_one({"marca": "Fiat", "modelo": "Test", "anio": 2024})
        return "✅ Conexión exitosa: documento guardado en MongoDB Atlas!"
    except Exception as e:
        return f"❌ Error al conectar con MongoDB Atlas: {e}"

if __name__ == '__main__':
    app.run(debug=True, port=5002)
