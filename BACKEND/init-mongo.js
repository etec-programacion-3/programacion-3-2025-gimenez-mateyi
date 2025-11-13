// Script de inicialización de MongoDB para Docker
// Este script crea la base de datos y las colecciones necesarias

db = db.getSiblingDB('concesionaria');

// Crear colecciones
db.createCollection('vehiculos');
db.createCollection('usuarios');
db.createCollection('mensajes');

// Crear índices
db.vehiculos.createIndex({ "modelo": 1 });
db.usuarios.createIndex({ "username": 1 }, { unique: true });
db.usuarios.createIndex({ "email": 1 }, { unique: true });

// Insertar datos de ejemplo - Vehículos
db.vehiculos.insertMany([
    {
        "modelo": "Fiat Cronos",
        "precio": 15000000,
        "anio": 2024,
        "descripcion": "Sedán moderno con tecnología avanzada y confort.",
        "imagen": "/static/img/fiat-cronos.png",
        "stock": 5,
        "colores": [
            {
                "nombre": "Rojo",
                "codigo": "#DC3545",
                "imagen": "/static/img/cronos-rojo.png"
            },
            {
                "nombre": "Blanco",
                "codigo": "#FFFFFF",
                "imagen": "/static/img/cronos-blanco.png"
            },
            {
                "nombre": "Negro",
                "codigo": "#000000",
                "imagen": "/static/img/cronos-negro.png"
            }
        ],
        "especificaciones": {
            "motor": "1.8L 16v E.torQ",
            "potencia": "130 CV",
            "transmision": "Manual 5 velocidades",
            "combustible": "Nafta",
            "capacidad": "5 personas",
            "baul": "525 litros"
        }
    },
    {
        "modelo": "Fiat Argo",
        "precio": 12000000,
        "anio": 2024,
        "descripcion": "Auto compacto y eficiente, perfecto para la ciudad.",
        "imagen": "/static/img/fiat-argo.png",
        "stock": 8,
        "especificaciones": {
            "motor": "1.3L 8v Firefly",
            "potencia": "99 CV",
            "transmision": "Manual 5 velocidades",
            "combustible": "Nafta",
            "capacidad": "5 personas",
            "baul": "300 litros"
        }
    },
    {
        "modelo": "Fiat Pulse",
        "precio": 32000000,
        "anio": 2024,
        "descripcion": "SUV compacta moderna con diseño innovador y tecnología avanzada. Perfecta para la ciudad y aventuras.",
        "imagen": "/static/img/fiat-pulse.png",
        "stock": 3,
        "especificaciones": {
            "motor": "1.0L Turbo 200",
            "potencia": "130 CV",
            "transmision": "Automática CVT",
            "combustible": "Nafta",
            "capacidad": "5 personas",
            "baul": "400 litros"
        }
    },
    {
        "modelo": "Fiat Toro",
        "precio": 23000000,
        "anio": 2024,
        "descripcion": "Pickup robusta y versátil. Potencia, confort y capacidad de carga para trabajo y aventura.",
        "imagen": "/static/img/fiat-toro.png",
        "stock": 4,
        "especificaciones": {
            "motor": "2.0L 16v Turbo Diesel",
            "potencia": "170 CV",
            "transmision": "Automática 9 velocidades",
            "combustible": "Diesel",
            "capacidad": "5 personas",
            "carga": "1000 kg"
        }
    },
    {
        "modelo": "Fiat 500",
        "precio": 18000000,
        "anio": 2024,
        "descripcion": "Ícono italiano de estilo y elegancia. Compacto, urbano y con personalidad única para la ciudad.",
        "imagen": "/static/img/fiat-500.png",
        "stock": 6,
        "especificaciones": {
            "motor": "1.2L 8v Fire",
            "potencia": "69 CV",
            "transmision": "Manual 5 velocidades",
            "combustible": "Nafta",
            "capacidad": "4 personas",
            "baul": "185 litros"
        }
    }
]);

// Insertar usuario administrador (contraseña: admin123 - ya hasheada)
db.usuarios.insertOne({
    "username": "admin",
    "password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5FS2jM5JXw4qe",
    "email": "admin@gimenez.com",
    "role": "admin"
});

print("✅ Base de datos 'concesionaria' inicializada correctamente");
print("✅ Colecciones creadas: vehiculos, usuarios, mensajes");
print("✅ Datos de ejemplo insertados");
print("✅ Usuario admin creado (username: admin, password: admin123)");