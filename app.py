from flask import Flask, render_template, request
from pymongo import MongoClient
import logging

# Configuración de logs
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, template_folder='templates')
app.static_folder = 'static'

# --- 🔹 Conexión a MongoDB Atlas ---
MONGO_URL = "mongodb+srv://mateyi2:Colon1339@cluster0.terwnab.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(MONGO_URL)
    db = client['concesionaria']
    collection = db['vehiculos']
    logging.info("✅ Conectado correctamente a MongoDB Atlas")
except Exception as e:
    logging.error(f"❌ Error al conectar a MongoDB: {e}")
    client = db = collection = None


# --- 🔹 Rutas principales ---
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/quienes-somos')
def quienes_somos():
    return render_template('quienes_somos.html')


@app.route('/catalogo')
def catalogo():
    vehiculos = []

    if collection is not None:
        try:
            vehiculos = list(collection.find())
        except Exception as e:
            logging.error(f"Error al cargar vehículos: {e}")

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

        # Factores para cálculo simple
        base_precio = 10000000
        anio_factor = max(0.8, 1.0 - (2025 - anio) * 0.1)
        estado_factor = {'excelente': 1.0, 'bueno': 0.8, 'regular': 0.6}.get(estado, 0.6)
        precio_estimado = base_precio * anio_factor * estado_factor

        return render_template('cotizador.html', precio=precio_estimado, datos=request.form)

    return render_template('cotizador.html', precio=None)


@app.route('/test-db')
def test_db():
    try:
        if db is not None:
            return {"status": "ok", "databases": client.list_database_names()}
        else:
            return {"status": "error", "error": "No hay conexión a MongoDB desde el servidor"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


if __name__ == '__main__':
    app.run(debug=True, port=5002)
