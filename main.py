"""Programa principal de Mini Utilidades."""

from textos import mayusculas, invertir


def main():
    print("Bienvenido a Mini Utilidades")
    print("En mayúsculas:", mayusculas("hola"))
    print("Invertido:", invertir("hola"))


if __name__ == "__main__":
    main()