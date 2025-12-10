// ==================== BACKEND NODE.JS + EXPRESS ====================
// Servidor backend independiente para Giménez Automotores
// Alumno: Mateo Giménez - ETEC 2025

const express = require('express');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { MongoClient, ObjectId } = require('mongodb');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'secret_super_seguro_cambiar_en_produccion';
const MONGO_URL = process.env.MONGO_URL || 'mongodb://admin:admin123@localhost:27017/concesionaria?authSource=admin';

// ==================== MIDDLEWARES ====================
app.use(cors({
  origin: '*', // Permite cualquier origen (frontend en otra PC)
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Logger de requests
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
  next();
});

// ==================== CONEXIÓN A MONGODB ====================
let db;
let vehiculosCollection;
let usuariosCollection;
let mensajesCollection;
let favoritosCollection;
let turnosCollection;

async function connectDB() {
  try {
    const client = await MongoClient.connect(MONGO_URL, {
      useNewUrlParser: true,
      useUnifiedTopology: true
    });
    
    db = client.db('concesionaria');
    vehiculosCollection = db.collection('vehiculos');
    usuariosCollection = db.collection('usuarios');
    mensajesCollection = db.collection('mensajes');
    favoritosCollection = db.collection('favoritos');
    turnosCollection = db.collection('turnos');
    
    console.log('✅ Conectado a MongoDB');
    
    // Crear índices
    await usuariosCollection.createIndex({ username: 1 }, { unique: true });
    await usuariosCollection.createIndex({ email: 1 }, { unique: true });
    
  } catch (error) {
    console.error('❌ Error al conectar a MongoDB:', error);
    process.exit(1);
  }
}

// ==================== MIDDLEWARE DE AUTENTICACIÓN ====================
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN
  
  if (!token) {
    return res.status(401).json({ error: 'Token no proporcionado' });
  }
  
  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Token inválido' });
    }
    req.user = user;
    next();
  });
}

function isAdmin(req, res, next) {
  if (req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Acceso denegado. Solo administradores' });
  }
  next();
}

// ==================== RUTAS DE AUTENTICACIÓN ====================

// POST /api/auth/register - Registrar usuario
app.post('/api/auth/register', async (req, res) => {
  try {
    const { username, email, password } = req.body;
    
    // Validaciones
    if (!username || !email || !password) {
      return res.status(400).json({ error: 'Faltan campos requeridos' });
    }
    
    if (username.length < 3) {
      return res.status(400).json({ error: 'El username debe tener al menos 3 caracteres' });
    }
    
    if (password.length < 6) {
      return res.status(400).json({ error: 'La contraseña debe tener al menos 6 caracteres' });
    }
    
    // Verificar si el usuario ya existe
    const existeUsername = await usuariosCollection.findOne({ username });
    if (existeUsername) {
      return res.status(400).json({ error: 'El username ya está en uso' });
    }
    
    const existeEmail = await usuariosCollection.findOne({ email });
    if (existeEmail) {
      return res.status(400).json({ error: 'El email ya está registrado' });
    }
    
    // Hash de la contraseña
    const hashedPassword = await bcrypt.hash(password, 10);
    
    // Crear usuario
    const nuevoUsuario = {
      username: username.toLowerCase(),
      email: email.toLowerCase(),
      password: hashedPassword,
      role: 'usuario',
      createdAt: new Date()
    };
    
    const resultado = await usuariosCollection.insertOne(nuevoUsuario);
    
    res.status(201).json({
      message: 'Usuario creado exitosamente',
      userId: resultado.insertedId
    });
    
  } catch (error) {
    console.error('Error en register:', error);
    res.status(500).json({ error: 'Error al crear usuario' });
  }
});

// POST /api/auth/login - Iniciar sesión
app.post('/api/auth/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    
    if (!username || !password) {
      return res.status(400).json({ error: 'Username y password son requeridos' });
    }
    
    // Buscar usuario
    const usuario = await usuariosCollection.findOne({ 
      username: username.toLowerCase() 
    });
    
    if (!usuario) {
      return res.status(401).json({ error: 'Credenciales inválidas' });
    }
    
    // Verificar contraseña
    const passwordValida = await bcrypt.compare(password, usuario.password);
    
    if (!passwordValida) {
      return res.status(401).json({ error: 'Credenciales inválidas' });
    }
    
    // Generar token JWT
    const token = jwt.sign(
      { 
        userId: usuario._id.toString(), 
        username: usuario.username,
        role: usuario.role 
      },
      JWT_SECRET,
      { expiresIn: '7d' }
    );
    
    res.json({
      message: 'Login exitoso',
      token,
      user: {
        id: usuario._id,
        username: usuario.username,
        email: usuario.email,
        role: usuario.role
      }
    });
    
  } catch (error) {
    console.error('Error en login:', error);
    res.status(500).json({ error: 'Error al iniciar sesión' });
  }
});

// GET /api/auth/me - Obtener usuario actual
app.get('/api/auth/me', authenticateToken, async (req, res) => {
  try {
    const usuario = await usuariosCollection.findOne(
      { _id: new ObjectId(req.user.userId) },
      { projection: { password: 0 } }
    );
    
    if (!usuario) {
      return res.status(404).json({ error: 'Usuario no encontrado' });
    }
    
    res.json(usuario);
    
  } catch (error) {
    console.error('Error en /me:', error);
    res.status(500).json({ error: 'Error al obtener usuario' });
  }
});

// ==================== RUTAS DE VEHÍCULOS ====================

// GET /api/vehiculos - Obtener todos los vehículos
app.get('/api/vehiculos', async (req, res) => {
  try {
    const vehiculos = await vehiculosCollection.find({}).toArray();
    
    // Convertir ObjectId a string
    const vehiculosFormateados = vehiculos.map(v => ({
      ...v,
      _id: v._id.toString()
    }));
    
    res.json(vehiculosFormateados);
    
  } catch (error) {
    console.error('Error al obtener vehículos:', error);
    res.status(500).json({ error: 'Error al obtener vehículos' });
  }
});

// GET /api/vehiculos/destacados - Vehículos destacados (primeros 3)
app.get('/api/vehiculos/destacados', async (req, res) => {
  try {
    const vehiculos = await vehiculosCollection.find({}).limit(3).toArray();
    
    const vehiculosFormateados = vehiculos.map(v => ({
      ...v,
      _id: v._id.toString()
    }));
    
    res.json(vehiculosFormateados);
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al obtener vehículos destacados' });
  }
});

// GET /api/vehiculos/:id - Obtener un vehículo por ID
app.get('/api/vehiculos/:id', async (req, res) => {
  try {
    const vehiculo = await vehiculosCollection.findOne({ 
      _id: new ObjectId(req.params.id) 
    });
    
    if (!vehiculo) {
      return res.status(404).json({ error: 'Vehículo no encontrado' });
    }
    
    res.json({
      ...vehiculo,
      _id: vehiculo._id.toString()
    });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al obtener vehículo' });
  }
});

// POST /api/vehiculos - Crear vehículo (SOLO ADMIN)
app.post('/api/vehiculos', authenticateToken, isAdmin, async (req, res) => {
  try {
    const { modelo, descripcion, precio, imagen, anio, stock } = req.body;
    
    if (!modelo || !descripcion || !precio || !imagen) {
      return res.status(400).json({ error: 'Faltan campos requeridos' });
    }
    
    const nuevoVehiculo = {
      modelo,
      descripcion,
      precio: parseFloat(precio),
      imagen,
      anio: anio || new Date().getFullYear(),
      stock: stock || 1,
      createdAt: new Date()
    };
    
    const resultado = await vehiculosCollection.insertOne(nuevoVehiculo);
    
    res.status(201).json({
      message: 'Vehículo creado exitosamente',
      _id: resultado.insertedId.toString()
    });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al crear vehículo' });
  }
});

// PUT /api/vehiculos/:id - Actualizar vehículo (SOLO ADMIN)
app.put('/api/vehiculos/:id', authenticateToken, isAdmin, async (req, res) => {
  try {
    const { modelo, descripcion, precio, imagen, anio, stock } = req.body;
    
    const datosActualizar = {};
    if (modelo) datosActualizar.modelo = modelo;
    if (descripcion) datosActualizar.descripcion = descripcion;
    if (precio) datosActualizar.precio = parseFloat(precio);
    if (imagen) datosActualizar.imagen = imagen;
    if (anio) datosActualizar.anio = anio;
    if (stock !== undefined) datosActualizar.stock = stock;
    
    const resultado = await vehiculosCollection.updateOne(
      { _id: new ObjectId(req.params.id) },
      { $set: datosActualizar }
    );
    
    if (resultado.matchedCount === 0) {
      return res.status(404).json({ error: 'Vehículo no encontrado' });
    }
    
    res.json({ message: 'Vehículo actualizado exitosamente' });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al actualizar vehículo' });
  }
});

// DELETE /api/vehiculos/:id - Eliminar vehículo (SOLO ADMIN)
app.delete('/api/vehiculos/:id', authenticateToken, isAdmin, async (req, res) => {
  try {
    const resultado = await vehiculosCollection.deleteOne({ 
      _id: new ObjectId(req.params.id) 
    });
    
    if (resultado.deletedCount === 0) {
      return res.status(404).json({ error: 'Vehículo no encontrado' });
    }
    
    res.json({ message: 'Vehículo eliminado exitosamente' });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al eliminar vehículo' });
  }
});

// ==================== RUTAS DE MENSAJES ====================

// POST /api/mensajes - Crear mensaje de contacto (PÚBLICO)
app.post('/api/mensajes', async (req, res) => {
  try {
    const { nombre, email, telefono, mensaje } = req.body;
    
    if (!nombre || !email || !mensaje) {
      return res.status(400).json({ error: 'Faltan campos requeridos' });
    }
    
    const nuevoMensaje = {
      nombre,
      email,
      telefono: telefono || '',
      mensaje,
      leido: false,
      fecha: new Date()
    };
    
    const resultado = await mensajesCollection.insertOne(nuevoMensaje);
    
    res.status(201).json({
      message: 'Mensaje enviado exitosamente',
      _id: resultado.insertedId.toString()
    });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al enviar mensaje' });
  }
});

// GET /api/mensajes - Obtener mensajes (SOLO ADMIN)
app.get('/api/mensajes', authenticateToken, isAdmin, async (req, res) => {
  try {
    const soloNoLeidos = req.query.no_leidos === 'true';
    
    const filtro = soloNoLeidos ? { leido: false } : {};
    
    const mensajes = await mensajesCollection
      .find(filtro)
      .sort({ fecha: -1 })
      .toArray();
    
    const mensajesFormateados = mensajes.map(m => ({
      ...m,
      _id: m._id.toString()
    }));
    
    res.json(mensajesFormateados);
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al obtener mensajes' });
  }
});

// PUT /api/mensajes/:id/leido - Marcar mensaje como leído (SOLO ADMIN)
app.put('/api/mensajes/:id/leido', authenticateToken, isAdmin, async (req, res) => {
  try {
    const { leido } = req.body;
    
    const resultado = await mensajesCollection.updateOne(
      { _id: new ObjectId(req.params.id) },
      { $set: { leido: leido !== undefined ? leido : true } }
    );
    
    if (resultado.matchedCount === 0) {
      return res.status(404).json({ error: 'Mensaje no encontrado' });
    }
    
    res.json({ message: 'Estado actualizado' });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al actualizar mensaje' });
  }
});

// DELETE /api/mensajes/:id - Eliminar mensaje (SOLO ADMIN)
app.delete('/api/mensajes/:id', authenticateToken, isAdmin, async (req, res) => {
  try {
    const resultado = await mensajesCollection.deleteOne({ 
      _id: new ObjectId(req.params.id) 
    });
    
    if (resultado.deletedCount === 0) {
      return res.status(404).json({ error: 'Mensaje no encontrado' });
    }
    
    res.json({ message: 'Mensaje eliminado' });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al eliminar mensaje' });
  }
});

// GET /api/mensajes/stats - Estadísticas de mensajes (SOLO ADMIN)
app.get('/api/mensajes/stats', authenticateToken, isAdmin, async (req, res) => {
  try {
    const total = await mensajesCollection.countDocuments();
    const noLeidos = await mensajesCollection.countDocuments({ leido: false });
    
    res.json({
      total,
      no_leidos: noLeidos,
      leidos: total - noLeidos
    });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al obtener estadísticas' });
  }
});

// ==================== RUTAS DE FAVORITOS ====================

// POST /api/favoritos - Agregar a favoritos (REQUIERE AUTH)
app.post('/api/favoritos', authenticateToken, async (req, res) => {
  try {
    const { vehiculoId } = req.body;
    
    if (!vehiculoId) {
      return res.status(400).json({ error: 'vehiculoId es requerido' });
    }
    
    // Verificar si ya existe
    const existe = await favoritosCollection.findOne({
      usuarioId: req.user.userId,
      vehiculoId
    });
    
    if (existe) {
      return res.status(400).json({ error: 'Ya está en favoritos' });
    }
    
    const nuevoFavorito = {
      usuarioId: req.user.userId,
      vehiculoId,
      fechaAgregado: new Date()
    };
    
    await favoritosCollection.insertOne(nuevoFavorito);
    
    res.status(201).json({ message: 'Agregado a favoritos' });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al agregar favorito' });
  }
});

// DELETE /api/favoritos/:vehiculoId - Eliminar de favoritos (REQUIERE AUTH)
app.delete('/api/favoritos/:vehiculoId', authenticateToken, async (req, res) => {
  try {
    const resultado = await favoritosCollection.deleteOne({
      usuarioId: req.user.userId,
      vehiculoId: req.params.vehiculoId
    });
    
    if (resultado.deletedCount === 0) {
      return res.status(404).json({ error: 'No está en favoritos' });
    }
    
    res.json({ message: 'Eliminado de favoritos' });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al eliminar favorito' });
  }
});

// GET /api/favoritos - Obtener mis favoritos (REQUIERE AUTH)
app.get('/api/favoritos', authenticateToken, async (req, res) => {
  try {
    const favoritos = await favoritosCollection
      .find({ usuarioId: req.user.userId })
      .toArray();
    
    // Obtener información de cada vehículo
    const vehiculosIds = favoritos.map(f => new ObjectId(f.vehiculoId));
    const vehiculos = await vehiculosCollection
      .find({ _id: { $in: vehiculosIds } })
      .toArray();
    
    const vehiculosFormateados = vehiculos.map(v => ({
      ...v,
      _id: v._id.toString()
    }));
    
    res.json(vehiculosFormateados);
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al obtener favoritos' });
  }
});

// ==================== RUTAS DE COTIZADOR ====================

// POST /api/cotizador - Cotizar vehículo usado (PÚBLICO)
app.post('/api/cotizador', async (req, res) => {
  try {
    const { marca, modelo, anio, kilometraje, estado } = req.body;
    
    // Validaciones
    if (!marca || !modelo || !anio || !kilometraje || !estado) {
      return res.status(400).json({ error: 'Faltan campos requeridos' });
    }
    
    const anioActual = new Date().getFullYear();
    if (anio < 1990 || anio > anioActual + 1) {
      return res.status(400).json({ 
        error: `El año debe estar entre 1990 y ${anioActual + 1}` 
      });
    }
    
    const estadosValidos = ['excelente', 'muy_bueno', 'bueno', 'regular'];
    if (!estadosValidos.includes(estado)) {
      return res.status(400).json({ 
        error: `Estado debe ser: ${estadosValidos.join(', ')}` 
      });
    }
    
    // Cálculo de cotización
    const valorBase = 8000000; // Base 8 millones
    const aniosUso = anioActual - anio;
    const depreciacionAnual = 400000;
    const depreciacionTotal = aniosUso * depreciacionAnual;
    const depreciacionKm = (kilometraje / 10000) * 80000;
    
    const multiplicadores = {
      'excelente': 1.15,
      'muy_bueno': 1.0,
      'bueno': 0.85,
      'regular': 0.65
    };
    
    const multiplicador = multiplicadores[estado];
    let valorEstimado = (valorBase - depreciacionTotal - depreciacionKm) * multiplicador;
    valorEstimado = Math.max(valorEstimado, 500000); // Mínimo 500k
    
    res.json({
      valorEstimado: Math.round(valorEstimado),
      detalles: {
        marca,
        modelo,
        anio,
        kilometraje,
        estado,
        valorBase,
        aniosUso,
        depreciacionAnual,
        depreciacionTotal,
        depreciacionKm,
        multiplicador
      }
    });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al calcular cotización' });
  }
});

// ==================== RUTAS DE PLANES ====================

// GET /api/planes - Obtener planes de financiación (PÚBLICO)
app.get('/api/planes', (req, res) => {
  try {
    const planes = [
      {
        id: 'plan-a',
        nombre: 'Plan 12 Cuotas Sin Interés',
        descripcion: 'Ideal para compras rápidas. Pagá tu auto en 12 cuotas fijas sin interés.',
        cuotas: 12,
        interes: 0,
        tasaMensual: 0,
        engancheMinimo: 20,
        montoMinimo: 5000000,
        montoMaximo: 15000000,
        vigencia: '2025-12-31',
        destacado: true
      },
      {
        id: 'plan-b',
        nombre: 'Plan 24 Cuotas Tasa Promocional',
        descripcion: 'Tasa promocional del 5% anual. Perfecto para financiar sin comprometer tu presupuesto.',
        cuotas: 24,
        interes: 5,
        tasaMensual: 0.42,
        engancheMinimo: 15,
        montoMinimo: 3000000,
        montoMaximo: 20000000,
        vigencia: '2025-12-31',
        destacado: true
      },
      {
        id: 'plan-c',
        nombre: 'Plan 36 Cuotas Extendido',
        descripcion: 'Financiación a largo plazo con cuotas más bajas. Tasa del 8% anual.',
        cuotas: 36,
        interes: 8,
        tasaMensual: 0.67,
        engancheMinimo: 10,
        montoMinimo: 2000000,
        montoMaximo: 25000000,
        vigencia: '2025-12-31',
        destacado: false
      },
      {
        id: 'plan-100',
        nombre: 'Plan 100% Financiado',
        descripcion: 'Sin enganche. Financiamos el 100% del valor del vehículo en hasta 48 cuotas.',
        cuotas: 48,
        interes: 12,
        tasaMensual: 1.0,
        engancheMinimo: 0,
        montoMinimo: 4000000,
        montoMaximo: 18000000,
        vigencia: '2025-12-31',
        destacado: true
      }
    ];
    
    // Filtros opcionales
    const destacados = req.query.destacados === 'true';
    const cuotasMax = parseInt(req.query.cuotas_max);
    const monto = parseFloat(req.query.monto);
    
    let planesFiltrados = planes;
    
    if (destacados) {
      planesFiltrados = planesFiltrados.filter(p => p.destacado);
    }
    
    if (cuotasMax) {
      planesFiltrados = planesFiltrados.filter(p => p.cuotas <= cuotasMax);
    }
    
    if (monto) {
      planesFiltrados = planesFiltrados.filter(
        p => p.montoMinimo <= monto && monto <= p.montoMaximo
      );
    }
    
    res.json(planesFiltrados);
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al obtener planes' });
  }
});

// POST /api/planes/:planId/calcular - Calcular cuota (PÚBLICO)
app.post('/api/planes/:planId/calcular', (req, res) => {
  try {
    const { monto, enganche } = req.body;
    
    if (!monto) {
      return res.status(400).json({ error: 'Monto es requerido' });
    }
    
    // Obtener plan
    const planes = {
      'plan-a': { cuotas: 12, tasaMensual: 0, engancheMinimo: 20, montoMinimo: 5000000, montoMaximo: 15000000, interes: 0 },
      'plan-b': { cuotas: 24, tasaMensual: 0.42, engancheMinimo: 15, montoMinimo: 3000000, montoMaximo: 20000000, interes: 5 },
      'plan-c': { cuotas: 36, tasaMensual: 0.67, engancheMinimo: 10, montoMinimo: 2000000, montoMaximo: 25000000, interes: 8 },
      'plan-100': { cuotas: 48, tasaMensual: 1.0, engancheMinimo: 0, montoMinimo: 4000000, montoMaximo: 18000000, interes: 12 }
    };
    
    const plan = planes[req.params.planId];
    
    if (!plan) {
      return res.status(404).json({ error: 'Plan no encontrado' });
    }
    
    const montoTotal = parseFloat(monto);
    const engancheMonto = parseFloat(enganche || 0);
    
    // Validar monto
    if (montoTotal < plan.montoMinimo || montoTotal > plan.montoMaximo) {
      return res.status(400).json({
        error: `El monto debe estar entre ${plan.montoMinimo.toLocaleString()} y ${plan.montoMaximo.toLocaleString()}`
      });
    }
    
    // Validar enganche mínimo
    const engancheMinimo = montoTotal * (plan.engancheMinimo / 100);
    if (engancheMonto < engancheMinimo) {
      return res.status(400).json({
        error: `El enganche mínimo es ${Math.round(engancheMinimo).toLocaleString()} (${plan.engancheMinimo}%)`
      });
    }
    
    const montoFinanciar = montoTotal - engancheMonto;
    const tasaMensual = plan.tasaMensual / 100;
    const cuotas = plan.cuotas;
    
    let cuotaMensual, totalAPagar, interesTotal;
    
    if (tasaMensual === 0) {
      cuotaMensual = montoFinanciar / cuotas;
      totalAPagar = montoFinanciar;
      interesTotal = 0;
    } else {
      // Fórmula de amortización francesa
      cuotaMensual = montoFinanciar * (tasaMensual * Math.pow(1 + tasaMensual, cuotas)) / (Math.pow(1 + tasaMensual, cuotas) - 1);
      totalAPagar = cuotaMensual * cuotas;
      interesTotal = totalAPagar - montoFinanciar;
    }
    
    res.json({
      planId: req.params.planId,
      montoVehiculo: Math.round(montoTotal),
      enganche: Math.round(engancheMonto),
      montoFinanciar: Math.round(montoFinanciar),
      cuotas,
      cuotaMensual: Math.round(cuotaMensual),
      totalAPagar: Math.round(totalAPagar),
      interesTotal: Math.round(interesTotal),
      tasaAnual: plan.interes,
      tasaMensual: plan.tasaMensual
    });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al calcular cuota' });
  }
});

// ==================== RUTAS DE TURNOS (TEST DRIVE) ====================

// POST /api/turnos - Agendar turno (REQUIERE AUTH)
app.post('/api/turnos', authenticateToken, async (req, res) => {
  try {
    const { vehiculoId, fecha, hora, comentarios } = req.body;
    
    if (!vehiculoId || !fecha || !hora) {
      return res.status(400).json({ error: 'Faltan campos requeridos' });
    }
    
    // Verificar que el vehículo existe
    const vehiculo = await vehiculosCollection.findOne({ 
      _id: new ObjectId(vehiculoId) 
    });
    
    if (!vehiculo) {
      return res.status(404).json({ error: 'Vehículo no encontrado' });
    }
    
    // Crear fecha y hora completa
    const fechaHora = new Date(`${fecha}T${hora}`);
    
    const nuevoTurno = {
      usuarioId: req.user.userId,
      vehiculoId,
      fechaHora,
      comentarios: comentarios || '',
      estado: 'pendiente',
      createdAt: new Date()
    };
    
    const resultado = await turnosCollection.insertOne(nuevoTurno);
    
    res.status(201).json({
      message: 'Turno agendado exitosamente',
      turnoId: resultado.insertedId.toString()
    });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al agendar turno' });
  }
});

// GET /api/turnos - Obtener mis turnos (REQUIERE AUTH)
app.get('/api/turnos', authenticateToken, async (req, res) => {
  try {
    const turnos = await turnosCollection
      .find({ usuarioId: req.user.userId })
      .sort({ fechaHora: -1 })
      .toArray();
    
    // Obtener información de cada vehículo
    const turnosConVehiculos = await Promise.all(
      turnos.map(async (turno) => {
        const vehiculo = await vehiculosCollection.findOne({ 
          _id: new ObjectId(turno.vehiculoId) 
        });
        
        return {
          ...turno,
          _id: turno._id.toString(),
          vehiculo: vehiculo ? {
            ...vehiculo,
            _id: vehiculo._id.toString()
          } : null
        };
      })
    );
    
    res.json(turnosConVehiculos);
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al obtener turnos' });
  }
});

// DELETE /api/turnos/:id - Cancelar turno (REQUIERE AUTH)
app.delete('/api/turnos/:id', authenticateToken, async (req, res) => {
  try {
    const resultado = await turnosCollection.updateOne(
      { 
        _id: new ObjectId(req.params.id),
        usuarioId: req.user.userId
      },
      { $set: { estado: 'cancelado' } }
    );
    
    if (resultado.matchedCount === 0) {
      return res.status(404).json({ error: 'Turno no encontrado' });
    }
    
    res.json({ message: 'Turno cancelado exitosamente' });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al cancelar turno' });
  }
});

// ==================== RUTA DE PRUEBA ====================
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    message: 'Backend funcionando correctamente',
    timestamp: new Date().toISOString()
  });
});

// ==================== MANEJO DE ERRORES ====================
app.use((req, res) => {
  res.status(404).json({ error: 'Ruta no encontrada' });
});

app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({ error: 'Error interno del servidor' });
});

// ==================== INICIAR SERVIDOR ====================
async function startServer() {
  await connectDB();
  
  app.listen(PORT, () => {
    console.log('='.repeat(60));
    console.log('🚗 GIMÉNEZ AUTOMOTORES - BACKEND API');
    console.log('='.repeat(60));
    console.log(`📍 Servidor corriendo en: http://localhost:${PORT}`);
    console.log(`🔗 MongoDB: Conectado`);
    console.log(`🔐 Endpoints disponibles:`);
    console.log(`   - GET  /api/health`);
    console.log(`   - POST /api/auth/register`);
    console.log(`   - POST /api/auth/login`);
    console.log(`   - GET  /api/vehiculos`);
    console.log(`   - GET  /api/vehiculos/destacados`);
    console.log(`   - POST /api/mensajes`);
    console.log('='.repeat(60));
  });
}

startServer();