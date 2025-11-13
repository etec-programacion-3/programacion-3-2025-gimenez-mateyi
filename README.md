# 🚗 Giménez Automotores - Sistema de Gestión de Concesionaria

**Proyecto Final - Programación 3**  
**Alumno:** Mateo Giménez  
**Institución:** ETEC  
**Año:** 2025

---

## 📋 Descripción del Proyecto

**Giménez Automotores** es una aplicación web completa para la gestión de un concesionario oficial FIAT. El sistema permite a los clientes explorar vehículos, realizar cotizaciones, agendar test drives y contactar con la concesionaria. Los administradores pueden gestionar el catálogo de vehículos y revisar mensajes de clientes.

### 🎯 Funcionalidades Principales

#### Para Usuarios:
- ✅ Explorar catálogo de vehículos con filtros
- ✅ Ver detalles completos de cada modelo (especificaciones, colores, galería)
- ✅ Cotizar vehículos usados
- ✅ Solicitar información y test drives
- ✅ Sistema de favoritos
- ✅ Registro e inicio de sesión

#### Para Administradores:
- ✅ CRUD completo de vehículos (Crear, Leer, Actualizar, Eliminar)
- ✅ Gestión de mensajes de clientes
- ✅ Panel de administración con estadísticas
- ✅ Control de stock

---

## 🚀 Inicio Rápido (3 Pasos)

```bash
# 1. Iniciar MongoDB con Docker
docker-compose up -d

# 2. Configurar e instalar
cd BACKEND
cp .env.local .env
pip install -r requirements.txt

# 3. Ejecutar
python app.py
```

**Abrir:** http://127.0.0.1:5002  
**Login Admin:** `admin` / `admin123`

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.10+**
- **Flask 3.0.0** - Framework web
- **Flask-Login 0.6.3** - Autenticación de usuarios
- **PyMongo 4.6.1** - Driver de MongoDB
- **bcrypt 4.1.2** - Hash de contraseñas
- **python-dotenv 1.0.0** - Variables de entorno

### Frontend
- **HTML5, CSS3, JavaScript**
- **Bootstrap 5.3.0** - Framework CSS
- **Bootstrap Icons 1.11.1** - Iconografía
- **Swiper 11** - Carruseles de imágenes

### Base de Datos
- **MongoDB 7.0** - Base de datos NoSQL (Docker)
- **Mongo Express 1.0** - Interfaz web para administrar BD (opcional)

### DevOps
- **Docker & Docker Compose** - Orquestación de contenedores

---

## 📁 Estructura del Proyecto

```
programacion-3-2025-gimenez-mateyi-2/
│
├── docker-compose.yml              # Configuración Docker
├── init-mongo.js                   # Script de inicialización BD
├── README.md                       # Este archivo
├── requests.http                   # Pruebas de API (REST Client)
├── .gitignore                      # Archivos ignorados por Git
│
├── BACKEND/
│   ├── app.py                      # Aplicación Flask principal
│   ├── models.py                   # Modelos y conexión MongoDB
│   ├── requirements.txt            # Dependencias Python
│   ├── .env.local                  # Plantilla de configuración
│   └── routes/
│       ├── auth.py                 # Autenticación
│       ├── vehiculos.py            # Gestión de vehículos
│       ├── usuarios.py             # Gestión de usuarios
│       ├── mensajes.py             # Mensajes de contacto
│       └── planes_cotizador.py     # Cotizador
│
└── FRONTEND/
    ├── templates/                  # Plantillas HTML
    │   ├── base.html              # Plantilla base
    │   ├── index.html             # Página de inicio
    │   ├── catalogo.html          # Catálogo de vehículos
    │   ├── detalle_vehiculo.html  # Detalle de vehículo
    │   ├── quienes_somos.html     # Quiénes somos
    │   ├── planes.html            # Planes de financiación
    │   ├── cotizador.html         # Cotizador de usados
    │   ├── contacto.html          # Formulario de contacto
    │   ├── login.html             # Inicio de sesión
    │   ├── register.html          # Registro
    │   ├── admin_vehiculos.html   # Panel admin vehículos
    │   └── admin_mensajes.html    # Panel admin mensajes
    │
    └── static/
        ├── css/
        │   └── styles.css         # Estilos personalizados
        └── img/                   # Imágenes de vehículos
```

---

## 🗄️ Base de Datos

### Configuración con Docker

La base de datos MongoDB corre en un contenedor Docker con los siguientes servicios:

```yaml
services:
  mongodb:           # Base de datos MongoDB
  mongo-express:     # Interfaz web (opcional)
```

### Estructura de Datos

**Base de datos:** `concesionaria`

#### Colección: `vehiculos`
```javascript
{
  "_id": ObjectId("..."),
  "modelo": "Fiat Cronos",
  "precio": 15000000,
  "anio": 2024,
  "descripcion": "Sedán moderno...",
  "imagen": "/static/img/fiat-cronos.png",
  "stock": 5,
  "especificaciones": {
    "motor": "1.8L 16v E.torQ",
    "potencia": "130 CV",
    "transmision": "Manual 5 velocidades",
    "combustible": "Nafta"
  }
}
```

#### Colección: `usuarios`
```javascript
{
  "_id": ObjectId("..."),
  "username": "admin",
  "password": "$2b$12$...",  // Hash bcrypt
  "email": "admin@gimenez.com",
  "role": "admin"  // 'admin' o 'usuario'
}
```

#### Colección: `mensajes`
```javascript
{
  "_id": ObjectId("..."),
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "telefono": "261-1234567",
  "mensaje": "Consulta sobre Fiat Cronos",
  "leido": false
}
```

---

## 🔧 Instalación Detallada

### Prerrequisitos

- **Docker Desktop** o **Docker + Docker Compose**
- **Python 3.10+**
- **Git**
- **pip** (gestor de paquetes Python)

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/etec-programacion-3/programacion-3-2025-gimenez-mateyi-2.git
cd programacion-3-2025-gimenez-mateyi-2
```

### Paso 2: Iniciar MongoDB con Docker

```bash
# Iniciar servicios en segundo plano
docker-compose up -d

# Verificar que están corriendo
docker-compose ps
```

Deberías ver:
```
NAME                      STATUS          PORTS
gimenez-mongodb          Up (healthy)    0.0.0.0:27017->27017/tcp
gimenez-mongo-express    Up              0.0.0.0:8081->8081/tcp
```

**⏱️ Tiempo:** ~30-60 segundos (primera vez descarga las imágenes)

### Paso 3: Configurar Variables de Entorno

```bash
cd BACKEND
cp .env.local .env
```

El archivo `.env` contiene:
```env
MONGO_URL=mongodb://admin:admin123@localhost:27017/concesionaria?authSource=admin
SECRET_KEY=clave_secreta_para_evaluacion_prog3_2025
```

### Paso 4: Instalar Dependencias Python

```bash
# Asegurarse de estar en BACKEND/
pip install -r requirements.txt
```

**Dependencias instaladas:**
- Flask 3.0.0
- Flask-Login 0.6.3
- pymongo 4.6.1
- bcrypt 4.1.2
- python-dotenv 1.0.0
- Werkzeug 3.0.1

### Paso 5: Verificar Datos en MongoDB

```bash
# Verificar que se cargaron los vehículos
docker exec -it gimenez-mongodb mongosh -u admin -p admin123 --authenticationDatabase admin -eval "use concesionaria; db.vehiculos.find().count()"
```

Debería mostrar: `5` (5 vehículos)

### Paso 6: Ejecutar la Aplicación

```bash
python app.py
```

Deberías ver:
```
============================================================
🚗 GIMÉNEZ AUTOMOTORES - SERVIDOR INICIANDO
============================================================
📍 URL: http://127.0.0.1:5002
🔗 MongoDB: Conectado
🔐 Login: http://127.0.0.1:5002/login
============================================================
```

### Paso 7: Acceder a la Aplicación

- **Web:** http://127.0.0.1:5002
- **Mongo Express (opcional):** http://localhost:8081
  - Usuario: `admin`
  - Contraseña: `admin123`

---

## 👤 Credenciales de Prueba

### Administrador
- **Usuario:** `admin`
- **Contraseña:** `admin123`
- **URL Login:** http://127.0.0.1:5002/login

**Funcionalidades del admin:**
- CRUD completo de vehículos
- Visualización de mensajes de clientes
- Panel de administración

### Usuario Regular
Puede registrarse desde: http://127.0.0.1:5002/register

---

## 🧪 Probar la API

### Opción 1: REST Client (VS Code)

1. Instalar extensión "REST Client" en VS Code
2. Abrir archivo `requests.http`
3. Click en "Send Request" sobre cada petición

### Opción 2: Postman

1. Importar `Gimenez_Automotores.postman_collection.json`
2. Ejecutar peticiones

### Opción 3: curl (Terminal)

```bash
# Ver vehículos destacados
curl http://127.0.0.1:5002/api/vehiculos/destacados

# Login admin
curl -X POST http://127.0.0.1:5002/login \
  -d "username=admin&password=admin123"
```

---

## 📊 Endpoints Principales

### Páginas Públicas
```
GET  /                          → Página de inicio
GET  /catalogo                  → Lista de vehículos
GET  /vehiculo/<id>            → Detalle de vehículo
POST /cotizador                → Cotizar usado
POST /contacto                 → Enviar mensaje
GET  /quienes-somos            → Información
GET  /planes                   → Planes de financiación
```

### Autenticación
```
POST /register                 → Registrar usuario
POST /login                    → Iniciar sesión
GET  /logout                   → Cerrar sesión
```

### Admin (requiere login como admin)
```
GET  /admin/vehiculos          → Panel de administración
POST /admin/vehiculo/crear     → Crear vehículo
POST /admin/vehiculo/editar/:id → Editar vehículo
POST /admin/vehiculo/eliminar/:id → Eliminar vehículo
GET  /admin/mensajes           → Ver mensajes
```

### API REST (JSON)
```
GET /api/vehiculos/destacados  → Vehículos destacados
GET /api/mensajes/stats        → Estadísticas mensajes
```

---

## 🐳 Comandos de Docker

```bash
# Iniciar servicios
docker-compose up -d

# Ver estado
docker-compose ps

# Ver logs
docker-compose logs -f

# Ver logs solo de MongoDB
docker-compose logs -f mongodb

# Reiniciar servicios
docker-compose restart

# Detener servicios
docker-compose down

# Detener y eliminar datos (⚠️ borra todo)
docker-compose down -v

# Acceder a MongoDB shell
docker exec -it gimenez-mongodb mongosh -u admin -p admin123 --authenticationDatabase admin
```

---

## ✅ Verificación del Sistema

### Test 1: Docker está corriendo
```bash
docker-compose ps
```
Debería mostrar 2 contenedores: `mongodb` y `mongo-express`

### Test 2: Conexión Python a MongoDB
```bash
cd BACKEND
python -c "from models import VehiculoDB; db = VehiculoDB(); print('✅ Conectado' if db.client else '❌ Error')"
```

### Test 3: Datos en la base de datos
```bash
python -c "from models import VehiculoDB; db = VehiculoDB(); print(f'Vehículos: {len(db.obtener_vehiculos())}')"
```
Debería mostrar: `Vehículos: 5`

### Test 4: Servidor web funcionando
```bash
curl http://127.0.0.1:5002/
```
Debería retornar HTML

---

## 🎨 Características de Diseño

- ✅ Diseño responsive (mobile-first)
- ✅ Animaciones CSS modernas
- ✅ Efectos de hover 3D en cards
- ✅ Gradientes y glassmorphism
- ✅ Partículas flotantes animadas en hero
- ✅ Hero sections con overlays dinámicos
- ✅ Cards premium con sombras dinámicas
- ✅ Paleta de colores consistente (rojo FIAT + azul/morado)
- ✅ Selector de colores interactivo por vehículo

---

## 🔐 Seguridad

- **Contraseñas:** Hasheadas con bcrypt (12 rounds)
- **Sesiones:** Gestionadas con Flask-Login
- **Validación:** Inputs sanitizados en frontend y backend
- **Roles:** Sistema RBAC (admin/usuario)
- **Variables sensibles:** Almacenadas en .env (no incluidas en Git)
- **CORS:** Configurado para localhost
- **SQL Injection:** Prevenido (uso de MongoDB con PyMongo)

---

## ❌ Solución de Problemas

### Docker no inicia
```bash
# Verificar que Docker Desktop está corriendo
docker --version
docker-compose --version

# En Linux, iniciar servicio
sudo systemctl start docker
```

### Puerto 27017 ocupado
```bash
# Detener MongoDB local si está corriendo
sudo systemctl stop mongod  # Linux
net stop MongoDB            # Windows
```

### Error de conexión a MongoDB
```bash
# Verificar que MongoDB está corriendo
docker-compose ps

# Ver logs para más detalles
docker-compose logs mongodb

# Reiniciar servicios
docker-compose restart
```

### No aparecen vehículos en el catálogo
```bash
# Verificar datos en MongoDB
docker exec -it gimenez-mongodb mongosh -u admin -p admin123 --authenticationDatabase admin

# Dentro de mongosh:
use concesionaria
db.vehiculos.find().count()  # Debería ser 5
exit

# Si muestra 0, reiniciar con volúmenes limpios:
docker-compose down -v
docker-compose up -d
```

### Error "ModuleNotFoundError"
```bash
pip install -r requirements.txt --force-reinstall
```

### Error 405: Method Not Allowed
Verificar que las rutas acepten POST:
```python
@app.route('/cotizador', methods=['GET', 'POST'])
```

---

## 📝 Notas para el Profesor

### Evaluación del Proyecto

Este proyecto implementa:

1. **Backend con Flask:**
   - Arquitectura MVC
   - Blueprints para organización modular
   - Manejo de sesiones y autenticación
   - CRUD completo de vehículos
   - API RESTful

2. **Base de Datos MongoDB:**
   - 3 colecciones (vehiculos, usuarios, mensajes)
   - Operaciones CRUD
   - Índices y validaciones
   - Configuración con Docker Compose

3. **Frontend Responsive:**
   - HTML5 semántico
   - CSS3 con animaciones avanzadas
   - JavaScript vanilla para interactividad
   - Bootstrap 5 para diseño responsive

4. **Docker & DevOps:**
   - docker-compose.yml funcional
   - Script de inicialización (init-mongo.js)
   - Volúmenes persistentes
   - Health checks configurados

5. **Seguridad:**
   - Hash de contraseñas con bcrypt
   - Sistema de roles (RBAC)
   - Protección de rutas
   - Variables de entorno

6. **Testing:**
   - Archivo requests.http con 25+ peticiones
   - Colección de Postman incluida
   - Scripts de verificación

---

