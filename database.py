from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()

class File(db.Model):
    """Modelo para archivos subidos"""

    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String(255), nullable=False, unique=True)
    original_filename = db.Column(db.String(255), nullable=True)  # Nombre original del archivo
    file_size = db.Column(db.Float, default=0.0)  # Tamaño en MB
    mime_type = db.Column(db.String(100), nullable=True)  # Tipo MIME
    upload_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Metadatos adicionales para Dublin Core
    dc_creator = db.Column(db.String(255), default='Metadatos App Admin')
    dc_subject = db.Column(db.String(500), nullable=True)  # Palabras clave/categorías
    dc_language = db.Column(db.String(10), default='es')
    dc_rights = db.Column(db.String(500), default='© 2024 Metadatos App. Todos los derechos reservados.')

    def __repr__(self):
        return f'<File {self.title}>'

    @property
    def file_extension(self):
        """Obtiene la extensión del archivo"""
        if '.' in self.filename:
            return self.filename.rsplit('.', 1)[1].lower()
        return ''

    @property
    def is_image(self):
        """Verifica si el archivo es una imagen"""
        image_extensions = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'}
        return self.file_extension in image_extensions

    @property
    def is_document(self):
        """Verifica si el archivo es un documento"""
        doc_extensions = {'pdf', 'doc', 'docx', 'txt', 'rtf'}
        return self.file_extension in doc_extensions

    @property
    def is_media(self):
        """Verifica si el archivo es multimedia"""
        media_extensions = {'mp3', 'wav', 'ogg', 'mp4', 'avi', 'mkv', 'mov'}
        return self.file_extension in media_extensions

    @property
    def formatted_size(self):
        """Retorna el tamaño formateado"""
        if self.file_size < 1:
            return f"{int(self.file_size * 1024)} KB"
        return f"{self.file_size:.2f} MB"

    @property
    def short_description(self):
        """Retorna una descripción truncada para vistas de lista"""
        if len(self.description) <= 100:
            return self.description
        return self.description[:100] + "..."

    def to_dict(self):
        """Convierte el objeto a diccionario para APIs"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'filename': self.filename,
            'file_size': self.file_size,
            'file_extension': self.file_extension,
            'upload_date': self.upload_date.isoformat(),
            'is_image': self.is_image,
            'is_document': self.is_document,
            'is_media': self.is_media
        }

    @staticmethod
    def search(query):
        """Busca archivos por título o descripción"""
        return File.query.filter(
            db.or_(
                File.title.contains(query),
                File.description.contains(query),
                File.dc_subject.contains(query) if query else False
            )
        )

    @classmethod
    def get_stats(cls):
        """Obtiene estadísticas de archivos"""
        total_files = cls.query.count()
        total_size = db.session.query(db.func.sum(cls.file_size)).scalar() or 0

        # Archivos por tipo
        images = cls.query.filter(cls.filename.like('%.jpg')).count() + \
                cls.query.filter(cls.filename.like('%.jpeg')).count() + \
                cls.query.filter(cls.filename.like('%.png')).count() + \
                cls.query.filter(cls.filename.like('%.gif')).count()

        documents = cls.query.filter(cls.filename.like('%.pdf')).count() + \
                   cls.query.filter(cls.filename.like('%.doc')).count() + \
                   cls.query.filter(cls.filename.like('%.docx')).count()

        return {
            'total_files': total_files,
            'total_size_mb': round(total_size, 2),
            'images': images,
            'documents': documents,
            'others': total_files - images - documents
        }

class ActivityLog(db.Model):
    """Modelo para registrar actividades de administración"""

    __tablename__ = 'activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)  # 'upload', 'delete', 'login', 'logout'
    description = db.Column(db.String(500), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv4 o IPv6
    user_agent = db.Column(db.Text, nullable=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relación con File
    file = db.relationship('File', backref=db.backref('logs', lazy=True))

    def __repr__(self):
        return f'<ActivityLog {self.action} by {self.username}>'

    @classmethod
    def log_activity(cls, action, description, username, ip_address=None, user_agent=None, file_id=None):
        """Registra una actividad con manejo seguro de transacciones"""
        try:
            # Usar transacción explícita para mejor aislamiento
            with db.session.begin():
                log = cls(
                    action=action,
                    description=description,
                    username=username,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    file_id=file_id
                )
                db.session.add(log)
                # Commit automático al salir del bloque with
        except Exception as e:
            # Import here to avoid circular imports
            import uuid
            error_id = str(uuid.uuid4())[:8]
            print(f"Error ID {error_id} logging activity: {type(e).__name__}")
            # También log en el sistema de logging si está disponible
            try:
                from flask import current_app
                current_app.logger.error(f'Error ID {error_id} logging activity: {type(e).__name__}', exc_info=True)
            except (ImportError, RuntimeError):
                pass  # Flask context no disponible
            # No re-raise para evitar interrumpir el flujo principal
            return False
        return True

def check_db_connection():
    """Verifica conexión a base de datos de forma segura"""
    try:
        # Usar ORM en lugar de SQL raw
        result = db.session.query(db.literal(1)).scalar()
        return True
    except Exception:
        return False

def init_db(app):
    """Inicializa la base de datos con manejo mejorado de errores"""
    with app.app_context():
        try:
            # Verificar que el directorio de la base de datos existe
            db_url = app.config.get('SQLALCHEMY_DATABASE_URI', '')
            if db_url.startswith('sqlite:///'):
                db_path = db_url.replace('sqlite:///', '')
                if db_path.startswith('/'):
                    # Ruta absoluta
                    db_dir = os.path.dirname(db_path)
                else:
                    # Ruta relativa
                    db_dir = os.path.dirname(os.path.abspath(db_path))

                # Crear directorio si no existe
                if not os.path.exists(db_dir):
                    try:
                        os.makedirs(db_dir, exist_ok=True)
                        os.chmod(db_dir, 0o777)  # Permisos completos para Docker
                        print(f"✅ Directorio de BD creado: {db_dir}")
                    except Exception as e:
                        print(f"⚠️ Error creando directorio de BD {db_dir}: {type(e).__name__}")
                        raise

                # Verificar permisos del directorio
                if not os.access(db_dir, os.W_OK):
                    print(f"⚠️ Sin permisos de escritura en {db_dir}")
                    try:
                        os.chmod(db_dir, 0o777)
                        print(f"✅ Permisos corregidos para {db_dir}")
                    except Exception as e:
                        print(f"❌ No se pudieron corregir permisos: {type(e).__name__}")
                        raise

            # Crear todas las tablas solo si no existen
            try:
                db.create_all()
                print("✅ Base de datos inicializada correctamente")
            except Exception as e:
                if "already exists" in str(e).lower():
                    print("ℹ️ Tablas de BD ya existen, continuando...")
                else:
                    print(f"⚠️ Error creando tablas: {type(e).__name__}")
                    raise

            # Verificar que la BD funciona usando método seguro
            try:
                if check_db_connection():
                    print("✅ Conexión a base de datos verificada")
                else:
                    print("⚠️ Conexión a base de datos falló")
                    raise Exception("Database connection test failed")
            except Exception as e:
                print(f"⚠️ Error verificando conexión a BD: {type(e).__name__}")
                raise

        except Exception as e:
            print(f"❌ Error inicializando base de datos: {type(e).__name__}")
            print(f"❌ DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
            raise
