// verificar_admin.js
// Script para verificar y crear el usuario admin si no existe

const bcrypt = require('bcryptjs');
const { MongoClient } = require('mongodb');

const MONGO_URL = 'mongodb://admin:admin123@localhost:27017/concesionaria?authSource=admin';

async function verificarAdmin() {
  let client;
  
  try {
    console.log('🔍 Conectando a MongoDB...');
    client = await MongoClient.connect(MONGO_URL);
    const db = client.db('concesionaria');
    const usuariosCollection = db.collection('usuarios');
    
    // Buscar usuario admin
    const adminExiste = await usuariosCollection.findOne({ username: 'admin' });
    
    if (adminExiste) {
      console.log('✅ Usuario admin encontrado:');
      console.log('   Username:', adminExiste.username);
      console.log('   Email:', adminExiste.email);
      console.log('   Role:', adminExiste.role);
      
      // Verificar contraseña
      const passwordCorrecta = await bcrypt.compare('admin123', adminExiste.password);
      
      if (passwordCorrecta) {
        console.log('✅ La contraseña "admin123" es CORRECTA');
      } else {
        console.log('❌ La contraseña NO coincide. Actualizando...');
        
        const nuevoHash = await bcrypt.hash('admin123', 10);
        await usuariosCollection.updateOne(
          { username: 'admin' },
          { $set: { password: nuevoHash } }
        );
        
        console.log('✅ Contraseña actualizada correctamente');
      }
    } else {
      console.log('❌ Usuario admin NO encontrado. Creando...');
      
      const hashedPassword = await bcrypt.hash('admin123', 10);
      
      await usuariosCollection.insertOne({
        username: 'admin',
        password: hashedPassword,
        email: 'admin@gimenez.com',
        role: 'admin',
        createdAt: new Date()
      });
      
      console.log('✅ Usuario admin creado exitosamente');
      console.log('   Username: admin');
      console.log('   Password: admin123');
      console.log('   Email: admin@gimenez.com');
      console.log('   Role: admin');
    }
    
    console.log('\n📝 CREDENCIALES DE ACCESO:');
    console.log('   Usuario: admin');
    console.log('   Contraseña: admin123');
    console.log('\n🌐 Ahora puedes iniciar sesión en: http://localhost:8080/login.html');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    
    if (error.message.includes('ECONNREFUSED')) {
      console.log('\n💡 Solución: Asegúrate de que MongoDB esté corriendo:');
      console.log('   docker-compose up -d');
    }
  } finally {
    if (client) {
      await client.close();
      console.log('\n✅ Conexión cerrada');
    }
  }
}

// Ejecutar
verificarAdmin();