"""Programa principal de Mini Utilidades."""

from matematicas import suma, resta 
from textos import mayusculas, invertir


def main():
    print("Bienvenido a Mini Utilidades")
    print("Suma de 2 + 3 =", suma(2, 3))
    print("Resta de 5 - 1 =", resta(5, 1))
    print("En mayúsculas:", mayusculas("hola"))
    print("Invertido:", invertir("hola"))


if __name__ == "__main__":
    main()
