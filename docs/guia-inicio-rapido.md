# 🚀 Guía de Inicio Rápido - Metadatos App con Podman

Esta guía te permitirá ejecutar la aplicación Metadatos App en un contenedor Podman en menos de 10 minutos desde cero.

---

## 📋 **Prerrequisitos**

- **Git** instalado
- **Podman** instalado ([Guía de instalación](docker_instructions.md#-paso-1-instalar-podman))
- **Terminal/Línea de comandos**
- **Conexión a internet** para descargar dependencias

---

## ⚡ **Inicio Rápido (5 minutos)**

### **Paso 1: Clonar el Repositorio**

```bash
# Clonar desde GitHub
git clone https://github.com/Gabo-araya/metadatos-app.git
cd metadatos-app

# Verificar que tienes todos los archivos
ls -la
```

**Archivos esperados:**
```
├── app.py                 # Aplicación Flask principal
├── database.py            # Modelos de base de datos
├── wsgi_simple.py         # WSGI para contenedores
├── requirements.txt       # Dependencias Python
├── Dockerfile.optimized   # Dockerfile para Podman
├── docker-compose.yml     # Configuración compose
├── templates/             # Plantillas HTML
├── static/               # Archivos CSS/JS
└── docs/                 # Documentación
```

### **Paso 2: Crear Variables de Entorno**

```bash
# Crear archivo de configuración para contenedor
cat > .env.docker << 'EOF'
# Configuración de seguridad (CAMBIAR EN PRODUCCIÓN)
SECRET_KEY=mi-clave-secreta-cambiar-en-produccion-2024
FLASK_ENV=production
FLASK_DEBUG=False

# Base de datos
DATABASE_URL=sqlite:///data/metadatos.db

# Credenciales de administrador (CAMBIAR ESTOS VALORES)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=MiPassword2024!

# Configuración de archivos
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# URL base
BASE_URL=http://localhost:5000

# Metadatos Dublin Core
DC_CREATOR=Mi Organización
DC_PUBLISHER=Metadatos App
DC_RIGHTS=© 2024 Mi Organización. Todos los derechos reservados.
DC_LANGUAGE=es
EOF

echo "✅ Archivo .env.docker creado"
```

### **Paso 3: Construir la Imagen**

```bash
# Construir imagen con Podman
podman build -f Dockerfile.optimized -t metadatos-app:latest .

# Verificar que se creó correctamente
podman images | grep metadatos-app
```

**Salida esperada:**
```
localhost/metadatos-app  latest  abc123def456  2 minutes ago  xyz MB
```

### **Paso 4: Ejecutar el Contenedor**

```bash
# Ejecutar contenedor con volúmenes persistentes
podman run -d \
  --name metadatos-app \
  -p 5000:5000 \
  --env-file .env.docker \
  -v metadatos_data:/app/data \
  -v metadatos_uploads:/app/uploads \
  -v metadatos_logs:/app/logs \
  metadatos-app:latest

echo "✅ Contenedor iniciado"
```

### **Paso 5: Verificar Funcionamiento**

```bash
# Verificar que el contenedor está corriendo
podman ps

# Probar health check (esperar 10-15 segundos)
sleep 15
curl -f http://localhost:5000/health

# Ver logs de inicio
podman logs metadatos-app --tail 10
```

**Salida esperada del health check:**
```json
{"status":"healthy","timestamp":"2024-08-11T10:30:15.123456"}
```

### **Paso 6: Acceder a la Aplicación**

```bash
echo "🎉 ¡Aplicación lista!"
echo "📱 Accede en tu navegador:"
echo "   http://localhost:5000"
echo ""
echo "🔐 Login de administrador:"
echo "   URL: http://localhost:5000/login"
echo "   Usuario: admin"
echo "   Contraseña: MiPassword2024!"
```

---

## 🔧 **Comandos de Gestión**

### **Ver Estado del Contenedor**

```bash
# Ver contenedores corriendo
podman ps

# Ver logs en tiempo real
podman logs -f metadatos-app

# Ver estadísticas de uso
podman stats metadatos-app

# Inspeccionar configuración
podman inspect metadatos-app
```

### **Gestión del Contenedor**

```bash
# Parar contenedor
podman stop metadatos-app

# Iniciar contenedor parado
podman start metadatos-app

# Reiniciar contenedor
podman restart metadatos-app

# Entrar al contenedor para debugging
podman exec -it metadatos-app /bin/bash
```

### **Gestión de Datos**

```bash
# Ver volúmenes creados
podman volume ls

# Backup de datos
podman run --rm \
  -v metadatos_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup-$(date +%Y%m%d_%H%M%S).tar.gz -C /data .

# Restaurar backup (ejemplo)
# podman run --rm \
#   -v metadatos_data:/data \
#   -v $(pwd):/backup \
#   alpine tar xzf /backup/backup-20240811_103000.tar.gz -C /data
```

---

## 🚨 **Solución de Problemas Rápida**

### **❌ Problema: "Port already in use"**

```bash
# Ver qué está usando el puerto 5000
lsof -i :5000
# O en algunos sistemas:
ss -tulpn | grep :5000

# Cambiar puerto si es necesario
podman stop metadatos-app && podman rm metadatos-app
podman run -d \
  --name metadatos-app \
  -p 8000:5000 \  # <-- Cambiar puerto aquí
  --env-file .env.docker \
  -v metadatos_data:/app/data \
  -v metadatos_uploads:/app/uploads \
  -v metadatos_logs:/app/logs \
  metadatos-app:latest

echo "Aplicación disponible en: http://localhost:8000"
```

### **❌ Problema: "Container won't start"**

```bash
# Ver logs detallados del error
podman logs metadatos-app

# Verificar configuración de variables
cat .env.docker

# Reconstruir imagen si es necesario
podman stop metadatos-app && podman rm metadatos-app
podman rmi metadatos-app:latest
podman build -f Dockerfile.optimized -t metadatos-app:latest .
```

### **❌ Problema: "Cannot connect to application"**

```bash
# Verificar que el contenedor está corriendo
podman ps

# Verificar puertos
podman port metadatos-app

# Probar health check interno
podman exec -it metadatos-app curl -f http://localhost:5000/health

# Verificar firewall (Ubuntu/Debian)
sudo ufw status
```

### **❌ Problema: "Permission denied" en uploads**

```bash
# Entrar al contenedor y verificar permisos
podman exec -it metadatos-app ls -la /app/

# Corregir permisos si es necesario
podman exec -it metadatos-app chmod -R 777 /app/uploads /app/logs /app/data
```

---

## 🔄 **Actualizar la Aplicación**

```bash
# 1. Obtener últimos cambios
git pull origin main

# 2. Parar y eliminar contenedor actual
podman stop metadatos-app && podman rm metadatos-app

# 3. Reconstruir imagen
podman build -f Dockerfile.optimized -t metadatos-app:$(date +%Y%m%d) .

# 4. Ejecutar nueva versión (conserva datos en volúmenes)
podman run -d \
  --name metadatos-app \
  -p 5000:5000 \
  --env-file .env.docker \
  -v metadatos_data:/app/data \
  -v metadatos_uploads:/app/uploads \
  -v metadatos_logs:/app/logs \
  metadatos-app:$(date +%Y%m%d)

# 5. Verificar
curl -f http://localhost:5000/health
podman logs metadatos-app --tail 5
```

---

## 📊 **Modo Desarrollo (Opcional)**

Si quieres desarrollar y hacer cambios en el código:

```bash
# Clonar en modo desarrollo
git clone https://github.com/Gabo-araya/metadatos-app.git
cd metadatos-app

# Crear entorno virtual Python
python3 -m venv env
source env/bin/activate  # Linux/macOS
# env\Scripts\activate    # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno para desarrollo
cp .env.example .env  # Si existe
# O crear manualmente:
cat > .env << 'EOF'
SECRET_KEY=clave-desarrollo-no-usar-en-produccion
FLASK_ENV=development
FLASK_DEBUG=True
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
DATABASE_URL=sqlite:///metadatos.db
UPLOAD_FOLDER=uploads
EOF

# Inicializar base de datos
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Ejecutar en modo desarrollo
flask run
# O: python app.py

# Aplicación disponible en: http://127.0.0.1:5000
```

---

## 🔒 **Configuración de Producción**

Para usar en producción, actualiza `.env.docker`:

```bash
cat > .env.docker << 'EOF'
# CONFIGURACIÓN DE PRODUCCIÓN - CAMBIAR TODOS ESTOS VALORES
SECRET_KEY=clave-super-secreta-produccion-256-bits-cambiar-obligatorio
FLASK_ENV=production
FLASK_DEBUG=False

# Base de datos (considerar PostgreSQL para producción)
DATABASE_URL=sqlite:///data/metadatos.db

# Credenciales admin FUERTES
ADMIN_USERNAME=admin_prod_$(date +%s)
ADMIN_PASSWORD=ClaveProduccion2024!MuySegura#

# Configuración restrictiva
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
LOG_LEVEL=WARNING

# URL real de tu dominio
BASE_URL=https://tu-dominio.com

# Información de tu organización
DC_CREATOR=Tu Organización
DC_PUBLISHER=Tu Organización
DC_RIGHTS=© 2024 Tu Organización. Todos los derechos reservados.
DC_LANGUAGE=es
EOF

# Ejecutar con configuración de producción
podman run -d \
  --name metadatos-app-prod \
  -p 80:5000 \
  --env-file .env.docker \
  --restart unless-stopped \
  -v metadatos_data_prod:/app/data \
  -v metadatos_uploads_prod:/app/uploads \
  -v metadatos_logs_prod:/app/logs \
  metadatos-app:latest
```

---

## 📱 **Usar con Docker Compose**

Si prefieres usar docker-compose:

```bash
# Usar Podman Compose (recomendado)
podman compose up -d

# Ver estado
podman compose ps

# Ver logs
podman compose logs -f

# Parar servicios
podman compose down

# Actualizar servicios
podman compose pull
podman compose up -d
```

---

## 🎯 **Script de Instalación Automatizada**

Crea un script para automatizar todo el proceso:

```bash
cat > setup.sh << 'EOF'
#!/bin/bash
set -e

echo "🚀 Iniciando instalación de Metadatos App..."

# Verificar prerrequisitos
command -v podman >/dev/null 2>&1 || { echo "❌ Podman no está instalado. Instálalo primero."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ Git no está instalado. Instálalo primero."; exit 1; }

# Variables
REPO_URL="https://github.com/Gabo-araya/metadatos-app.git"
APP_NAME="metadatos-app"
PORT="5000"

# Pedir credenciales
read -p "👤 Usuario administrador [admin]: " ADMIN_USER
ADMIN_USER=${ADMIN_USER:-admin}
read -s -p "🔐 Contraseña administrador: " ADMIN_PASS
echo
read -p "🌐 Puerto de la aplicación [$PORT]: " USER_PORT
USER_PORT=${USER_PORT:-$PORT}

echo "📁 Clonando repositorio..."
git clone $REPO_URL
cd $APP_NAME

echo "⚙️ Creando configuración..."
cat > .env.docker << EOL
SECRET_KEY=clave-generada-$(date +%s)-$(openssl rand -hex 16)
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=sqlite:///data/metadatos.db
ADMIN_USERNAME=$ADMIN_USER
ADMIN_PASSWORD=$ADMIN_PASS
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
BASE_URL=http://localhost:$USER_PORT
DC_CREATOR=Mi Organización
DC_PUBLISHER=Metadatos App
DC_RIGHTS=© 2024 Mi Organización. Todos los derechos reservados.
DC_LANGUAGE=es
EOL

echo "🔨 Construyendo imagen..."
podman build -f Dockerfile.optimized -t metadatos-app:latest .

echo "🚀 Iniciando contenedor..."
podman run -d \
  --name metadatos-app \
  -p $USER_PORT:5000 \
  --env-file .env.docker \
  -v metadatos_data:/app/data \
  -v metadatos_uploads:/app/uploads \
  -v metadatos_logs:/app/logs \
  metadatos-app:latest

echo "⏳ Esperando que la aplicación inicie..."
sleep 15

if curl -f http://localhost:$USER_PORT/health > /dev/null 2>&1; then
    echo "✅ ¡Instalación completada exitosamente!"
    echo "🌐 Aplicación disponible en: http://localhost:$USER_PORT"
    echo "🔐 Login: http://localhost:$USER_PORT/login"
    echo "👤 Usuario: $ADMIN_USER"
    echo "🔑 Contraseña: [la que ingresaste]"
    echo ""
    echo "📋 Comandos útiles:"
    echo "   podman logs metadatos-app     # Ver logs"
    echo "   podman stop metadatos-app     # Parar aplicación"
    echo "   podman start metadatos-app    # Iniciar aplicación"
else
    echo "❌ Error: La aplicación no respondió correctamente"
    echo "Ver logs con: podman logs metadatos-app"
fi
EOF

chmod +x setup.sh
echo "✅ Script de instalación creado: ./setup.sh"
```

**Para usar el script:**

```bash
# Hacer ejecutable y correr
chmod +x setup.sh
./setup.sh
```

---

## 🆘 **Soporte y Ayuda**

- **📖 Documentación completa**: [docs/docker_instructions.md](docker_instructions.md)
- **🐛 Reportar problemas**: [GitHub Issues](https://github.com/Gabo-araya/metadatos-app/issues)
- **💬 Preguntas**: Crear un issue con la etiqueta "question"

---

**🎉 ¡Listo! Tu aplicación Metadatos App está funcionando en Podman.**