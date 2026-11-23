"""Módulo que modela las cuentas de usuario de una plataforma de formación."""


class CuentaUsuario:
    """Representa una cuenta de usuario dentro de la plataforma."""

    # Atributos de clase (compartidos por todas las instancias)
    MAX_INTENTOS: int = 3
    dominio: str = "formacion.local"

    def __init__(
        self,
        nombre: str,
        email: str,
        password_hash: str,
        activa: bool = True,
    ) -> None:
        """Inicializa una nueva instancia de CuentaUsuario."""
        self.nombre: str = nombre                  # Público
        self._email: str = ""                      # Protegido por convención
        self.__password_hash: str = password_hash  # Privado
        self._activa: bool = activa                # Protegido por convención
        self._intentos_fallidos: int = 0           # Protegido por convención

        # Usamos el modificador para validar el email desde la creación
        self.cambiar_email(email)

    # --- MÉTODOS CONSULTORES (no modifican el estado)

    def esta_activa(self) -> bool:
        """Indica si la cuenta se encuentra activa."""
        return self._activa

    def puede_iniciar_sesion(self) -> bool:
        """Comprueba si la cuenta está activa y no ha superado MAX_INTENTOS."""
        return self._activa and self._intentos_fallidos < self.MAX_INTENTOS

    def perfil_publico(self) -> str:
        """Devuelve una cadena con la información pública del usuario."""
        estado = "Activa" if self._activa else "Bloqueada/Inactiva"
        return f"Usuario: {self.nombre} | Dominio: {self.dominio} | Estado: {estado}"

    def consultar_email(self) -> str:
        """Devuelve el correo electrónico asociado a la cuenta."""
        return self._email

    # --- MÉTODOS MODIFICADORES (cambian el estado con validación)

    def activar(self) -> None:
        """Activa la cuenta del usuario."""
        self._activa = True

    def desactivar(self) -> None:
        """Desactiva la cuenta del usuario."""
        self._activa = False

    def cambiar_email(self, nuevo_email: str) -> None:
        """Valida y actualiza el email comprobando '@' y el dominio de clase."""
        sufijo_esperado = f"@{self.dominio}"
        if "@" not in nuevo_email or not nuevo_email.endswith(sufijo_esperado):
            raise ValueError(
                f"Email inválido: '{nuevo_email}'. Debe contener '@' y terminar en '{sufijo_esperado}'."
            )
        # Comprobamos que haya al menos un carácter antes de la arroba
        if nuevo_email.index("@") == 0:
            raise ValueError("El email debe tener un nombre de usuario antes de '@'.")
        self._email = nuevo_email

    def registrar_intento_fallido(self) -> None:
        """Incrementa los intentos fallidos y desactiva la cuenta al llegar al límite."""
        self._intentos_fallidos += 1
        if self._intentos_fallidos >= self.MAX_INTENTOS:
            self.desactivar()

    def reiniciar_intentos(self) -> None:
        """Restablece a cero el contador de intentos fallidos."""
        self._intentos_fallidos = 0


def main() -> None:
    """Función principal de demostración de los criterios a, b y c del RA1."""
    print("=== 1. CREACIÓN DE INSTANCIAS Y __dict__ ===")
    cuenta1 = CuentaUsuario("Ana García", "ana@formacion.local", "hash_secreto_123")
    cuenta2 = CuentaUsuario("Luis Pérez", "luis@formacion.local", "hash_clave_999")

    print("Tipo de cuenta1:", type(cuenta1))
    print("cuenta1.__dict__:", cuenta1.__dict__)
    print("cuenta2.__dict__:", cuenta2.__dict__)

    print("\n=== 2. IDENTIDAD DE OBJETOS (is e id) ===")
    print(f"id(cuenta1): {id(cuenta1)}")
    print(f"id(cuenta2): {id(cuenta2)}")
    print("¿cuenta1 is cuenta2?:", cuenta1 is cuenta2)  # False: son objetos distintos

    referencia_alias = cuenta1
    print("¿referencia_alias is cuenta1?:", referencia_alias is cuenta1)  # True: mismo objeto

    print("\n=== 3. ENVÍO DE MENSAJES E INDEPENDENCIA DE ESTADO ===")
    print("Perfil inicial cuenta1:", cuenta1.perfil_publico())
    print("¿Puede iniciar sesión cuenta1?:", cuenta1.puede_iniciar_sesion())

    # Simulamos 3 intentos fallidos en cuenta1
    for intento in range(1, 4):
        cuenta1.registrar_intento_fallido()
        print(f"Intento fallido {intento} en cuenta1 -> Activa: {cuenta1.esta_activa()}")

    print("¿Puede iniciar sesión cuenta1 tras 3 fallos?:", cuenta1.puede_iniciar_sesion())
    # Comprobamos que mutar cuenta1 no afecta en absoluto a cuenta2
    print("¿Sigue activa cuenta2?:", cuenta2.esta_activa())
    print("¿Puede iniciar sesión cuenta2?:", cuenta2.puede_iniciar_sesion())

    # Reactivación y cambio de email validado
    cuenta1.reiniciar_intentos()
    cuenta1.activar()
    cuenta1.cambiar_email("ana.garcia@formacion.local")
    print("Nuevo email cuenta1:", cuenta1.consultar_email())

    try:
        cuenta1.cambiar_email("ana@gmail.com")
    except ValueError as error:
        print("Validación correcta (error capturado):", error)

    print("\n=== 4. ATRIBUTOS DE CLASE Y NAME MANGLING ===")
    print("Atributo de clase desde la clase:", CuentaUsuario.dominio)
    print("Atributo de clase desde cuenta1:", cuenta1.dominio)
    print("Atributo de clase desde cuenta2:", cuenta2.dominio)

    # Acceso al atributo privado mediante name mangling
    print("Hash privado de cuenta1 (vía name mangling):", cuenta1._CuentaUsuario__password_hash)
    print(
        "NOTA DE SEGURIDAD: El doble guion bajo solo renombra el atributo internamente "
        "(_Clase__atributo) para evitar colisiones accidentales; NO es cifrado ni seguridad real."
    )


if __name__ == "__main__":
    main()