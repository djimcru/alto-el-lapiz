from flask import Flask, render_template, request
import random
import string
import os

app = Flask(__name__)

categorias = ["Nombre", "Apellido", "Lugar", "Comida", "Animal", "Marca", "Objeto"]
letra_actual = random.choice(string.ascii_uppercase)

@app.route("/", methods=["GET", "POST"])
def index():
    global letra_actual

    if request.method == "POST":
        respuestas = {cat.lower(): request.form.get(cat.lower()) for cat in categorias}
        errores = []
        puntaje = 0

        for campo, valor in respuestas.items():
            if valor and valor.lower().startswith(letra_actual.lower()):
                puntaje += 10
            else:
                errores.append(f"{campo.capitalize()} no empieza con la letra {letra_actual}")

        return render_template("resultado.html", respuestas=respuestas, errores=errores, letra=letra_actual, puntaje=puntaje)

    letra_actual = random.choice(string.ascii_uppercase)
    return render_template("index.html", letra=letra_actual, categorias=categorias)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
