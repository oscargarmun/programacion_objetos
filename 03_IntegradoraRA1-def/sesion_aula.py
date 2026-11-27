"""Módulo que implementa un gestor de sesiones de aula con registro en fichero."""

from datetime import datetime
from typing import IO, Any


class SesionAula:
    """Modela una sesión de aula y gestiona su registro mediante gestor de contexto."""

    centro: str = "CFGS Python"
    total_sesiones: int = 0

    def __init__(
        self,
        aula: str,
        profesor: str,
        alumnos: int,
        log_path: str,
    ) -> None:
        """Valida los datos, normaliza campos e inicializa la sesión."""
        if not isinstance(aula, str) or not aula.strip():
            raise ValueError("El nombre del aula no puede estar vacío.")
        if not isinstance(profesor, str) or not profesor.strip():
            raise ValueError("El nombre del profesor no puede estar vacío.")
        if isinstance(alumnos, bool) or not isinstance(alumnos, int) or alumnos <= 0:
            raise ValueError("El número de alumnos debe ser un entero positivo.")
        if not isinstance(log_path, str) or not log_path.strip():
            raise ValueError("La ruta del fichero de registro no puede estar vacía.")

        self.aula: str = aula.strip()
        self.profesor: str = profesor.strip()
        self.alumnos: int = alumnos
        self.log_path: str = log_path.strip()
        self._log: IO[str] | None = None
        self._cerrada: bool = False

        SesionAula.total_sesiones += 1

    def __enter__(self) -> "SesionAula":
        """Abre el fichero de registro en modo append, escribe el inicio y devuelve self."""
        self._log = open(self.log_path, "a", encoding="utf-8")
        self._cerrada = False
        marca_tiempo = datetime.now().isoformat(timespec="seconds")
        self._log.write(
            f"[{marca_tiempo}] INICIO SESIÓN | Centro: {self.centro} | "
            f"Aula: {self.aula} | Profesor: {self.profesor} | Alumnos: {self.alumnos}\n"
        )
        self._log.flush()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> bool:
        """Escribe línea de cierre o error, cierra el fichero y no silencia excepciones."""
        marca_tiempo = datetime.now().isoformat(timespec="seconds")
        try:
            if self._log is not None and not self._log.closed:
                if exc_type is None:
                    self._log.write(
                        f"[{marca_tiempo}] FIN SESIÓN | Aula: {self.aula} | Cierre normal\n"
                    )
                else:
                    nombre_error = getattr(exc_type, "__name__", str(exc_type))
                    self._log.write(
                        f"[{marca_tiempo}] ERROR EN SESIÓN | Aula: {self.aula} | "
                        f"Excepción: {nombre_error}: {exc_val}\n"
                    )
                self._log.flush()
        finally:
            if self._log is not None and not self._log.closed:
                self._log.close()
            self._cerrada = True

        return False

    def registrar(self, mensaje: str) -> None:
        """Valida que el recurso esté abierto y escribe un mensaje en el registro."""
        if not isinstance(mensaje, str) or not mensaje.strip():
            raise ValueError("El mensaje a registrar no puede estar vacío.")
        if self._log is None or self._log.closed or self._cerrada:
            raise RuntimeError(
                "El registro no está abierto. Use la sesión dentro de un bloque 'with'."
            )
        marca_tiempo = datetime.now().isoformat(timespec="seconds")
        self._log.write(f"[{marca_tiempo}] {mensaje.strip()}\n")
        self._log.flush()

    def __del__(self) -> None:
        """Emite un aviso si la sesión no se cerró con el gestor de contexto."""
        try:
            if not self._cerrada:
                print(
                    f"Aviso (__del__): la sesión del aula '{self.aula}' "
                    f"({self.log_path}) no se cerró mediante 'with'."
                )
        except Exception:
            pass


def main() -> None:
    """Demostración de clases, instancias, constructor, with y __del__."""
    print("=== 1. INSTANCIACIÓN, TIPOS Y __dict__ ===")
    sesion_1 = SesionAula("  Aula 101 ", " Laura Gómez ", 24, "sesion_101.log")
    sesion_2 = SesionAula("Aula 204", "Carlos Ruiz", 18, "sesion_204.log")

    print("type(SesionAula):", type(SesionAula))
    print("type(sesion_1):", type(sesion_1))
    print("isinstance(sesion_1, SesionAula):", isinstance(sesion_1, SesionAula))
    print("sesion_1 is sesion_2:", sesion_1 is sesion_2)
    print("sesion_1.__dict__:", sesion_1.__dict__)
    print("sesion_2.__dict__:", sesion_2.__dict__)

    print("\n=== 2. ATRIBUTO DE CLASE VS ATRIBUTO DE INSTANCIA ===")
    print("SesionAula.centro:", SesionAula.centro)
    print("sesion_1.centro:", sesion_1.centro)
    print("sesion_2.centro:", sesion_2.centro)

    # Al asignar sesion_1.centro se crea un atributo de instancia que tapa al de clase
    sesion_1.centro = "Campus Norte"
    print("Tras asignar sesion_1.centro = 'Campus Norte':")
    print("  sesion_1.centro:", sesion_1.centro)
    print("  sesion_2.centro:", sesion_2.centro)
    print("  SesionAula.centro:", SesionAula.centro)

    print("\n=== 3. USO DE 'with' Y REGISTRO NORMAL ===")
    with sesion_1 as s1:
        s1.registrar("Inicio de práctica de POO en Python.")
        s1.registrar("Revisión de ejercicios sobre __init__ y __enter__.")
    print("¿sesion_1._cerrada tras salir de with?:", sesion_1._cerrada)

    print("\n=== 4. EXCEPCIÓN DENTRO DE 'with' (VERIFICACIÓN DE __exit__) ===")
    try:
        with sesion_2 as s2:
            s2.registrar("Cargando entorno de laboratorio...")
            raise RuntimeError("Fallo de red simulado en el aula")
    except RuntimeError as error:
        print("Excepción capturada fuera del bloque with:", error)
    print("¿sesion_2._cerrada tras error en with?:", sesion_2._cerrada)

    print("\n=== 5. TOTAL DE SESIONES CREADAS ===")
    print("SesionAula.total_sesiones:", SesionAula.total_sesiones)

    print("\n=== 6. AVISO DE __del__ SI NO SE USA 'with' ===")
    sesion_sin_cerrar = SesionAula("Aula 302", "Elena Martín", 15, "sesion_302.log")
    del sesion_sin_cerrar


if __name__ == "__main__":
    main()