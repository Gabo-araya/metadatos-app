# 🐳 Containerización con Podman

Esta guía completa te ayudará a containerizar la aplicación Metadatos App usando Podman, una alternativa rootless y más segura a Docker.

---

## 📋 **Prerrequisitos**

- Sistema operativo Linux, macOS o Windows
- Acceso a terminal/línea de comandos
- Proyecto Metadatos App funcionando localmente

---

## 📦 **Paso 1: Instalar Podman**

### **Ubuntu/Debian**
```bash
sudo apt update
sudo apt install podman
```

### **CentOS/RHEL/Fedora**
```bash
sudo dnf install podman
```

### **macOS**
```bash
# Instalar usando Homebrew
brew install podman

# Inicializar la máquina virtual (solo en macOS)
podman machine init
podman machine start
```

### **Verificar instalación**
```bash
podman --version
podman info
```

---

## 🔧 **Paso 2: Preparar Archivos de Configuración**

### **Crear Dockerfile**

Crea `Dockerfile.optimized` en el directorio raíz (ya existe en el proyecto):

```dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copiar código de la aplicación
COPY . .

# Crear directorios con permisos completos
RUN mkdir -p uploads logs data static/uploads && \
    chmod -R 777 uploads logs data static && \
    touch logs/app.log && \
    chmod 666 logs/app.log

# Exponer puerto
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Usar wsgi_simple para evitar problemas de logging
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "wsgi_simple:application"]
```

### **Crear .containerignore**

```bash
cat > .containerignore << 'EOF'
# Git
.git
.gitignore

# Python
__pycache__/
*.pyc
venv/
env/
*.egg-info/

# Local development
.env
.env.local
uploads/
logs/
*.log
*.db
*.sqlite*
instance/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Documentation
docs/
README.md
*.md

# Backup files
bkup/
EOF
```

### **Crear docker-compose.yml para Podman**

```yaml
# docker-compose.yml
version: '3.8'

services:
  metadatos-app:
    build:
      context: .
      dockerfile: Dockerfile.optimized
    container_name: metadatos-app
    restart: unless-stopped

    environment:
      - SECRET_KEY=${SECRET_KEY:-change-this-secret-key-in-production}
      - FLASK_ENV=production
      - FLASK_DEBUG=False
      - DATABASE_URL=sqlite:///data/metadatos.db
      - ADMIN_USERNAME=${ADMIN_USERNAME:-admin}
      - ADMIN_PASSWORD=${ADMIN_PASSWORD:-change-this-password}
      - UPLOAD_FOLDER=uploads
      - MAX_CONTENT_LENGTH=16777216
      - LOG_LEVEL=INFO
      - LOG_FILE=logs/app.log
      - BASE_URL=http://localhost:5000

    ports:
      - "5000:5000"

    volumes:
      - metadatos_data:/app/data
      - metadatos_uploads:/app/uploads
      - metadatos_logs:/app/logs

    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

    # Recursos
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
        reservations:
          cpus: "0.5"
          memory: 256M

volumes:
  metadatos_data:
    driver: local
  metadatos_uploads:
    driver: local
  metadatos_logs:
    driver: local

networks:
  default:
    name: metadatos-network
```

---

## 🚀 **Paso 3: Configurar Variables de Entorno**

### **Crear archivo .env.docker**

```bash
cat > .env.docker << 'EOF'
# Configuración básica de seguridad
SECRET_KEY=podman-secret-key-change-in-production-2024
FLASK_ENV=production
FLASK_DEBUG=False

# Base de datos
DATABASE_URL=sqlite:///data/metadatos.db

# Credenciales admin
ADMIN_USERNAME=admin_podman
ADMIN_PASSWORD=PodmanPassword2024!

# Configuración de archivos
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# URL base
BASE_URL=http://localhost:5000

# Metadatos Dublin Core
DC_CREATOR=Metadatos App Podman
DC_PUBLISHER=Metadatos App
DC_RIGHTS=© 2024 Metadatos App. Todos los derechos reservados.
DC_LANGUAGE=es
EOF
```

---

## 🏗️ **Paso 4: Construir y Ejecutar con Podman**

### **Opción A: Contenedor Simple**

```bash
# Construir la imagen
podman build -f Dockerfile.optimized -t metadatos-app:latest .

# Verificar que se creó
podman images

# Ejecutar el contenedor
podman run -d \
  --name metadatos-app \
  -p 5000:5000 \
  --env-file .env.docker \
  -v metadatos_data:/app/data \
  -v metadatos_uploads:/app/uploads \
  -v metadatos_logs:/app/logs \
  metadatos-app:latest

# Verificar que está corriendo
podman ps

# Ver logs
podman logs metadatos-app

# Probar la aplicación
curl http://localhost:5000/health
```

### **Opción B: Usando Podman Compose**

```bash
# Método 1: Podman Compose nativo (Podman 4.0+)
podman compose up -d

# Método 2: Usar docker-compose con Podman
# Configurar socket (solo si usas docker-compose)
export DOCKER_HOST=unix:///run/user/$UID/podman/podman.sock

# Iniciar servicios en segundo plano
podman compose up -d

# Ver estado
podman compose ps

# Ver logs en tiempo real
podman compose logs -f metadatos-app

# Parar servicios
podman compose down
```

---

## 🔍 **Paso 5: Verificar la Aplicación**

### **Tests básicos**

```bash
# 1. Verificar que el contenedor está corriendo
podman ps

# 2. Verificar salud de la aplicación
curl -f http://localhost:5000/health

# 3. Probar página principal
curl -I http://localhost:5000/

# 4. Verificar logs
podman logs --tail 20 metadatos-app

# 5. Verificar volúmenes
podman volume ls
```

### **Acceder a la aplicación**

1. **Abrir navegador** en: `http://localhost:5000`
2. **Probar login** en: `http://localhost:5000/login`
   - Usuario: `admin_podman`
   - Contraseña: `PodmanPassword2024!`
3. **Subir archivo de prueba** para verificar funcionalidad

---

## 🛠️ **Comandos Útiles de Podman**

### **Gestión de Contenedores**

```bash
# Ver contenedores corriendo
podman ps

# Ver todos los contenedores (incluso parados)
podman ps -a

# Entrar al contenedor para debugging
podman exec -it metadatos-app /bin/bash

# Ver logs en tiempo real
podman logs -f metadatos-app

# Ver estadísticas de recursos
podman stats metadatos-app

# Inspeccionar contenedor
podman inspect metadatos-app

# Parar contenedor
podman stop metadatos-app

# Reiniciar contenedor
podman restart metadatos-app

# Eliminar contenedor
podman rm metadatos-app
```

### **Gestión de Imágenes**

```bash
# Ver todas las imágenes
podman images

# Eliminar imagen
podman rmi metadatos-app:latest

# Limpiar imágenes no utilizadas
podman image prune

# Ver información detallada de la imagen
podman inspect metadatos-app:latest
```

### **Gestión de Volúmenes**

```bash
# Ver volúmenes
podman volume ls

# Inspeccionar volumen
podman volume inspect metadatos_data

# Backup de volumen
podman run --rm -v metadatos_data:/data -v $(pwd):/backup alpine tar czf /backup/data_backup.tar.gz -C /data .

# Eliminar volúmenes no utilizados
podman volume prune
```

---

## 🔧 **Actualizar la Aplicación**

```bash
# Para actualizar después de cambios en el código:

# 1. Parar y eliminar contenedor actual
podman stop metadatos-app && podman rm metadatos-app

# 2. Reconstruir imagen con tag actualizado
podman build -f Dockerfile.optimized -t metadatos-app:$(date +%Y%m%d) .

# 3. Ejecutar nuevo contenedor
podman run -d \
  --name metadatos-app \
  -p 5000:5000 \
  --env-file .env.docker \
  -v metadatos_data:/app/data \
  -v metadatos_uploads:/app/uploads \
  -v metadatos_logs:/app/logs \
  metadatos-app:$(date +%Y%m%d)

# 4. Verificar que funciona
podman logs metadatos-app
curl http://localhost:5000/health
```

---

## 🚨 **Troubleshooting**

### **Problemas Comunes**

#### **1. Contenedor no inicia**
```bash
# Ver logs detallados
podman logs metadatos-app

# Ver eventos del sistema
podman events --filter container=metadatos-app

# Verificar configuración
podman inspect metadatos-app
```

#### **2. Problemas de permisos**
```bash
# Verificar permisos dentro del contenedor
podman exec -it metadatos-app ls -la /app

# Verificar usuario que ejecuta la app
podman exec -it metadatos-app whoami

# Corregir permisos si es necesario
podman exec -it metadatos-app chmod -R 777 /app/uploads /app/logs /app/data
```

#### **3. No puede conectar a la aplicación**
```bash
# Verificar puertos mapeados
podman port metadatos-app

# Verificar que el servicio escucha en el puerto correcto
podman exec -it metadatos-app netstat -tulpn | grep :5000

# Probar conexión desde dentro del contenedor
podman exec -it metadatos-app curl -f http://localhost:5000/health
```

#### **4. Problemas con volúmenes**
```bash
# Verificar que los volúmenes están montados
podman exec -it metadatos-app df -h

# Verificar contenido de los volúmenes
podman exec -it metadatos-app ls -la /app/data /app/uploads /app/logs

# Recrear volúmenes si es necesario
podman volume rm metadatos_data metadatos_uploads metadatos_logs
```

#### **5. Problemas de memoria**
```bash
# Verificar uso de recursos
podman stats metadatos-app

# Aumentar límites si es necesario (en docker-compose.yml)
# memory: 1024M
```

### **Logs y Debugging**

```bash
# Ver logs de aplicación dentro del contenedor
podman exec -it metadatos-app tail -f /app/logs/app.log

# Ver logs del sistema Podman
journalctl -u podman

# Modo debug temporal
podman run -it --rm \
  --env-file .env.docker \
  -e FLASK_DEBUG=True \
  -p 5000:5000 \
  metadatos-app:latest
```

---

## 🔒 **Consideraciones de Seguridad**

### **Mejores Prácticas**

1. **Cambiar credenciales por defecto**:
   ```bash
   # Editar .env.docker con valores seguros
   SECRET_KEY=tu-clave-muy-segura-aqui
   ADMIN_PASSWORD=ContraseñaSuperSegura123!
   ```

2. **Usar usuario no-root** (Podman ya es rootless por defecto)

3. **Limitar recursos**:
   ```bash
   # En docker-compose.yml ya están configurados los límites
   ```

4. **Actualizar regularmente**:
   ```bash
   # Reconstruir con imagen base actualizada
   podman build --no-cache -f Dockerfile.optimized -t metadatos-app:latest .
   ```

5. **Backup regular**:
   ```bash
   # Script de backup automatizado
   podman run --rm -v metadatos_data:/data -v $(pwd):/backup alpine \
     tar czf /backup/metadatos_backup_$(date +%Y%m%d_%H%M%S).tar.gz -C /data .
   ```

---

## 🎯 **Comandos de Producción**

### **Configuración para Producción**

```bash
# Variables de entorno de producción
cat > .env.production << 'EOF'
SECRET_KEY=clave-super-secreta-produccion-cambiar
FLASK_ENV=production
FLASK_DEBUG=False
ADMIN_USERNAME=admin_prod
ADMIN_PASSWORD=PasswordProduccionSegura2024!
BASE_URL=https://tu-dominio.com
LOG_LEVEL=WARNING
EOF

# Ejecutar en modo producción
podman run -d \
  --name metadatos-app-prod \
  -p 80:5000 \
  --env-file .env.production \
  --restart unless-stopped \
  -v metadatos_data_prod:/app/data \
  -v metadatos_uploads_prod:/app/uploads \
  -v metadatos_logs_prod:/app/logs \
  metadatos-app:latest
```

### **Monitoreo**

```bash
# Crear script de monitoreo
cat > monitor.sh << 'EOF'
#!/bin/bash
while true; do
  if ! podman ps | grep -q metadatos-app; then
    echo "$(date): Contenedor no está corriendo, reiniciando..."
    podman start metadatos-app
  fi
  sleep 60
done
EOF

chmod +x monitor.sh
./monitor.sh &
```

---

¡Tu aplicación Metadatos App ahora está completamente containerizada con Podman! 🚀