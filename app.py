from flask import Flask, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import logging
from datetime import datetime
from functools import wraps
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
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///metadatos.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    # Configuración de archivos permitidos
    ALLOWED_EXTENSIONS = {
        'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp',
        'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
        'odt', 'ods', 'odp',
        'zip', 'rar', '7z', 'tar', 'gz',
        'mp3', 'wav', 'ogg', 'mp4', 'avi', 'mkv', 'mov',
        'csv', 'json', 'xml'
    }

app = Flask(__name__)
app.config.from_object(Config)

# Asegúrate de que la carpeta de subida exista
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
init_db(app)

# Crear tablas en el contexto de la aplicación
with app.app_context():
    db.create_all()

# Credenciales de administración mejoradas
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'adminpass123!')
ADMIN_PASSWORD_HASH = generate_password_hash(ADMIN_PASSWORD)

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
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_file_size_mb(file_path):
    """Obtiene el tamaño del archivo en MB"""
    try:
        size_bytes = os.path.getsize(file_path)
        return round(size_bytes / (1024 * 1024), 2)
    except OSError:
        return 0

def login_required(f):
    """Decorador para rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
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
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

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
        current_app.logger.error(f'Error en página principal: {e}')
        flash('Error al cargar los archivos', 'danger')
        return render_template('index.html', files=None)

@app.route('/help')
def help_page():
    """Página de ayuda"""
    return render_template('help.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login para administradores"""
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')

            if not username or not password:
                flash('Por favor, completa todos los campos.', 'warning')
                return render_template('login.html')

            if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
                session['logged_in'] = True
                session['username'] = username
                session['login_time'] = datetime.now().isoformat()

                current_app.logger.info(f'Login exitoso para usuario: {username}')
                flash('Sesión iniciada correctamente.', 'success')

                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('admin_panel'))
            else:
                current_app.logger.warning(f'Intento de login fallido para usuario: {username}')
                flash('Usuario o contraseña incorrectos.', 'danger')

        except Exception as e:
            current_app.logger.error(f'Error en login: {e}')
            flash('Error interno del servidor', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    username = session.get('username', 'Usuario desconocido')
    session.clear()
    current_app.logger.info(f'Logout para usuario: {username}')
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():
    """Panel de administración"""
    if request.method == 'POST':
        try:
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()

            # Validaciones básicas
            if not title or not description:
                flash('Por favor, completa todos los campos.', 'warning')
                return redirect(request.url)

            if len(title) > 255:
                flash('El título es demasiado largo (máximo 255 caracteres).', 'warning')
                return redirect(request.url)

            if 'file' not in request.files:
                flash('No se seleccionó ningún archivo', 'warning')
                return redirect(request.url)

            file = request.files['file']

            if file.filename == '':
                flash('No se seleccionó ningún archivo', 'warning')
                return redirect(request.url)

            if not allowed_file(file.filename):
                flash('Tipo de archivo no permitido. Tipos permitidos: ' +
                      ', '.join(sorted(app.config['ALLOWED_EXTENSIONS'])), 'danger')
                return redirect(request.url)

            # Procesar archivo
            filename = secure_filename(file.filename)

            # Evitar duplicados de nombres
            counter = 1
            original_filename = filename
            while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                name, ext = os.path.splitext(original_filename)
                filename = f"{name}_{counter}{ext}"
                counter += 1

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Obtener tamaño del archivo
            file_size = get_file_size_mb(file_path)

            # Guardar en base de datos
            new_file = File(
                title=title,
                description=description,
                filename=filename,
                file_size=file_size
            )
            db.session.add(new_file)
            db.session.commit()

            current_app.logger.info(f'Archivo subido: {filename} por {session.get("username")}')
            flash(f'Archivo "{title}" subido exitosamente.', 'success')
            return redirect(url_for('admin_panel'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error subiendo archivo: {e}')
            flash(f'Error al subir el archivo: {str(e)}', 'danger')
            return redirect(request.url)

    # Mostrar archivos existentes
    try:
        page = request.args.get('page', 1, type=int)
        files = File.query.order_by(File.upload_date.desc()).paginate(
            page=page, per_page=10, error_out=False
        )
        return render_template('admin.html', files=files)
    except Exception as e:
        current_app.logger.error(f'Error cargando panel admin: {e}')
        flash('Error al cargar los archivos', 'danger')
        return render_template('admin.html', files=None)

@app.route('/admin/delete/<int:file_id>', methods=['POST'])
@login_required
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

        current_app.logger.info(f'Archivo eliminado: {filename} por {session.get("username")}')
        flash(f'Archivo "{title}" eliminado exitosamente.', 'success')

    except FileNotFoundError:
        current_app.logger.warning(f'Archivo físico no encontrado: {filename}')
        db.session.delete(file_to_delete)
        db.session.commit()
        flash(f'Archivo "{title}" eliminado de la base de datos (archivo físico no encontrado).', 'warning')

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error eliminando archivo {file_id}: {e}')
        flash(f'Error al eliminar el archivo: {str(e)}', 'danger')

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
        current_app.logger.error(f'Error viendo archivo {file_id}: {e}')
        flash('Error al cargar el archivo', 'danger')
        return redirect(url_for('index'))


@app.route('/health')
def health_check():
    """Health check endpoint for Docker"""
    try:
        # Verificar base de datos
        db.session.execute(db.text('SELECT 1'))
        return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500


if __name__ == '__main__':
    app.run(debug=True)
