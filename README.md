# 🚗 Giménez Automotores - Sistema de Gestión de Concesionaria

## 📋 Descripción del Proyecto

**Giménez Automotores** es una aplicación web fullstack para la gestión integral de una concesionaria oficial FIAT. El sistema permite a los clientes explorar vehículos, calcular financiaciones, agendar test drives y contactarse con la empresa, mientras que los administradores pueden gestionar el inventario y atender consultas.

---

##  Características Principales

### 👥 Para Usuarios
- 🔍 **Catálogo de Vehículos**: Exploración completa con filtros avanzados
- 💰 **Cotizador**: Cálculo de valor de vehículos usados
- 📊 **Planes de Financiación**: Simulador de cuotas con múltiples opciones
- ❤️ **Sistema de Favoritos**: Guardar vehículos de interés
- 📅 **Agendamiento de Test Drives**: Reserva de turnos
- 📧 **Formulario de Contacto**: Consultas directas
- 👤 **Gestión de Perfil**: Dashboard personalizado

### 🔐 Para Administradores
- 📦 **Gestión de Inventario**: CRUD completo de vehículos
- 📬 **Bandeja de Mensajes**: Visualización y gestión de consultas
- 📊 **Estadísticas**: Métricas de mensajes no leídos
- 🎯 **Panel de Control**: Administración centralizada

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Node.js** (v16+) - Entorno de ejecución
- **Express.js** - Framework web minimalista
- **MongoDB** - Base de datos NoSQL
- **JWT** - Autenticación con tokens
- **bcryptjs** - Hash de contraseñas
- **CORS** - Configuración de políticas de acceso

### Frontend
- **HTML5** - Estructura semántica
- **CSS3** - Estilos modernos con animaciones
- **JavaScript (Vanilla)** - Lógica del cliente
- **Bootstrap 5** - Framework CSS
- **Bootstrap Icons** - Iconografía

### Infraestructura
- **Docker** - Contenedorización de MongoDB
- **Docker Compose** - Orquestación de servicios

---

## 📁 Estructura del Proyecto

```
GIMENEZ-AUTOMOTORES/
│
├── BACKEND/
│   ├── server.js              # Servidor Express principal
│   ├── package.json           # Dependencias del backend
│   ├── docker-compose.yml     # Configuración de MongoDB
│   ├── init-mongo.js          # Script de inicialización de BD
│   ├── .env                   # Variables de entorno (crear)
│   └── requests.http          # Tests de API
│
├── FRONTEND/
│   ├── index.html             # Página principal
│   ├── catalogo.html          # Catálogo de vehículos
│   ├── detalle_vehiculo.html  # Detalle individual
│   ├── planes.html            # Planes de financiación
│   ├── cotizador.html         # Cotizador de usados
│   ├── contacto.html          # Formulario de contacto
│   ├── quienes_somos.html     # Información institucional
│   ├── login.html             # Inicio de sesión
│   ├── register.html          # Registro de usuarios
│   ├── admin_vehiculos.html   # Panel admin de vehículos
│   ├── admin_mensajes.html    # Panel admin de mensajes
│   └── static/
│       ├── css/
│       │   └── styles.css     # Estilos globales
│       └── img/               # Imágenes de vehículos
│
└── README.md                  # Este archivo
```

---

## 🚀 Instalación y Configuración

### Prerequisitos

Asegúrate de tener instalado:
- **Node.js** v16 o superior ([Descargar](https://nodejs.org/))
- **Docker Desktop** ([Descargar](https://www.docker.com/products/docker-desktop))
- **Git** ([Descargar](https://git-scm.com/))

### Paso 1: Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd GIMENEZ-AUTOMOTORES
```

### Paso 2: Configurar MongoDB con Docker

```bash
cd BACKEND
docker-compose up -d
```

Este comando:
- ✅ Descarga la imagen de MongoDB 7.0
- ✅ Crea un contenedor con la base de datos
- ✅ Inicializa datos de prueba (5 vehículos + 1 admin)
- ✅ Configura MongoDB en `localhost:27017`

**Verificar que MongoDB esté corriendo:**
```bash
docker-compose ps
```

### Paso 3: Instalar Dependencias del Backend

```bash
npm install
```

### Paso 4: Configurar Variables de Entorno

Crea un archivo `.env` en la carpeta `BACKEND/` con:

```env
PORT=3000
JWT_SECRET=tu_secreto_super_seguro
MONGO_URL=mongodb://admin:admin123@localhost:27017/concesionaria?authSource=admin
```

### Paso 5: Iniciar el Backend

```bash
npm start
```

El servidor estará disponible en: **http://localhost:3000**

### Paso 6: Abrir el Frontend

Abre el archivo `FRONTEND/index.html` en tu navegador, o utiliza **Live Server** en VS Code.

**Alternativamente, con Python:**
```bash
cd FRONTEND
python -m http.server 8000
```

Luego abre: **http://localhost:8000**

---

## 👨‍💻 Credenciales de Prueba

### Usuario Administrador
- **Usuario:** `admin`
- **Contraseña:** `admin123`
- **Permisos:** Gestión completa del sistema

### Crear Usuario Normal
Registrarse desde: `http://localhost:8000/register.html`

---

## 🧪 Probar la API

### Opción 1: Con REST Client (VS Code)

1. Instala la extensión **REST Client** en VS Code
2. Abre el archivo `BACKEND/requests.http`
3. Haz clic en "Send Request" sobre cada endpoint

### Opción 2: Con cURL

```bash
# Health check
curl http://localhost:3000/api/health

# Login
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Obtener vehículos
curl http://localhost:3000/api/vehiculos
```

### Opción 3: Con Postman

Importa las siguientes colecciones desde `requests.http`

---

## 📡 Endpoints Principales

### Autenticación
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Obtener usuario actual (requiere token)

### Vehículos
- `GET /api/vehiculos` - Listar todos
- `GET /api/vehiculos/destacados` - Obtener destacados
- `GET /api/vehiculos/:id` - Obtener por ID
- `POST /api/vehiculos` - Crear (solo admin)
- `PUT /api/vehiculos/:id` - Actualizar (solo admin)
- `DELETE /api/vehiculos/:id` - Eliminar (solo admin)

### Mensajes
- `POST /api/mensajes` - Enviar mensaje (público)
- `GET /api/mensajes` - Listar mensajes (solo admin)
- `PUT /api/mensajes/:id/leido` - Marcar como leído (solo admin)
- `DELETE /api/mensajes/:id` - Eliminar mensaje (solo admin)
- `GET /api/mensajes/stats` - Estadísticas (solo admin)

### Cotizador
- `POST /api/cotizador` - Cotizar vehículo usado (público)

### Planes
- `GET /api/planes` - Obtener planes de financiación
- `POST /api/planes/:planId/calcular` - Calcular cuota

### Favoritos
- `POST /api/favoritos` - Agregar favorito (requiere auth)
- `GET /api/favoritos` - Obtener favoritos (requiere auth)
- `DELETE /api/favoritos/:vehiculoId` - Eliminar favorito (requiere auth)

### Turnos
- `POST /api/turnos` - Agendar turno (requiere auth)
- `GET /api/turnos` - Obtener turnos (requiere auth)
- `DELETE /api/turnos/:id` - Cancelar turno (requiere auth)

---

## 🎨 Características del Frontend

### Diseño Premium
- Gradientes animados en heroes
- Efectos hover con translateY y box-shadow
- Animaciones suaves (fadeInUp, bgMove, float)
- Cards con diseño moderno y elevación
- Formularios con iconos y estados de focus
- Responsive design para mobile, tablet y desktop

### Funcionalidades Interactivas
- Filtros de búsqueda en tiempo real
- Calculadora de cuotas con resultados dinámicos
- Validación de formularios en el cliente
- Alertas de éxito/error con Bootstrap
- Sistema de navegación condicional según rol

---

## 🔒 Seguridad

- ✅ **Hash de contraseñas** con bcryptjs (salt rounds: 10)
- ✅ **Autenticación JWT** con expiración de 7 días
- ✅ **Validación de datos** en backend y frontend
- ✅ **Autorización por roles** (admin/usuario)
- ✅ **CORS configurado** para desarrollo

---

## 🐳 Gestión de Docker

### Comandos Útiles

```bash
# Iniciar MongoDB
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener MongoDB
docker-compose down

# Reiniciar MongoDB
docker-compose restart

# Eliminar todo (incluye datos)
docker-compose down -v

# Ver estado
docker-compose ps
```

### Acceso a Mongo Express (Opcional)

Si habilitaste Mongo Express en `docker-compose.yml`:
- **URL:** http://localhost:8081
- **Usuario:** admin
- **Contraseña:** admin123

---

## 📊 Datos Precargados

La base de datos se inicializa con:

### Vehículos (5 unidades)
- Fiat Cronos 2024 - $15.000.000
- Fiat Argo 2024 - $12.000.000
- Fiat Pulse 2024 - $32.000.000
- Fiat Toro 2024 - $23.000.000
- Fiat 500 2024 - $18.000.000

### Usuario Administrador
- Username: `admin`
- Password: `admin123`
- Email: admin@gimenez.com

---

## 🐛 Troubleshooting

### Error: "Cannot connect to MongoDB"
```bash
# Verificar que Docker esté corriendo
docker ps

# Reiniciar el contenedor
docker-compose restart mongodb
```

### Error: "Port 3000 already in use"
```bash
# Cambiar el puerto en .env
PORT=3001

# O matar el proceso
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:3000 | xargs kill -9
```

### Error: "CORS policy blocked"
Verifica que el frontend esté accediendo a `http://localhost:3000` y no a otra URL.

### MongoDB no inicia
```bash
# Eliminar volúmenes y reintentar
docker-compose down -v
docker-compose up -d
```

---

## 📝 Scripts NPM

```json
{
  "start": "node server.js",      // Iniciar servidor
  "dev": "nodemon server.js",     // Desarrollo con auto-reload
  "test": "echo \"No tests yet\""
}
```
