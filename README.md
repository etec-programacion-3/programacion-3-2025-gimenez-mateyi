# programacion-3-2025-gimenez-mateyi
programacion-3-2025-gimenez-mateyi created by GitHub Classroom

Giménez Automotores — Pagina web (Flask + MongoDB)

Proyecto de concesionaria para listar, destacar y gestionar vehículos Fiat. Backend en Flask, plantillas con Jinja2, assets estáticos en static/, datos en MongoDB (Atlas o local).

Estructura del proyecto (resumen)

app.py  punto de entrada de la aplicación Flask

templates/ — plantillas Jinja2 (base.html, index.html, etc.)

static/ — CSS, JS, img (imagenes de vehículos, placeholder.png)

requirements.txt — dependencias Python

scripts/ (opcional) — utilidades de soporte (migraciones, sync imagenes)

### Backend
- Python 3.11+
- Flask 3.0.0
- Flask-Login 0.6.3
- PyMongo 4.6.1
- bcrypt 4.1.2
- python-dotenv 1.0.0

### Frontend
- HTML5, CSS3, JavaScript
- Bootstrap 5.3.0
- Bootstrap Icons 1.11.1

### Base de Datos
- MongoDB Atlas (NoSQL en la nube)

### 1. Clonar el repositorio
git clone /home/mateog/programacion-3-2025-gimenez-mateyi/programacion-3-2025-gimenez-mateyi-2/
cd /home/mateog/programacion-3-2025-gimenez-mateyi/programacion-3-2025-gimenez-mateyi-2/

### 2. Crear entorno virtual

**En Linux/macOS:**
python3 -m venv venv
source venv/bin/activate

### 3. Instalar dependencias
```bash
pip install -r requirements.txt

**Contenido de `requirements.txt`:**
```txt
pymongo==4.6.1
python-dotenv==1.0.0
Flask-Login==0.6.3
bcrypt==4.1.2
astroid==3.3.11
blinker==1.9.0
click==8.2.1
dill==0.4.0
Flask==3.1.2
isort==6.0.1
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
mccabe==0.7.0
platformdirs==4.4.0
pylint==3.3.8
tomlkit==0.13.3
Werkzeug==3.1.3

### 6. Iniciar el servidor
```bash
python app.py
```
