from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from database import db, File, init_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metadatos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'supersecretkey'  # ¡Cambia esto en producción!

# Asegúrate de que la carpeta de subida exista
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
init_db(app)

# Nuevo código para Flask 2.3+
with app.app_context():
    db.create_all()

# Credenciales de administración (simplificado para un solo usuario)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD_HASH = generate_password_hash('adminpass') # ¡Cambia esto!

def create_admin_user():
    # En una aplicación real, esto se manejaría mejor, quizás con una migración o un script de setup
    pass # Ya que es un usuario fijo, no necesitamos crearlo en la DB aquí.

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash('Por favor, inicia sesión para acceder a esta página.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    files = File.query.order_by(File.upload_date.desc()).all()
    return render_template('index.html', files=files)

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['logged_in'] = True
            flash('Sesión iniciada correctamente.', 'success')
            return redirect(url_for('admin_panel'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        if 'file' not in request.files:
            flash('No se seleccionó ningún archivo', 'danger')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No se seleccionó ningún archivo', 'danger')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            new_file = File(title=title, description=description, filename=filename)
            db.session.add(new_file)
            db.session.commit()
            flash('Archivo subido exitosamente.', 'success')
            return redirect(url_for('admin_panel'))

    files = File.query.order_by(File.upload_date.desc()).all()
    return render_template('admin.html', files=files)

@app.route('/admin/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    file_to_delete = File.query.get_or_404(file_id)
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_to_delete.filename))
        db.session.delete(file_to_delete)
        db.session.commit()
        flash('Archivo eliminado exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al eliminar el archivo: {e}', 'danger')
    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    app.run(debug=True)
