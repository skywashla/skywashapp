from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones'

# Leer usuarios desde archivo al iniciar
usuarios = {}
if os.path.exists('usuarios.txt'):
    with open('usuarios.txt', 'r') as f:
        for linea in f:
            if ':' in linea:
                usuario, clave = linea.strip().split(':')
                usuarios[usuario] = clave

# Ruta base para guardar archivos de formularios
directorio_guardado = 'formularios_guardados'
os.makedirs(directorio_guardado, exist_ok=True)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    usuario = request.form['usuario']
    clave = request.form['clave']
    if usuario in usuarios:
        return "El usuario ya existe. Usa otro nombre."
    with open('usuarios.txt', 'a') as f:
        f.write(f"{usuario}:{clave}\n")
    usuarios[usuario] = clave
    return redirect(url_for('login'))

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = request.form['usuario']
    clave = request.form['clave']
    if usuario in usuarios and usuarios[usuario] == clave:
        session['usuario'] = usuario
        return redirect(url_for('dashboard'))
    else:
        return "Usuario o clave incorrecta"

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', usuario=session['usuario'])

@app.route('/guardar/bitacora', methods=['POST'])
def guardar_bitacora():
    return guardar_formulario(request.form, 'bitacora')

@app.route('/guardar/libro', methods=['POST'])
def guardar_libro():
    return guardar_formulario(request.form, 'libro')

@app.route('/guardar/riesgo', methods=['POST'])
def guardar_riesgo():
    return guardar_formulario(request.form, 'riesgo')

def guardar_formulario(form_data, tipo):
    datos = dict(form_data)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_archivo = f"{tipo}_{timestamp}.txt"
    ruta_archivo = os.path.join(directorio_guardado, nombre_archivo)

    with open(ruta_archivo, 'w') as f:
        f.write(f"Formulario: {tipo}\n")
        f.write(f"Fecha y hora: {timestamp}\n")
        f.write("----------------------------------\n")
        for campo, valor in datos.items():
            f.write(f"{campo}: {valor}\n")

    return f"Formulario '{tipo}' guardado exitosamente."

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    