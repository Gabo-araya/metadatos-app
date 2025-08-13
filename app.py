from flask import Flask, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm, CSRFProtect
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
import os
import logging
import bleach
import re
import hashlib
import uuid
import json
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from database import db, File, init_db

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

class Config:
    # SECRET_KEY segura - requerida en producción
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        if os.environ.get('FLASK_ENV') == 'development':
            # Solo para desarrollo - generar clave consistente basada en path
            project_path = str(Path(__file__).parent)
            SECRET_KEY = 'dev-key-' + hashlib.sha256(project_path.encode()).hexdigest()[:32]
            print("⚠️ WARNING: Using development SECRET_KEY. Set SECRET_KEY environment variable for production!")
        else:
            raise RuntimeError("SECRET_KEY environment variable must be set in production!")
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///metadatos.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # No mostrar SQL en logs de producción
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

    # Configuración de archivos permitidos - más restrictiva
    ALLOWED_EXTENSIONS = {
        'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp',
        'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
        'odt', 'ods', 'odp', 'csv'
        # Removidas extensiones potencialmente peligrosas: xml, zip, rar, 7z, tar, gz, mp3, wav, ogg, mp4, avi, mkv, mov
    }
    
    @classmethod
    def validate_config(cls):
        """Valida que la configuración sea segura"""
        errors = []
        if not cls.SECRET_KEY:
            errors.append("SECRET_KEY is required")
        elif len(cls.SECRET_KEY) < 32:
            errors.append("SECRET_KEY must be at least 32 characters")
        
        if cls.MAX_CONTENT_LENGTH > 50 * 1024 * 1024:  # 50MB máximo
            errors.append("MAX_CONTENT_LENGTH should not exceed 50MB for security")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True

app = Flask(__name__)
app.config.from_object(Config)

# Validar configuración en startup
try:
    Config.validate_config()
except ValueError as e:
    print(f"❌ Configuration Error: {e}")
    if os.environ.get('FLASK_ENV') != 'development':
        raise

# Configuración de seguridad mejorada
app.config.update(
    # Configuración CSRF
    WTF_CSRF_TIME_LIMIT=None,  # Token CSRF no expira
    WTF_CSRF_SSL_STRICT=(os.environ.get('FLASK_ENV') == 'production'),
    WTF_CSRF_CHECK_DEFAULT=True,
    WTF_CSRF_METHODS=['POST', 'PUT', 'PATCH', 'DELETE'],
    
    # Configuración de sesiones segura
    SESSION_COOKIE_NAME='metadatos_session',
    SESSION_COOKIE_SECURE=(os.environ.get('FLASK_ENV') == 'production'),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=2),
    
    # Configuración de seguridad adicional
    SEND_FILE_MAX_AGE_DEFAULT=timedelta(hours=1),
    MAX_COOKIE_SIZE=4093  # Prevenir cookies muy grandes
)

# Configurar protección CSRF
csrf = CSRFProtect(app)

# Configurar rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)
limiter.init_app(app)

# Asegúrate de que la carpeta de subida exista
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
init_db(app)

# Crear tablas en el contexto de la aplicación
with app.app_context():
    db.create_all()

# Security headers para todas las respuestas
@app.after_request
def add_security_headers(response):
    """Añade cabeceras de seguridad a todas las respuestas"""
    # Prevenir ataques XSS
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # HSTS para HTTPS
    if request.is_secure:
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Content Security Policy
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "img-src 'self' data: https:; "
        "font-src 'self' https://cdn.jsdelivr.net; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )
    
    # Referrer Policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    return response

# Credenciales de administración - validación mejorada
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

if not ADMIN_USERNAME or not ADMIN_PASSWORD:
    if os.environ.get('FLASK_ENV') == 'development':
        ADMIN_USERNAME = 'admin'
        ADMIN_PASSWORD = 'dev-admin-password-change-me'
        print("⚠️ WARNING: Using default admin credentials in development mode!")
    else:
        raise RuntimeError("ADMIN_USERNAME and ADMIN_PASSWORD environment variables must be set in production!")

# Validar fortaleza de contraseña
if len(ADMIN_PASSWORD) < 12:
    if os.environ.get('FLASK_ENV') != 'development':
        raise RuntimeError("ADMIN_PASSWORD must be at least 12 characters long!")
    else:
        print("⚠️ WARNING: Admin password should be at least 12 characters!")

ADMIN_PASSWORD_HASH = generate_password_hash(ADMIN_PASSWORD)

# Formularios WTF para protección CSRF
class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[
        DataRequired(message='El usuario es obligatorio'),
        Length(min=3, max=50, message='El usuario debe tener entre 3 y 50 caracteres')
    ])
    password = StringField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria'),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ])
    submit = SubmitField('Iniciar Sesión')

class FileUploadForm(FlaskForm):
    title = StringField('Título', validators=[
        DataRequired(message='El título es obligatorio'),
        Length(min=3, max=255, message='El título debe tener entre 3 y 255 caracteres')
    ])
    description = TextAreaField('Descripción', validators=[
        DataRequired(message='La descripción es obligatoria'),
        Length(min=10, max=1000, message='La descripción debe tener entre 10 y 1000 caracteres')
    ])
    file = FileField('Archivo', validators=[
        FileRequired(message='Debe seleccionar un archivo'),
        FileAllowed(list(Config.ALLOWED_EXTENSIONS), 'Tipo de archivo no permitido')
    ])
    dc_subject = StringField('Palabras clave', validators=[
        Length(max=500, message='Las palabras clave no pueden exceder 500 caracteres')
    ])
    submit = SubmitField('Subir Archivo')
    
    def validate_file(self, field):
        if field.data:
            filename = field.data.filename
            if not is_safe_filename(filename):
                raise ValidationError('Nombre de archivo no válido o potencialmente peligroso')

# Diccionario mejorado para mapear extensiones de archivo a clases de íconos de Bootstrap
FILE_ICON_MAP = {
    # Documentos
    'pdf': 'bi-file-earmark-pdf-fill text-danger',
    'doc': 'bi-file-earmark-word-fill text-primary',
    'docx': 'bi-file-earmark-word-fill text-primary',
    'odt': 'bi-file-earmark-word-fill text-primary',
    'txt': 'bi-file-earmark-text-fill text-secondary',

    # Hojas de cálculo
    'xls': 'bi-file-earmark-excel-fill text-success',
    'xlsx': 'bi-file-earmark-excel-fill text-success',
    'ods': 'bi-file-earmark-excel-fill text-success',
    'csv': 'bi-file-earmark-spreadsheet-fill text-success',

    # Presentaciones
    'ppt': 'bi-file-earmark-ppt-fill text-warning',
    'pptx': 'bi-file-earmark-ppt-fill text-warning',
    'odp': 'bi-file-earmark-ppt-fill text-warning',

    # Imágenes
    'jpg': 'bi-file-earmark-image-fill text-info',
    'jpeg': 'bi-file-earmark-image-fill text-info',
    'png': 'bi-file-earmark-image-fill text-info',
    'gif': 'bi-file-earmark-image-fill text-info',
    'bmp': 'bi-file-earmark-image-fill text-info',
    'webp': 'bi-file-earmark-image-fill text-info',

    # Archivos comprimidos
    'zip': 'bi-file-earmark-zip-fill text-dark',
    'rar': 'bi-file-earmark-zip-fill text-dark',
    '7z': 'bi-file-earmark-zip-fill text-dark',
    'tar': 'bi-file-earmark-zip-fill text-dark',
    'gz': 'bi-file-earmark-zip-fill text-dark',

    # Audio
    'mp3': 'bi-file-earmark-music-fill text-purple',
    'wav': 'bi-file-earmark-music-fill text-purple',
    'ogg': 'bi-file-earmark-music-fill text-purple',

    # Video
    'mp4': 'bi-file-earmark-play-fill text-danger',
    'avi': 'bi-file-earmark-play-fill text-danger',
    'mkv': 'bi-file-earmark-play-fill text-danger',
    'mov': 'bi-file-earmark-play-fill text-danger',

    # Datos
    'json': 'bi-file-earmark-code-fill text-warning',
    'xml': 'bi-file-earmark-code-fill text-warning',
}

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    if not filename or not isinstance(filename, str):
        return False
    
    # Verificar que tenga extensión
    if '.' not in filename:
        return False
    
    # Verificar extensión permitida
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in app.config['ALLOWED_EXTENSIONS']

def sanitize_input(text, max_length=None):
    """Sanitiza entrada de usuario para prevenir XSS"""
    if not text:
        return ''
    
    # Limpiar HTML malicioso
    cleaned = bleach.clean(text, tags=[], attributes={}, strip=True)
    
    # Limitar longitud si se especifica
    if max_length and len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    
    return cleaned.strip()

def is_safe_filename(filename):
    """Verifica que el nombre del archivo sea seguro"""
    if not filename:
        return False
    
    # Patrones peligrosos
    dangerous_patterns = [
        r'\.\./',  # Path traversal
        r'[<>:"|?*]',  # Caracteres inválidos en Windows
        r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\..*)?$',  # Nombres reservados Windows
        r'\x00',  # Null byte
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, filename, re.IGNORECASE):
            return False
    
    return True

def generate_safe_filename(original_filename, upload_folder, max_length=100):
    """Genera un nombre de archivo seguro y único"""
    # Usar secure_filename primero
    name, ext = os.path.splitext(secure_filename(original_filename))
    
    # Truncar nombre si es muy largo
    max_name_length = max_length - len(ext) - 15  # espacio para timestamp y contador
    if len(name) > max_name_length:
        name = name[:max_name_length]
    
    # Intentar con timestamp primero para mayor unicidad
    timestamp = int(datetime.now().timestamp())
    filename = f"{name}_{timestamp}{ext}"
    
    counter = 1
    while os.path.exists(os.path.join(upload_folder, filename)):
        if counter > 9999:  # Prevenir bucle infinito
            # Usar UUID como último recurso
            filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
            break
        filename = f"{name}_{timestamp}_{counter:04d}{ext}"
        counter += 1
    
    return filename

def is_safe_redirect_url(target_url):
    """Valida que la URL de redirección sea segura"""
    if not target_url:
        return False
    
    # Solo permitir rutas relativas que empiecen con /
    if not target_url.startswith('/'):
        return False
    
    # No permitir // que podría ser usado para bypass
    if target_url.startswith('//'):
        return False
    
    # No permitir caracteres peligrosos
    if any(char in target_url for char in ['<', '>', '"', "'"]):
        return False
    
    # No permitir URLs que parezcan absolutas
    if ':' in target_url and not target_url.startswith('/'):
        return False
    
    return True

def get_file_size_mb(file_path):
    """Obtiene el tamaño del archivo en MB"""
    try:
        size_bytes = os.path.getsize(file_path)
        return round(size_bytes / (1024 * 1024), 2)
    except OSError:
        return 0

def safe_log_user_action(action, username=None, ip=None, additional_info=None, file_info=None):
    """Log de acciones de usuario sin exponer información sensible"""
    # Máscarar IP para privacidad
    masked_ip = 'unknown'
    if ip:
        parts = ip.split('.')
        if len(parts) == 4:
            masked_ip = f"{parts[0]}.{parts[1]}.xxx.xxx"
        else:
            masked_ip = f"{ip[:8]}***"  # Para IPv6
    
    # Máscarar username parcialmente
    safe_username = 'anonymous'
    if username and len(username) > 3:
        safe_username = f"{username[:3]}***"
    elif username:
        safe_username = f"{username[0]}***"
    
    # Preparar datos de log seguros
    log_data = {
        'action': action,
        'username': safe_username,
        'ip_masked': masked_ip,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    # Añadir información adicional de forma segura
    if additional_info:
        log_data['info'] = str(additional_info)[:100]  # Limitar longitud
    
    if file_info:
        log_data['file'] = str(file_info)[:50]  # Limitar información del archivo
    
    # Log estructurado para análisis
    current_app.logger.info(f"USER_ACTION: {json.dumps(log_data)}")

def login_required(f):
    """Decorador para rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar sesión activa
        if 'logged_in' not in session or not session['logged_in']:
            flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('login'))
        
        # Verificar tiempo de sesión (opcional)
        if 'login_time' in session:
            try:
                login_time = datetime.fromisoformat(session['login_time'])
                if datetime.now() - login_time > timedelta(hours=8):
                    session.clear()
                    flash('Tu sesión ha expirado por seguridad.', 'warning')
                    return redirect(url_for('login'))
            except (ValueError, TypeError):
                # Si hay error con el timestamp, limpiar sesión
                session.clear()
                flash('Sesión inválida. Por favor, inicia sesión nuevamente.', 'warning')
                return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    return decorated_function

# Función de contexto para plantillas
@app.context_processor
def utility_processor():
    def get_file_icon(filename):
        """Obtiene la clase de ícono según la extensión del archivo"""
        _, ext = os.path.splitext(filename)
        ext = ext.lstrip('.').lower()
        return FILE_ICON_MAP.get(ext, 'bi-file-earmark text-muted')

    def format_file_size(size_mb):
        """Formatea el tamaño del archivo"""
        if size_mb < 1:
            return f"{int(size_mb * 1024)} KB"
        return f"{size_mb} MB"

    def current_year():
        """Obtiene el año actual"""
        return datetime.now().year

    return dict(
        get_file_icon=get_file_icon,
        format_file_size=format_file_size,
        current_year=current_year
    )

@app.errorhandler(404)
def not_found_error(error):
    """Manejo seguro de errores 404"""
    # Log sin información sensible
    current_app.logger.warning(f'404 error - Path: {request.path}, IP: {get_remote_address()}')
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo seguro de errores internos"""
    try:
        db.session.rollback()
    except Exception:
        pass  # Evitar errores en cascada
    
    # Log con ID único para tracking sin exponer detalles
    error_id = str(uuid.uuid4())[:8]
    current_app.logger.error(f'500 error ID {error_id}: {type(error).__name__}', exc_info=True)
    
    return render_template('errors/500.html', error_id=error_id), 500

@app.errorhandler(413)
def too_large(e):
    flash('El archivo es demasiado grande. Tamaño máximo permitido: 16MB', 'danger')
    return redirect(request.url)

@app.route('/')
def index():
    """Página principal con lista de archivos"""
    try:
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str)

        query = File.query

        if search:
            query = query.filter(
                db.or_(
                    File.title.contains(search),
                    File.description.contains(search)
                )
            )

        files = query.order_by(File.upload_date.desc()).paginate(
            page=page, per_page=12, error_out=False
        )

        return render_template('index.html', files=files, search=search)
    except Exception as e:
        error_id = str(uuid.uuid4())[:8]
        current_app.logger.error(f'Error ID {error_id} en página principal: {type(e).__name__}', exc_info=True)
        flash('Error interno al cargar los archivos', 'danger')
        return render_template('index.html', files=None)

@app.route('/help')
def help_page():
    """Página de ayuda"""
    return render_template('help.html')

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    """Página de login para administradores"""
    form = LoginForm()
    
    if form.validate_on_submit():
        try:
            username = sanitize_input(form.username.data.strip(), 50)
            password = form.password.data
            
            # Log intento de login con información de seguridad
            client_ip = get_remote_address()
            user_agent = request.headers.get('User-Agent', 'Unknown')[:200]
            
            if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
                session.permanent = True
                session['logged_in'] = True
                session['username'] = username
                session['login_time'] = datetime.now().isoformat()
                session['client_ip'] = client_ip
                session['csrf_token'] = str(uuid.uuid4())

                # Log detallado tradicional para auditoría
                current_app.logger.info(f'Login exitoso - Usuario: {username}, IP: {client_ip}, User-Agent: {user_agent}')
                # Log seguro estructurado
                safe_log_user_action('LOGIN_SUCCESS', username, client_ip, 'successful_authentication')
                flash('Sesión iniciada correctamente.', 'success')

                next_page = request.args.get('next')
                if next_page and is_safe_redirect_url(next_page):
                    return redirect(next_page)
                return redirect(url_for('admin_panel'))
            else:
                # Log tradicional para auditoría  
                current_app.logger.warning(f'Login fallido - Usuario: {username}, IP: {client_ip}, User-Agent: {user_agent}')
                # Log seguro estructurado
                safe_log_user_action('LOGIN_FAILED', username, client_ip, 'authentication_failure')
                flash('Usuario o contraseña incorrectos.', 'danger')
                
                # Implementar delay para prevenir ataques de fuerza bruta
                import time
                time.sleep(1)

        except Exception as e:
            error_id = str(uuid.uuid4())[:8]
            current_app.logger.error(f'Error ID {error_id} en login: {type(e).__name__}', exc_info=True)
            flash(f'Error interno del servidor (ID: {error_id})', 'danger')
    
    elif form.errors:
        # Log errores de validación
        client_ip = get_remote_address()
        current_app.logger.warning(f'Errores de validación en login - IP: {client_ip}, Errores: {form.errors}')
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{error}', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    username = session.get('username', 'Usuario desconocido')
    client_ip = get_remote_address()
    
    # Log tradicional
    current_app.logger.info(f'Logout para usuario: {username}')
    # Log seguro estructurado
    safe_log_user_action('LOGOUT', username, client_ip, 'session_closed')
    
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
@login_required
@limiter.limit("10 per minute")
def admin_panel():
    """Panel de administración"""
    form = FileUploadForm()
    
    if form.validate_on_submit():
        try:
            title = sanitize_input(form.title.data.strip(), 255)
            description = sanitize_input(form.description.data.strip(), 1000)
            dc_subject = sanitize_input(form.dc_subject.data.strip() if form.dc_subject.data else '', 500)

            # Las validaciones están en el formulario WTF

            file = form.file.data
            
            # Validaciones adicionales de seguridad
            if not is_safe_filename(file.filename):
                flash('Nombre de archivo no válido o potencialmente peligroso', 'danger')
                return redirect(request.url)

            # Procesar archivo con generación segura de nombre
            filename = generate_safe_filename(file.filename, app.config['UPLOAD_FOLDER'])
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Obtener tamaño del archivo
            file_size = get_file_size_mb(file_path)

            # Guardar en base de datos con metadatos sanitizados
            new_file = File(
                title=title,
                description=description,
                filename=filename,
                file_size=file_size,
                dc_subject=dc_subject,
                original_filename=file.filename
            )
            db.session.add(new_file)
            db.session.commit()

            # Log detallado del evento de seguridad
            client_ip = get_remote_address()
            current_app.logger.info(f'Archivo subido - Usuario: {session.get("username")}, IP: {client_ip}, Archivo: {filename}, Tamaño: {file_size}MB, Título: {title[:50]}...')
            # Log seguro estructurado
            safe_log_user_action('FILE_UPLOAD', session.get('username'), client_ip, f'size:{file_size}MB', filename[:30])
            flash(f'Archivo "{title}" subido exitosamente.', 'success')
            return redirect(url_for('admin_panel'))

        except Exception as e:
            db.session.rollback()
            client_ip = get_remote_address()
            error_id = str(uuid.uuid4())[:8]
            current_app.logger.error(f'Error ID {error_id} subiendo archivo - Usuario: {session.get("username")}, IP: {client_ip}, Error: {type(e).__name__}', exc_info=True)
            flash(f'Error interno al subir el archivo (ID: {error_id})', 'danger')
            return redirect(request.url)
    
    elif form.errors:
        # Log errores de validación
        client_ip = get_remote_address()
        current_app.logger.warning(f'Errores de validación en upload - Usuario: {session.get("username")}, IP: {client_ip}, Errores: {form.errors}')
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{error}', 'danger')

    # Mostrar archivos existentes
    try:
        page = request.args.get('page', 1, type=int)
        files = File.query.order_by(File.upload_date.desc()).paginate(
            page=page, per_page=10, error_out=False
        )
        return render_template('admin.html', files=files, form=form)
    except Exception as e:
        error_id = str(uuid.uuid4())[:8]
        current_app.logger.error(f'Error ID {error_id} cargando panel admin: {type(e).__name__}', exc_info=True)
        flash('Error interno al cargar los archivos', 'danger')
        return render_template('admin.html', files=None, form=form)

@app.route('/admin/delete/<int:file_id>', methods=['POST'])
@login_required
@limiter.limit("5 per minute")
def delete_file(file_id):
    """Eliminar archivo"""
    try:
        file_to_delete = File.query.get_or_404(file_id)
        filename = file_to_delete.filename
        title = file_to_delete.title

        # Eliminar archivo físico
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        # Eliminar de base de datos
        db.session.delete(file_to_delete)
        db.session.commit()

        # Log detallado del evento de eliminación
        client_ip = get_remote_address()
        current_app.logger.info(f'Archivo eliminado - Usuario: {session.get("username")}, IP: {client_ip}, Archivo: {filename}, Título: {title}')
        # Log seguro estructurado
        safe_log_user_action('FILE_DELETE', session.get('username'), client_ip, f'file_id:{file_id}', filename[:30])
        flash(f'Archivo "{title}" eliminado exitosamente.', 'success')

    except FileNotFoundError:
        current_app.logger.warning(f'Archivo físico no encontrado: {filename}')
        db.session.delete(file_to_delete)
        db.session.commit()
        flash(f'Archivo "{title}" eliminado de la base de datos (archivo físico no encontrado).', 'warning')

    except Exception as e:
        db.session.rollback()
        error_id = str(uuid.uuid4())[:8]
        current_app.logger.error(f'Error ID {error_id} eliminando archivo {file_id}: {type(e).__name__}', exc_info=True)
        flash(f'Error interno al eliminar el archivo (ID: {error_id})', 'danger')

    return redirect(url_for('admin_panel'))

@app.route('/file/<int:file_id>')
def view_file(file_id):
    """Ver detalles de un archivo específico"""
    try:
        file = File.query.get_or_404(file_id)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        # Verificar si el archivo existe físicamente
        file_exists = os.path.exists(file_path)

        return render_template('file_detail.html', file=file, file_exists=file_exists)
    except Exception as e:
        error_id = str(uuid.uuid4())[:8]
        current_app.logger.error(f'Error ID {error_id} viendo archivo {file_id}: {type(e).__name__}', exc_info=True)
        flash('Error interno al cargar el archivo', 'danger')
        return redirect(url_for('index'))


@app.route('/health')
def health_check():
    """Health check endpoint for Docker"""
    try:
        # Verificar base de datos usando método seguro
        from database import check_db_connection
        
        if not check_db_connection():
            return {'status': 'unhealthy', 'reason': 'database_connection_failed'}, 500
        return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}, 200
    except Exception as e:
        error_id = str(uuid.uuid4())[:8]
        current_app.logger.error(f'Health check error ID {error_id}: {type(e).__name__}', exc_info=True)
        return {'status': 'unhealthy', 'error_id': error_id}, 500

# Funciones de utilidad de seguridad
def verify_file_integrity():
    """Verifica la integridad de los archivos subidos"""
    issues = []
    try:
        files = File.query.all()
        for file_record in files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_record.filename)
            if not os.path.exists(file_path):
                issues.append(f"Archivo faltante: {file_record.filename}")
            elif not os.access(file_path, os.R_OK):
                issues.append(f"Archivo sin permisos de lectura: {file_record.filename}")
    except Exception as e:
        error_id = str(uuid.uuid4())[:8]
        current_app.logger.error(f'Error ID {error_id} verificando integridad: {type(e).__name__}', exc_info=True)
        issues.append(f"Error verificando integridad (ID: {error_id})")
    
    if issues:
        current_app.logger.warning(f"Problemas de integridad encontrados: {issues}")
    
    return issues


if __name__ == '__main__':
    app.run(debug=True)
