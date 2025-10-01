const express = require('express');
const dotenv = require('dotenv');

// Cargar variables de entorno
dotenv.config();

const app = express();

// Middleware básico para parsear JSON (útil para futuras rutas)
app.use(express.json());

// Ruta de prueba
app.get('/', (req, res) => {
  res.json({ message: '¡Servidor Express de Gimenez-Mateyi funcionando!' });
});

// Puerto desde .env o 3000 por defecto
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});