"""Módulo de bienvenida para el curso de Programación Orientada a Objetos."""

class Saludo:
    """Clase encargada de gestionar los saludos del sistema."""

    def __init__(self, mensaje: str) -> None:
        self.mensaje = mensaje

    def mostrar(self) -> None:
        print(self.mensaje)


if __name__ == "__main__":
    saludo = Saludo("¡Hola, Mundo desde POO siguiendo PEP 8!")
    saludo.mostrar()