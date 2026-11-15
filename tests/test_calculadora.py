# tests/test_calculadora.py
import pytest
from app.calculadora import sumar, restar, multiplicar, dividir, potencia, modulo

def test_sumar():
    assert sumar(2, 3) == 5
    assert sumar(-1, 1) == 0
    assert sumar(0, 0) == 0

def test_restar():
    assert restar(5, 2) == 3
    assert restar(1, -1) == 2
    assert restar(0, 0) == 0

def test_multiplicar():
    assert multiplicar(2, 3) == 6
    assert multiplicar(-1, 5) == -5
    assert multiplicar(0, 10) == 0

def test_dividir():
    assert dividir(10, 2) == 5.0
    assert dividir(5, -1) == -5.0
    with pytest.raises(ZeroDivisionError):
        dividir(1, 0)

def test_operaciones_con_decimales():
    assert sumar(0.1, 0.2) == pytest.approx(0.3)
    assert restar(0.3, 0.1) == pytest.approx(0.2)
    assert multiplicar(1.5, 0.2) == pytest.approx(0.3)
    assert dividir(1, 3) == pytest.approx(0.3333333)


def test_operaciones_con_dos_negativos():
    assert sumar(-2, -3) == -5
    assert restar(-5, -2) == -3
    assert multiplicar(-4, -2) == 8
    assert dividir(-10, -2) == 5.0


def test_potencia():
    assert potencia(2, 3) == 8
    assert potencia(5, 0) == 1
    assert potencia(-2, 3) == -8
    assert potencia(2, -1) == pytest.approx(0.5)
    assert potencia(9, 0.5) == pytest.approx(3.0)


def test_potencia_cero_con_exponente_negativo():
    with pytest.raises(ZeroDivisionError):
        potencia(0, -1)


def test_potencia_resultado_no_real():
    with pytest.raises(ValueError):
        potencia(-8.0, 0.5)


def test_potencia_resultado_demasiado_grande():
    with pytest.raises(OverflowError):
        potencia(10.0, 1000.0)


def test_modulo():
    assert modulo(10, 3) == 1
    assert modulo(9, 3) == 0
    assert modulo(5.5, 2) == pytest.approx(1.5)
    # El resultado toma el signo del divisor
    assert modulo(-7, 3) == 2
    assert modulo(7, -3) == -2


def test_modulo_por_cero():
    with pytest.raises(ZeroDivisionError):
        modulo(5, 0)
