import pytest
from calculadora import somar, subtrair, multiplicar, dividir

def test_somar():
    assert somar(10, 5) == 15
    assert somar(-1, 1) == 0

def test_subtrair():
    assert subtrair(10, 5) == 5
    assert subtrair(0, 5) == -5

def test_multiplicar():
    assert multiplicar(10, 5) == 50
    assert multiplicar(-2, 3) == -6

def test_dividir():
    assert dividir(10, 5) == 2.0
    assert dividir(7, 2) == 3.5

def test_dividir_por_zero():
    with pytest.raises(ValueError):
        dividir(10, 0)
