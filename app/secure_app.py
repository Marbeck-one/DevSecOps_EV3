# app/secure_app.py
from flask import Flask, request, render_template, session, redirect, url_for
from prometheus_flask_exporter import PrometheusMetrics # Para monitoreo
import sqlite3
import os
import hashlib
import secrets

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Inicializar métricas de Prometheus (IL 3.2 y 3.5)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')

def get_db_connection():
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = hash_password(password)

        conn = get_db_connection()
        # CORRECCIÓN DE SEGURIDAD: Uso de parámetros para evitar SQL Injection
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                            (username, hashed_pw)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            return "Credenciales inválidas", 401
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    # CORRECCIÓN: Filtrar comentarios solo del usuario o ver lógica de negocio
    comments = conn.execute('SELECT * FROM comments').fetchall()
    conn.close()
    
    return render_template('dashboard.html', comments=comments)

@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    comment = request.form['comment']
    user_id = session['user_id']

    conn = get_db_connection()
    # CORRECCIÓN: Inserción segura
    conn.execute("INSERT INTO comments (user_id, comment) VALUES (?, ?)", (user_id, comment))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Generar token CSRF al cargar la página de login y guardarlo en sesión
    if request.method == 'GET':
        if 'csrf_token' not in session:
            session['csrf_token'] = secrets.token_hex(16)
            
    if request.method == 'POST':
        # ... (tu lógica de validación de usuario) ...
        # Si el login es exitoso:
            session['user_id'] = user['id']
            session['role'] = user['role']
            # Regenerar token por seguridad al loguearse
            session['csrf_token'] = secrets.token_hex(16) 
            return redirect(url_for('dashboard'))
            
    return render_template('login.html')

@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    # --- VALIDACIÓN CSRF ---
    token_formulario = request.form.get('csrf_token')
    token_sesion = session.get('csrf_token')
    
    if not token_formulario or token_formulario != token_sesion:
        return "Error de seguridad: Token CSRF inválido", 403

# Inicialización de DB si se ejecuta directo
if __name__ == '__main__':
    # Aseguramos que la DB exista
    if not os.path.exists('example.db'):
        import create_db
    app.run(host='0.0.0.0', port=5000)
