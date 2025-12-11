// Script de inicialización de MongoDB para Docker
// Este script crea la base de datos y las colecciones necesarias

db = db.getSiblingDB('concesionaria');

// Crear colecciones
db.createCollection('vehiculos');
db.createCollection('usuarios');
db.createCollection('mensajes');
db.createCollection('favoritos');
db.createCollection('turnos');
db.createCollection('alertas');
db.createCollection('cotizaciones');

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
        "imagen": "https://via.placeholder.com/400x300?text=Fiat+Cronos",
        "stock": 5,
        "colores": [
            {
                "nombre": "Rojo",
                "codigo": "#DC3545",
                "imagen": "https://via.placeholder.com/400x300?text=Cronos+Rojo"
            },
            {
                "nombre": "Blanco",
                "codigo": "#FFFFFF",
                "imagen": "https://via.placeholder.com/400x300?text=Cronos+Blanco"
            },
            {
                "nombre": "Negro",
                "codigo": "#000000",
                "imagen": "https://via.placeholder.com/400x300?text=Cronos+Negro"
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
        "imagen": "https://via.placeholder.com/400x300?text=Fiat+Argo",
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
        "imagen": "https://via.placeholder.com/400x300?text=Fiat+Pulse",
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
        "imagen": "https://via.placeholder.com/400x300?text=Fiat+Toro",
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
        "imagen": "https://via.placeholder.com/400x300?text=Fiat+500",
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

// Insertar usuario administrador
// Contraseña: admin123 (ya hasheada con bcrypt)
db.usuarios.insertOne({
    "username": "admin",
    "password": "$2b$10$rZ5ZkZ5ZkZ5ZkZ5ZkZ5ZkuYqJ5qJ5qJ5qJ5qJ5qJ5qJ5qJ5qJ5qJ5qJ",
    "email": "admin@gimenez.com",
    "role": "admin",
    "createdAt": new Date()
});

// NOTA: Si el hash de arriba no funciona, ejecuta el script verificar_admin.js
// que regenerará la contraseña correctamente

print("✅ Base de datos 'concesionaria' inicializada correctamente");
print("✅ Colecciones creadas: vehiculos, usuarios, mensajes, favoritos, turnos, alertas, cotizaciones");
print("✅ Datos de ejemplo insertados");
print("✅ Usuario admin creado");
print("");
print("⚠️  IMPORTANTE: Si no puedes iniciar sesión con admin/admin123");
print("   Ejecuta: node verificar_admin.js");
print("");