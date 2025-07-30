---

## 🐳 **PARTE 2: Containerización con Podman**

### **Paso 1: Instalar Podman** (si no lo tienes)

**En Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install podman
```

**En CentOS/RHEL/Fedora**:
```bash
sudo dnf install podman
```

**En macOS**:
```bash
brew install podman
```

### **Paso 2: Crear Dockerfile**

En el directorio raíz del proyecto, crear `Dockerfile`:### **Paso 3: Crear .dockerignore**### **Paso 4: Crear docker-compose.yml**### **Paso 5: Crear nginx.conf (Opcional para Producción)**### **Paso 6: Agregar Health Check al app.py**

Agregar esta ruta a tu `app.py`:

```python
@app.route('/health')
def health_check():
    """Health check endpoint for Docker"""
    try:
        # Verificar base de datos
        db.session.execute('SELECT 1')
        return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500
```

### **Paso 7: Construir y Ejecutar con Podman**

```bash
# Crear archivo .env para Docker
cat > .env.docker << 'EOF'
SECRET_KEY=tu-clave-secreta-para-docker-cambiar-en-produccion
ADMIN_USERNAME=admin_docker
ADMIN_PASSWORD=Password_Docker_2024!
EOF

# Construir la imagen
podman build -t metadatos-app:latest .

# Verificar que se creó
podman images

# Ejecutar el contenedor (modo simple)
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
curl http://localhost:5000
```

### **Paso 8: Usar Docker Compose con Podman**

```bash
# Instalar podman-compose si no lo tienes
pip install podman-compose

# O usar docker-compose con podman
export DOCKER_HOST=unix:///run/user/$UID/podman/podman.sock

# Ejecutar con compose
podman-compose up -d

# Ver estado
podman-compose ps

# Ver logs
podman-compose logs -f metadatos-app

# Parar servicios
podman-compose down
```

### **Paso 9: Comandos Útiles de Podman**

```bash
# Ver contenedores corriendo
podman ps

# Ver todas las imágenes
podman images

# Entrar al contenedor
podman exec -it metadatos-app /bin/bash

# Ver logs en tiempo real
podman logs -f metadatos-app

# Parar contenedor
podman stop metadatos-app

# Reiniciar contenedor
podman restart metadatos-app

# Eliminar contenedor
podman rm metadatos-app

# Eliminar imagen
podman rmi metadatos-app:latest

# Ver uso de recursos
podman stats metadatos-app

# Inspeccionar contenedor
podman inspect metadatos-app
```

---

## 🔍 **Verificación y Troubleshooting**

### **Para PythonAnywhere:**

1. **Si la aplicación no carga**:
   - Revisar error log en Web tab
   - Verificar que el entorno virtual está correcto
   - Comprobar que el archivo WSGI es correcto

2. **Si hay errores de importación**:
   ```bash
   workon metadatos_env
   pip list | grep Flask
   ```

3. **Si la base de datos no funciona**:
   ```bash
   cd metadatos_project
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

### **Para Docker/Podman:**

1. **Si el contenedor no inicia**:
   ```bash
   podman logs metadatos-app
   ```

2. **Si hay problemas de permisos**:
   ```bash
   podman exec -it metadatos-app ls -la /app
   ```

3. **Si no puede conectar a la aplicación**:
   ```bash
   podman port metadatos-app
   ```

---
