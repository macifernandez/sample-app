from flask import Flask, request
import sqlite3
import hashlib

app = Flask(__name__)

conn = sqlite3.connect('usuarios.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    usuario TEXT,
    password TEXT
)
''')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

usuarios = [
    ("maciel", hash_password("1234")),
    ("admin", hash_password("admin123"))
]

for usuario, password in usuarios:
    cursor.execute("SELECT * FROM usuarios WHERE usuario=?", (usuario,))
    existe = cursor.fetchone()

    if not existe:
        cursor.execute("INSERT INTO usuarios VALUES (?, ?)", (usuario, password))

conn.commit()

@app.route('/')
def inicio():
    return "Servidor Flask operativo en puerto 5000"

@app.route('/login')
def login():
    usuario = request.args.get('usuario')
    password = request.args.get('password')

    if usuario is None or password is None:
        return "Debe ingresar usuario y password"

    password_hash = hash_password(password)

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=? AND password=?",
        (usuario, password_hash)
    )

    resultado = cursor.fetchone()

    if resultado:
        return "Login correcto"
    else:
        return "Login incorrecto"

app.run(host='0.0.0.0', port=5000)
