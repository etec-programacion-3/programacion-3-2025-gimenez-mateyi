from flask import Flask, render_template, request, jsonify
import json
from json.decoder import JSONDecodeError
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__, template_folder='templates')
app.static_folder = 'static'

def cargar_vehiculos():
    try:
        with open('data/vehiculos.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        return []

@app.route('/')
def home():
    vehiculos = cargar_vehiculos()
    destacados = [v for v in vehiculos if v['destacado']]
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
        # Simulación simple de cotización
        base_precio = 10000000  # Precio base en pesos
        anio_factor = max(0.8, 1.0 - (2025 - anio) * 0.1)  # Depreciación por año
        estado_factor = {'excelente': 1.0, 'bueno': 0.8, 'regular': 0.6}.get(estado, 0.6)
        precio_estimado = base_precio * anio_factor * estado_factor
        return render_template('cotizador.html', precio=precio_estimado, datos=request.form)
    return render_template('cotizador.html', precio=None)

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Usa puerto 5002 para evitar conflictos