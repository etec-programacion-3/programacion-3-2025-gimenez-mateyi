# API Documentation - Giménez Automotores

## Endpoints de Cotización y Planes

### 1. Cotizar Vehículo Usado

**Endpoint:** `POST /api/cotizar`

**Descripción:** Calcula el valor estimado de un vehículo usado.

**Request Body:**
```json
{
  "marca": "Fiat",
  "modelo": "Cronos",
  "anio": 2020,
  "estado": "bueno"
}
```

**Parámetros:**
- `marca` (string, requerido): Marca del vehículo
- `modelo` (string, requerido): Modelo del vehículo
- `anio` (integer, requerido): Año de fabricación (1990-2026)
- `estado` (string, requerido): Estado del vehículo - `"excelente"`, `"bueno"`, o `"regular"`

**Response 200:**
```json
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
    "factor_marca": 1.1,
    "antiguedad_anios": 5,
    "deprecacion_anual": "10%",
    "moneda": "ARS"
  }
}
```

**Ejemplo con cURL:**
```bash
curl -X POST http://localhost:5002/api/cotizar \
  -H "Content-Type: application/json" \
  -d '{
    "marca": "Fiat",
    "modelo": "Argo",
    "anio": 2022,
    "estado": "excelente"
  }'
```

---

### 2. Obtener Planes de Financiación

**Endpoint:** `GET /api/planes`

**Descripción:** Devuelve todos los planes de financiación disponibles.

**Query Parameters (opcionales):**
- `cuotas_max` (integer): Filtrar planes con cuotas menores o iguales
- `destacados` (boolean): Solo planes destacados (`true`/`false`)
- `monto` (float): Filtrar planes compatibles con el monto del vehículo

**Response 200:**
```json
[
  {
    "id": "plan-a",
    "nombre": "Plan 12 Cuotas Sin Interés",
    "descripcion": "Ideal para compras rápidas...",
    "cuotas": 12,
    "interes": 0,
    "tasa_mensual": 0,
    "enganche_minimo": 20,
    "monto_minimo": 5000000,
    "monto_maximo": 15000000,
    "vigencia": "2025-12-31",
    "destacado": true,
    "detalles": {
      "requiere_recibo_sueldo": true,
      "edad_minima": 18,
      "edad_maxima": 75,
      "documentacion": ["DNI", "Recibo de sueldo", "Servicio a nombre"]
    }
  }
]
```

**Ejemplos:**
```bash
# Obtener todos los planes
curl http://localhost:5002/api/planes

# Solo planes destacados
curl http://localhost:5002/api/planes?destacados=true

# Planes hasta 24 cuotas
curl http://localhost:5002/api/planes?cuotas_max=24

# Planes para un monto específico
curl http://localhost:5002/api/planes?monto=10000000
```

---

### 3. Calcular Cuota Mensual

**Endpoint:** `POST /api/planes/{plan_id}/calcular`

**Descripción:** Calcula la cuota mensual para un plan específico.

**Path Parameters:**
- `plan_id` (string): ID del plan (ej: `plan-a`)

**Request Body:**
```json
{
  "monto": 10000000,
  "enganche": 2000000
}
```

**Parámetros:**
- `monto` (float, requerido): Monto total del vehículo
- `enganche` (float, opcional): Monto del enganche (por defecto: 0)

**Response 200:**
```json
{
  "plan_id": "plan-a",
  "plan_nombre": "Plan 12 Cuotas Sin Interés",
  "monto_vehiculo": 10000000,
  "enganche": 2000000,
  "monto_financiar": 8000000,
  "cuotas": 12,
  "cuota_mensual": 666667,
  "total_a_pagar": 8000000,
  "interes_total": 0,
  "tasa_anual": 0,
  "tasa_mensual": 0
}
```

**Ejemplo:**
```bash
curl -X POST http://localhost:5002/api/planes/plan-a/calcular \
  -H "Content-Type: application/json" \
  -d '{
    "monto": 10000000,
    "enganche": 2000000
  }'
```

---

## Códigos de Error

- `400 Bad Request`: Datos inválidos o faltantes
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor