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
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

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
let alertasCollection;
let cotizacionesCollection;

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
    alertasCollection = db.collection('alertas');
    cotizacionesCollection = db.collection('cotizaciones');
    
    console.log('✅ Conectado a MongoDB');
    
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
  const token = authHeader && authHeader.split(' ')[1];
  
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
app.post('/api/auth/register', async (req, res) => {
  try {
    const { username, email, password } = req.body;
    
    if (!username || !email || !password) {
      return res.status(400).json({ error: 'Faltan campos requeridos' });
    }
    
    if (username.length < 3) {
      return res.status(400).json({ error: 'El username debe tener al menos 3 caracteres' });
    }
    
    if (password.length < 6) {
      return res.status(400).json({ error: 'La contraseña debe tener al menos 6 caracteres' });
    }
    
    const existeUsername = await usuariosCollection.findOne({ username: username.toLowerCase() });
    if (existeUsername) {
      return res.status(400).json({ error: 'El username ya está en uso' });
    }
    
    const existeEmail = await usuariosCollection.findOne({ email: email.toLowerCase() });
    if (existeEmail) {
      return res.status(400).json({ error: 'El email ya está registrado' });
    }
    
    const hashedPassword = await bcrypt.hash(password, 10);
    
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

app.post('/api/auth/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    
    if (!username || !password) {
      return res.status(400).json({ error: 'Username y password son requeridos' });
    }
    
    const usuario = await usuariosCollection.findOne({ 
      username: username.toLowerCase() 
    });
    
    if (!usuario) {
      return res.status(401).json({ error: 'Credenciales inválidas' });
    }
    
    const passwordValida = await bcrypt.compare(password, usuario.password);
    
    if (!passwordValida) {
      return res.status(401).json({ error: 'Credenciales inválidas' });
    }
    
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
app.get('/api/vehiculos', async (req, res) => {
  try {
    const vehiculos = await vehiculosCollection.find({}).toArray();
    
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
app.post('/api/favoritos', authenticateToken, async (req, res) => {
  try {
    const { vehiculoId } = req.body;
    
    if (!vehiculoId) {
      return res.status(400).json({ error: 'vehiculoId es requerido' });
    }
    
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
    
    res.status(201).json({ message: 'Agregado a favoritos', success: true });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al agregar favorito' });
  }
});

app.delete('/api/favoritos/:vehiculoId', authenticateToken, async (req, res) => {
  try {
    const resultado = await favoritosCollection.deleteOne({
      usuarioId: req.user.userId,
      vehiculoId: req.params.vehiculoId
    });
    
    if (resultado.deletedCount === 0) {
      return res.status(404).json({ error: 'No está en favoritos' });
    }
    
    res.json({ message: 'Eliminado de favoritos', success: true });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al eliminar favorito' });
  }
});

app.get('/api/favoritos', authenticateToken, async (req, res) => {
  try {
    const favoritos = await favoritosCollection
      .find({ usuarioId: req.user.userId })
      .toArray();
    
    const vehiculosIds = favoritos.map(f => new ObjectId(f.vehiculoId));
    
    if (vehiculosIds.length === 0) {
      return res.json([]);
    }
    
    const vehiculos = await vehiculosCollection
      .find({ _id: { $in: vehiculosIds } })
      .toArray();
    
    const vehiculosConFecha = vehiculos.map(v => {
      const favorito = favoritos.find(f => f.vehiculoId === v._id.toString());
      return {
        ...v,
        _id: v._id.toString(),
        fechaAgregado: favorito ? favorito.fechaAgregado : new Date()
      };
    });
    
    res.json(vehiculosConFecha);
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al obtener favoritos' });
  }
});

// ==================== RUTAS DE COTIZADOR ====================
app.post('/api/cotizador', async (req, res) => {
  try {
    const { marca, modelo, anio, kilometraje, estado } = req.body;
    
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
    
    const valorBase = 8000000;
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
    valorEstimado = Math.max(valorEstimado, 500000);
    
    // Guardar en historial si está autenticado
    const token = req.headers['authorization']?.split(' ')[1];
    if (token) {
      try {
        const decoded = jwt.verify(token, JWT_SECRET);
        const cotizacion = {
          usuarioId: decoded.userId,
          marca,
          modelo,
          anio,
          kilometraje,
          estado,
          valorEstimado: Math.round(valorEstimado),
          fecha: new Date()
        };
        await cotizacionesCollection.insertOne(cotizacion);
      } catch (err) {
        // Si el token no es válido, continuar sin guardar
      }
    }
    
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

app.get('/api/cotizaciones', authenticateToken, async (req, res) => {
  try {
    const cotizaciones = await cotizacionesCollection
      .find({ usuarioId: req.user.userId })
      .sort({ fecha: -1 })
      .toArray();
    
    const cotizacionesFormateadas = cotizaciones.map(c => ({
      ...c,
      _id: c._id.toString()
    }));
    
    res.json(cotizacionesFormateadas);
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al obtener cotizaciones' });
  }
});

// ==================== RUTAS DE TURNOS ====================
app.post('/api/turnos', authenticateToken, async (req, res) => {
  try {
    const { vehiculoId, fecha, hora, comentarios } = req.body;
    
    if (!vehiculoId || !fecha || !hora) {
      return res.status(400).json({ error: 'Faltan campos requeridos' });
    }
    
    const vehiculo = await vehiculosCollection.findOne({ 
      _id: new ObjectId(vehiculoId) 
    });
    
    if (!vehiculo) {
      return res.status(404).json({ error: 'Vehículo no encontrado' });
    }
    
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
      turnoId: resultado.insertedId.toString(),
      success: true
    });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al agendar turno' });
  }
});

app.get('/api/turnos', authenticateToken, async (req, res) => {
  try {
    const turnos = await turnosCollection
      .find({ usuarioId: req.user.userId })
      .sort({ fechaHora: -1 })
      .toArray();
    
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
    
    res.json({ message: 'Turno cancelado exitosamente', success: true });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al cancelar turno' });
  }
});

// ==================== RUTAS DE ALERTAS ====================
app.post('/api/alertas', authenticateToken, async (req, res) => {
  try {
    const { marca, modelo, precioMax, anioMin } = req.body;
    
    const nuevaAlerta = {
      usuarioId: req.user.userId,
      marca: marca || null,
      modelo: modelo || null,
      precioMax: precioMax ? parseFloat(precioMax) : null,
      anioMin: anioMin ? parseInt(anioMin) : null,
      activa: true,
      createdAt: new Date()
    };
    
    const resultado = await alertasCollection.insertOne(nuevaAlerta);
    
    res.status(201).json({
      message: 'Alerta creada exitosamente',
      alertaId: resultado.insertedId.toString(),
      success: true
    });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al crear alerta' });
  }
});

app.get('/api/alertas', authenticateToken, async (req, res) => {
  try {
    const alertas = await alertasCollection
      .find({ usuarioId: req.user.userId })
      .sort({ createdAt: -1 })
      .toArray();
    
    const alertasFormateadas = alertas.map(a => ({
      ...a,
      _id: a._id.toString()
    }));
    
    res.json(alertasFormateadas);
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al obtener alertas' });
  }
});

app.put('/api/alertas/:id/toggle', authenticateToken, async (req, res) => {
  try {
    const alerta = await alertasCollection.findOne({
      _id: new ObjectId(req.params.id),
      usuarioId: req.user.userId
    });
    
    if (!alerta) {
      return res.status(404).json({ error: 'Alerta no encontrada' });
    }
    
    const resultado = await alertasCollection.updateOne(
      { _id: new ObjectId(req.params.id) },
      { $set: { activa: !alerta.activa } }
    );
    
    res.json({ 
      message: 'Alerta actualizada', 
      success: true,
      activa: !alerta.activa
    });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al actualizar alerta' });
  }
});

app.delete('/api/alertas/:id', authenticateToken, async (req, res) => {
  try {
    const resultado = await alertasCollection.deleteOne({
      _id: new ObjectId(req.params.id),
      usuarioId: req.user.userId
    });
    
    if (resultado.deletedCount === 0) {
      return res.status(404).json({ error: 'Alerta no encontrada' });
    }
    
    res.json({ message: 'Alerta eliminada', success: true });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al eliminar alerta' });
  }
});

// ==================== RUTAS DE PLANES ====================
app.get('/api/planes', (req, res) => {
  try {
    const planes = [
      {
        id: 'plan-a',
        nombre: 'Plan 12 Cuotas Sin Interés',
        descripcion: 'Ideal para compras rápidas.',
        cuotas: 12,
        interes: 0,
        tasaMensual: 0,
        destacado: true
      },
      {
        id: 'plan-b',
        nombre: 'Plan 24 Cuotas',
        descripcion: 'Tasa promocional del 5% anual.',
        cuotas: 24,
        interes: 5,
        tasaMensual: 0.42,
        destacado: true
      }
    ];
    
    const destacados = req.query.destacados === 'true';
    let planesFiltrados = destacados ? planes.filter(p => p.destacado) : planes;
    
    res.json(planesFiltrados);
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al obtener planes' });
  }
});

// ==================== DASHBOARD USUARIO ====================
app.get('/api/usuario/stats', authenticateToken, async (req, res) => {
  try {
    const favoritos = await favoritosCollection.countDocuments({ 
      usuarioId: req.user.userId 
    });
    
    const cotizaciones = await cotizacionesCollection.countDocuments({ 
      usuarioId: req.user.userId 
    });
    
    const turnos = await turnosCollection.countDocuments({ 
      usuarioId: req.user.userId,
      estado: 'pendiente'
    });
    
    const alertas = await alertasCollection.countDocuments({ 
      usuarioId: req.user.userId,
      activa: true
    });
    
    res.json({
      favoritos,
      cotizaciones,
      turnos,
      alertas
    });
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error al obtener estadísticas' });
  }
});

// ==================== HEALTHh CHECK ====================
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
    console.log(`   - GET  /api/favoritos (AUTH)`);
    console.log(`   - GET  /api/turnos (AUTH)`);
    console.log(`   - GET  /api/alertas (AUTH)`);
    console.log(`   - GET  /api/cotizaciones (AUTH)`);
    console.log('='.repeat(60));
  });
}

startServer();
