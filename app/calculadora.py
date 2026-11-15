"""Operaciones aritméticas básicas de la calculadora."""

# IMPORTANTE: reemplaza ??? con los nombres completos de los 3 integrantes,
# separados por " | " y en el mismo orden de la sección Integrantes del README.
# Ejemplo: "Ana María Pérez | Luis Andrés Gómez | Sara Restrepo Ríos"
AUTOR = "Santiago Mesa Valencia | Jose Manuel Carvajal Aristizabal | Mateo Montoya Aristizabal"


def sumar(a, b):
    """Devuelve la suma de a y b."""
    return a + b


def restar(a, b):
    """Devuelve la resta de b a a (a - b)."""
    return a - b


def multiplicar(a, b):
    """Devuelve el producto de a y b."""
    return a * b


def dividir(a, b):
    """Devuelve el cociente a / b.

    Lanza ZeroDivisionError si b es cero.
    """
    if b == 0:
        raise ZeroDivisionError("No se puede dividir por cero")
    return a / b


def potencia(a, b):
    """Devuelve a elevado a la b (a ** b).

    Lanza ZeroDivisionError si a es cero y b es negativo, ValueError si el
    resultado no es un número real (base negativa con exponente fraccionario)
    y OverflowError si el resultado es demasiado grande.
    """
    resultado = a**b
    if isinstance(resultado, complex):
        raise ValueError("El resultado no es un número real")
    return resultado


def modulo(a, b):
    """Devuelve el resto de la división a / b (a % b).

    El resultado tiene el signo de b. Lanza ZeroDivisionError si b es cero.
    """
    if b == 0:
        raise ZeroDivisionError("No se puede dividir por cero")
    return a % b
