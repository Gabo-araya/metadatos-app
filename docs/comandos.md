# Comandos
---

1. Crearemos un entorno virtual con Python
   ```bash
   python3 -m venv env
   ```

2. Activamos el entorno virtual
   ```bash
   source env/bin/activate
   source env/bin/activate; clear
   ```

3. Instalar Dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecutar la Aplicación:

   ```bash
   python app.py
   ```

   La aplicación estará disponible en `http://127.0.0.1:5000/`.

---

---

## 🚨 **Solución de Problemas**

### **Problemas Comunes**

#### **Error: "Secret key not configured"**
```bash
# Verificar que SECRET_KEY esté configurada
echo $SECRET_KEY

# Si está vacía, configurarla:
export SECRET_KEY="tu-clave-secreta-aqui"
```

#### **Error: "Permission denied" en uploads**
```bash
# Dar permisos a la carpeta uploads
chmod 755 uploads/
chown -R www-data:www-data uploads/  # En producción
```

#### **Error: "Database not found"**
```bash
# Inicializar base de datos
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

#### **Archivos no se muestran**
- Verificar permisos de la carpeta `uploads/`
- Confirmar que la ruta en `.env` sea correcta
- Revisar logs para errores específicos

### **Debugging**

```bash
# Activar modo debug
export FLASK_DEBUG=True
flask run

# Ver logs en tiempo real
tail -f app.log

# Verificar configuración
python -c "from app import app; print(app.config)"
```

---
