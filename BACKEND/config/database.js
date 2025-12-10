const mongoose = require('mongoose');

/**
 * Conectar a MongoDB
 */
const connectDB = async () => {
  try {
    const conn = await mongoose.connect(process.env.MONGO_URI, {
      // Opciones recomendadas (algunas ya son default en Mongoose 6+)
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });

    console.log(`✅ MongoDB conectado: ${conn.connection.host}`);
    console.log(`📊 Base de datos: ${conn.connection.name}`);
  } catch (error) {
    console.error(`❌ Error de conexión MongoDB: ${error.message}`);
    process.exit(1); // Salir con error
  }
};

/**
 * Evento: Desconexión de MongoDB
 */
mongoose.connection.on('disconnected', () => {
  console.log('⚠️  MongoDB desconectado');
});

/**
 * Evento: Error en MongoDB
 */
mongoose.connection.on('error', (err) => {
  console.error(`❌ Error en MongoDB: ${err.message}`);
});

/**
 * Cerrar conexión gracefully
 */
const closeDB = async () => {
  try {
    await mongoose.connection.close();
    console.log('🔒 Conexión MongoDB cerrada');
  } catch (error) {
    console.error(`❌ Error al cerrar MongoDB: ${error.message}`);
  }
};

// Cerrar conexión cuando se termina el proceso
process.on('SIGINT', async () => {
  await closeDB();
  process.exit(0);
});

module.exports = connectDB;