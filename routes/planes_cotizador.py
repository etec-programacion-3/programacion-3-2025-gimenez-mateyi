from flask import Blueprint, request, jsonify
from datetime import datetime
import logging

# Crear el Blueprint
planes_cotizador_bp = Blueprint('planes_cotizador', __name__)

# Variable global para la base de datos
db = None

def init_planes_cotizador_routes(vehiculos_db):
    """Inicializa las rutas con la instancia de la base de datos"""
    global db
    db = vehiculos_db

# --- ENDPOINT: Cotizar Vehículo Usado ---

@planes_cotizador_bp.route('/api/cotizar', methods=['POST'])
def api_cotizar():
    """
    POST /api/cotizar
    
    Cotiza un vehículo usado basado en marca, modelo, año y estado.
    
    Body (JSON):
    {
        "marca": "Fiat",
        "modelo": "Cronos",
        "anio": 2020,
        "estado": "bueno"  // "excelente", "bueno", "regular"
    }
    
    Response:
    {
        "precio": 8500000,
        "detalles": {
            "marca": "Fiat",
            "modelo": "Cronos",
            "anio": 2020,
            "estado": "bueno",
            "base_precio": 10000000,
            "factor_anio": 0.85,
            "factor_estado": 0.8,
            "deprecacion_anual": 10%
        }
    }
    """
    try:
        # Validar que sea JSON
        if not request.is_json:
            return jsonify({"error": "Content-Type debe ser application/json"}), 400
        
        datos = request.json
        
        # Validar campos requeridos
        campos_requeridos = ['marca', 'modelo', 'anio', 'estado']
        for campo in campos_requeridos:
            if campo not in datos:
                return jsonify({"error": f"Falta el campo requerido: {campo}"}), 400
        
        marca = datos['marca']
        modelo = datos['modelo']
        anio = int(datos['anio'])
        estado = datos['estado'].lower()
        
        # Validar año
        anio_actual = datetime.now().year
        if anio < 1990 or anio > anio_actual + 1:
            return jsonify({"error": f"El año debe estar entre 1990 y {anio_actual + 1}"}), 400
        
        # Validar estado
        estados_validos = ['excelente', 'bueno', 'regular']
        if estado not in estados_validos:
            return jsonify({"error": f"Estado debe ser uno de: {', '.join(estados_validos)}"}), 400
        
        # Calcular cotización
        base_precio = 10000000  # Precio base en pesos argentinos
        
        # Factor de depreciación por año (10% anual)
        antiguedad = anio_actual - anio
        factor_anio = max(0.3, 1.0 - (antiguedad * 0.10))
        
        # Factor según estado del vehículo
        factores_estado = {
            'excelente': 1.0,
            'bueno': 0.8,
            'regular': 0.6
        }
        factor_estado = factores_estado[estado]
        
        # Factor adicional por marca/modelo (puedes expandir esto)
        factor_marca = 1.0
        if marca.lower() == 'fiat':
            factor_marca = 1.1  # 10% más para Fiat
        
        # Calcular precio final
        precio_estimado = base_precio * factor_anio * factor_estado * factor_marca
        
        # Redondear a miles
        precio_estimado = round(precio_estimado / 1000) * 1000
        
        # Preparar respuesta con detalles
        respuesta = {
            "precio": int(precio_estimado),
            "detalles": {
                "marca": marca,
                "modelo": modelo,
                "anio": anio,
                "estado": estado,
                "base_precio": base_precio,
                "factor_anio": round(factor_anio, 2),
                "factor_estado": factor_estado,
                "factor_marca": factor_marca,
                "antiguedad_anios": antiguedad,
                "deprecacion_anual": "10%",
                "moneda": "ARS"
            }
        }
        
        logging.info(f"Cotización realizada: {marca} {modelo} {anio} - Precio: ${precio_estimado:,.0f}")
        
        return jsonify(respuesta), 200
        
    except ValueError as e:
        return jsonify({"error": f"Error en los datos: {str(e)}"}), 400
    except Exception as e:
        logging.error(f"Error al cotizar: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


# --- ENDPOINT: Obtener Planes de Financiación ---

@planes_cotizador_bp.route('/api/planes', methods=['GET'])
def api_obtener_planes():
    """
    GET /api/planes
    
    Devuelve todos los planes de financiación disponibles.
    
    Response (JSON):
    [
        {
            "id": "plan-a",
            "nombre": "Plan 12 Cuotas",
            "descripcion": "Sin interés, ideal para compras rápidas",
            "cuotas": 12,
            "interes": 0,
            "enganche": 20,
            "detalles": {...}
        },
        ...
    ]
    """
    try:
        # Planes predefinidos (en producción, estos vendrían de la BD)
        planes = [
            {
                "id": "plan-a",
                "nombre": "Plan 12 Cuotas Sin Interés",
                "descripcion": "Ideal para compras rápidas. Pagá tu auto en 12 cuotas fijas sin interés.",
                "cuotas": 12,
                "interes": 0,
                "tasa_mensual": 0,
                "enganche_minimo": 20,  # porcentaje
                "monto_minimo": 5000000,
                "monto_maximo": 15000000,
                "vigencia": "2025-12-31",
                "destacado": True,
                "detalles": {
                    "requiere_recibo_sueldo": True,
                    "edad_minima": 18,
                    "edad_maxima": 75,
                    "documentacion": ["DNI", "Recibo de sueldo", "Servicio a nombre"]
                }
            },
            {
                "id": "plan-b",
                "nombre": "Plan 24 Cuotas Tasa Promocional",
                "descripcion": "Tasa promocional del 5% anual. Perfecto para financiar sin comprometer tu presupuesto.",
                "cuotas": 24,
                "interes": 5,
                "tasa_mensual": 0.42,
                "enganche_minimo": 15,
                "monto_minimo": 3000000,
                "monto_maximo": 20000000,
                "vigencia": "2025-12-31",
                "destacado": True,
                "detalles": {
                    "requiere_recibo_sueldo": True,
                    "edad_minima": 21,
                    "edad_maxima": 70,
                    "documentacion": ["DNI", "Recibo de sueldo últimos 3 meses", "Servicio a nombre"]
                }
            },
            {
                "id": "plan-c",
                "nombre": "Plan 36 Cuotas Extendido",
                "descripcion": "Financiación a largo plazo con cuotas más bajas. Tasa del 8% anual.",
                "cuotas": 36,
                "interes": 8,
                "tasa_mensual": 0.67,
                "enganche_minimo": 10,
                "monto_minimo": 2000000,
                "monto_maximo": 25000000,
                "vigencia": "2025-12-31",
                "destacado": False,
                "detalles": {
                    "requiere_recibo_sueldo": True,
                    "edad_minima": 21,
                    "edad_maxima": 65,
                    "documentacion": ["DNI", "Recibo de sueldo últimos 6 meses", "Servicio a nombre", "Garantía adicional"]
                }
            },
            {
                "id": "plan-100",
                "nombre": "Plan 100% Financiado",
                "descripcion": "Sin enganche. Financiamos el 100% del valor del vehículo en hasta 48 cuotas.",
                "cuotas": 48,
                "interes": 12,
                "tasa_mensual": 1.0,
                "enganche_minimo": 0,
                "monto_minimo": 4000000,
                "monto_maximo": 18000000,
                "vigencia": "2025-12-31",
                "destacado": True,
                "detalles": {
                    "requiere_recibo_sueldo": True,
                    "edad_minima": 25,
                    "edad_maxima": 60,
                    "documentacion": ["DNI", "Recibo de sueldo últimos 6 meses", "Servicio a nombre", "Constancia de trabajo", "Garantía"]
                }
            },
            {
                "id": "plan-corporativo",
                "nombre": "Plan Corporativo",
                "descripcion": "Especial para empresas y autónomos. Condiciones preferenciales.",
                "cuotas": 24,
                "interes": 3,
                "tasa_mensual": 0.25,
                "enganche_minimo": 25,
                "monto_minimo": 10000000,
                "monto_maximo": 50000000,
                "vigencia": "2025-12-31",
                "destacado": False,
                "detalles": {
                    "requiere_recibo_sueldo": False,
                    "edad_minima": 21,
                    "edad_maxima": 75,
                    "documentacion": ["CUIT/CUIL", "Últimas 3 DDJJ", "Constancia de inscripción", "Balance último año"],
                    "tipo": "empresarial"
                }
            }
        ]
        
        # Filtros opcionales por query params
        cuotas_max = request.args.get('cuotas_max', type=int)
        destacados = request.args.get('destacados', type=str)
        monto = request.args.get('monto', type=float)
        
        planes_filtrados = planes
        
        # Filtrar por cantidad máxima de cuotas
        if cuotas_max:
            planes_filtrados = [p for p in planes_filtrados if p['cuotas'] <= cuotas_max]
        
        # Filtrar solo destacados
        if destacados and destacados.lower() == 'true':
            planes_filtrados = [p for p in planes_filtrados if p.get('destacado', False)]
        
        # Filtrar por monto del vehículo
        if monto:
            planes_filtrados = [
                p for p in planes_filtrados 
                if p['monto_minimo'] <= monto <= p['monto_maximo']
            ]
        
        logging.info(f"Planes consultados: {len(planes_filtrados)} resultados")
        
        return jsonify(planes_filtrados), 200
        
    except Exception as e:
        logging.error(f"Error al obtener planes: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


# --- ENDPOINT: Calcular Cuota de un Plan ---

@planes_cotizador_bp.route('/api/planes/<plan_id>/calcular', methods=['POST'])
def api_calcular_cuota(plan_id):
    """
    POST /api/planes/{plan_id}/calcular
    
    Calcula la cuota mensual para un plan específico dado un monto.
    
    Body (JSON):
    {
        "monto": 10000000,
        "enganche": 2000000  // opcional
    }
    
    Response:
    {
        "plan_id": "plan-a",
        "monto_financiar": 8000000,
        "cuota_mensual": 666667,
        "total_a_pagar": 8000000,
        "interes_total": 0
    }
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type debe ser application/json"}), 400
        
        datos = request.json
        
        if 'monto' not in datos:
            return jsonify({"error": "Falta el campo requerido: monto"}), 400
        
        monto_total = float(datos['monto'])
        enganche = float(datos.get('enganche', 0))
        
        # Obtener el plan
        response_planes = api_obtener_planes()
        planes = response_planes[0].get_json()
        
        plan = next((p for p in planes if p['id'] == plan_id), None)
        
        if not plan:
            return jsonify({"error": "Plan no encontrado"}), 404
        
        # Validar monto
        if monto_total < plan['monto_minimo'] or monto_total > plan['monto_maximo']:
            return jsonify({
                "error": f"El monto debe estar entre ${plan['monto_minimo']:,.0f} y ${plan['monto_maximo']:,.0f}"
            }), 400
        
        # Validar enganche mínimo
        enganche_minimo = monto_total * (plan['enganche_minimo'] / 100)
        if enganche < enganche_minimo:
            return jsonify({
                "error": f"El enganche mínimo es ${enganche_minimo:,.0f} ({plan['enganche_minimo']}%)"
            }), 400
        
        # Calcular financiación
        monto_financiar = monto_total - enganche
        
        # Calcular interés
        tasa_mensual = plan['tasa_mensual'] / 100
        cuotas = plan['cuotas']
        
        if tasa_mensual == 0:
            # Sin interés
            cuota_mensual = monto_financiar / cuotas
            total_a_pagar = monto_financiar
            interes_total = 0
        else:
            # Con interés - fórmula de amortización francesa
            cuota_mensual = monto_financiar * (tasa_mensual * (1 + tasa_mensual)**cuotas) / ((1 + tasa_mensual)**cuotas - 1)
            total_a_pagar = cuota_mensual * cuotas
            interes_total = total_a_pagar - monto_financiar
        
        resultado = {
            "plan_id": plan_id,
            "plan_nombre": plan['nombre'],
            "monto_vehiculo": int(monto_total),
            "enganche": int(enganche),
            "monto_financiar": int(monto_financiar),
            "cuotas": cuotas,
            "cuota_mensual": int(cuota_mensual),
            "total_a_pagar": int(total_a_pagar),
            "interes_total": int(interes_total),
            "tasa_anual": plan['interes'],
            "tasa_mensual": plan['tasa_mensual']
        }
        
        logging.info(f"Cálculo de cuota para plan {plan_id}: Monto ${monto_total:,.0f}, Cuota ${cuota_mensual:,.0f}")
        
        return jsonify(resultado), 200
        
    except ValueError as e:
        return jsonify({"error": f"Error en los datos: {str(e)}"}), 400
    except Exception as e:
        logging.error(f"Error al calcular cuota: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500