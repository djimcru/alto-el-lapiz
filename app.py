from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import random
import string
import uuid

app = Flask(__name__)
app.secret_key = 'alto-el-lapiz-key'
socketio = SocketIO(app)

# Datos compartidos en memoria
jugadores = {}
respuestas_globales = {}
letra_actual = random.choice(string.ascii_uppercase)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        jugador_id = str(uuid.uuid4())
        session['jugador_id'] = jugador_id
        jugadores[jugador_id] = {'nombre': nombre, 'respuestas': {}, 'puntos': 0, 'terminado': False}
        return redirect(url_for('juego'))
    return render_template('index.html')

@app.route('/juego')
def juego():
    jugador_id = session.get('jugador_id')
    if not jugador_id or jugador_id not in jugadores:
        return redirect(url_for('index'))
    categorias = ["Nombre", "Apellido", "Lugar", "Comida", "Animal", "Marca", "Objeto"]
    return render_template('juego.html', letra=letra_actual, categorias=categorias, nombre=jugadores[jugador_id]['nombre'])

@app.route('/enviar', methods=['POST'])
def enviar():
    jugador_id = session.get('jugador_id')
    if not jugador_id or jugador_id not in jugadores:
        return redirect(url_for('index'))

    respuestas = {}
    puntos = 0
    for campo in request.form:
        valor = request.form[campo]
        respuestas[campo] = valor
        if valor.lower().startswith(letra_actual.lower()):
            puntos += 10

    jugadores[jugador_id]['respuestas'] = respuestas
    jugadores[jugador_id]['puntos'] = puntos
    jugadores[jugador_id]['terminado'] = True

    # Notifica a todos cuando alguien termina
    socketio.emit('jugador_termino', {'jugador': jugadores[jugador_id]['nombre']})

    if all(j['terminado'] for j in jugadores.values()):
        # Todos terminaron
        socketio.emit('todos_terminaron', {'jugadores': jugadores})

    return redirect(url_for('resultado'))

@app.route('/resultado')
def resultado():
    jugador_id = session.get('jugador_id')
    jugador = jugadores.get(jugador_id, {})
    return render_template('resultado.html', jugador=jugador, letra=letra_actual, todos=jugadores)

if __name__ == '__main__':
    socketio.run(app, debug=True)

