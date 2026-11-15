"""Aplicación web Flask que expone la calculadora mediante un formulario."""

import os
import secrets

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect

from .calculadora import dividir, modulo, multiplicar, potencia, restar, sumar

# Relaciona el valor del <select> del formulario con la función que lo calcula.
OPERACIONES = {
    "sumar": sumar,
    "restar": restar,
    "multiplicar": multiplicar,
    "dividir": dividir,
    "potencia": potencia,
    "modulo": modulo,
}

app = Flask(__name__)
# La clave firma la sesión y el token CSRF. En producción se define con la
# variable de entorno SECRET_KEY; si no existe, se genera una aleatoria.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
csrf = CSRFProtect(app)


@app.route("/", methods=["GET", "POST"])
def index():
    """Muestra el formulario y, si se envía, calcula y muestra el resultado."""
    resultado = None
    if request.method == "POST":
        try:
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            funcion = OPERACIONES.get(request.form["operacion"])

            if funcion is None:
                resultado = "Operación no válida"
            else:
                resultado = funcion(num1, num2)
        except ValueError:
            resultado = "Error: Introduce números válidos"
        except ZeroDivisionError:
            resultado = "Error: No se puede dividir por cero"
        except OverflowError:
            resultado = "Error: El resultado es demasiado grande"

    return render_template("index.html", resultado=resultado)


@app.route("/health")
def health():
    """Health check usado por el Load Balancer. Incluye la versión desplegada."""
    return {"status": "ok", "version": os.environ.get("APP_VERSION", "local")}


if __name__ == "__main__":  # pragma: no cover
    # Servidor de desarrollo: por defecto solo escucha en localhost y sin debug.
    # Para activarlos: FLASK_RUN_HOST=0.0.0.0 y FLASK_DEBUG=1
    app.run(
        host=os.environ.get("FLASK_RUN_HOST", "127.0.0.1"),
        port=int(os.environ.get("FLASK_RUN_PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )
