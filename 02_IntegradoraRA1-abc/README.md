# Práctica Integradora RA1 (Criterios a, b y c): CuentaUsuario

## 1. Explicación del modelo
El proyecto modela la entidad `CuentaUsuario` para una plataforma de formación aplicando los principios de la Programación Orientada a Objetos en Python:
* **Estado:** representado por atributos de instancia (`nombre`, `_email`, `__password_hash`, `_activa`, `_intentos_fallidos`) y atributos de clase (`MAX_INTENTOS`, `dominio`).
* **Comportamiento:** encapsulado en métodos públicos que separan las consultas de las modificaciones con validación.
* **Identidad:** cada instancia creada ocupa su propia referencia única comprobable mediante `id()` y el operador `is`.

## 2. Diferencia entre atributos de instancia y de clase
* **Atributos de clase (`MAX_INTENTOS`, `dominio`):** Se definen directamente en el cuerpo de la clase. Pertenecen a la clase y son compartidos por todas las instancias (todas las cuentas comparten el límite de 3 intentos y el dominio `formacion.local`).
* **Atributos de instancia (`self.nombre`, `self._email`, etc.):** Se definen dentro de `__init__` ligados a `self`. Cada objeto posee su propia copia independiente en su diccionario interno `__dict__`. Modificar el estado de `cuenta1` (por ejemplo, bloquearla por intentos fallidos) no altera el estado de `cuenta2`.

## 3. Diferencia entre método consultor y modificador
* **Métodos consultores (`esta_activa`, `puede_iniciar_sesion`, `perfil_publico`, `consultar_email`):** Devuelven información derivada del estado actual del objeto sin producir efectos secundarios (no modifican ningún atributo).
* **Métodos modificadores (`activar`, `desactivar`, `cambiar_email`, `registrar_intento_fallido`, `reiniciar_intentos`):** Alteran el estado interno del objeto. Antes de realizar el cambio aplican reglas de validación (por ejemplo, comprobar que el nuevo correo contenga `@` y pertenezca al dominio de la plataforma) para garantizar la integridad de los datos.

## 4. Reflexión sobre la visibilidad por convención
Python no bloquea el acceso externo a los atributos mediante palabras reservadas como `private` o `protected`; en su lugar utiliza convenciones y disciplina de diseño:
* **Público (`nombre`):** Forma parte de la interfaz pública de la clase y puede leerse o modificarse directamente.
* **Protegido (`_email`, `_activa`, `_intentos_fallidos`):** El guion bajo inicial indica a otros programadores que son detalles internos y deben manipularse únicamente a través de los métodos públicos de la clase.
* **Privado (`__password_hash`):** El doble guion bajo activa el mecanismo de *name mangling*, por el cual Python renombra el atributo internamente a `_CuentaUsuario__password_hash`. Esto evita sobrescrituras accidentales en subclases, pero **no proporciona seguridad real**, ya que cualquier código externo puede seguir leyendo o modificando el dato si utiliza el nombre transformado.

## 5. Ejemplo de ejecución
Al ejecutar `python cuenta_usuario.py` se obtiene una salida similar a:

```text
=== 1. CREACIÓN DE INSTANCIAS Y __dict__ ===
Tipo de cuenta1: <class '__main__.CuentaUsuario'>
cuenta1.__dict__: {'nombre': 'Ana García', '_email': 'ana@formacion.local', '_CuentaUsuario__password_hash': 'hash_secreto_123', '_activa': True, '_intentos_fallidos': 0}
cuenta2.__dict__: {'nombre': 'Luis Pérez', '_email': 'luis@formacion.local', '_CuentaUsuario__password_hash': 'hash_clave_999', '_activa': True, '_intentos_fallidos': 0}

=== 2. IDENTIDAD DE OBJETOS (is e id) ===
id(cuenta1): 140234891234560
id(cuenta2): 140234891234752
¿cuenta1 is cuenta2?: False
¿referencia_alias is cuenta1?: True

=== 3. ENVÍO DE MENSAJES E INDEPENDENCIA DE ESTADO ===
Perfil inicial cuenta1: Usuario: Ana García | Dominio: formacion.local | Estado: Activa
¿Puede iniciar sesión cuenta1?: True
Intento fallido 1 en cuenta1 -> Activa: True
Intento fallido 2 en cuenta1 -> Activa: True
Intento fallido 3 en cuenta1 -> Activa: False
¿Puede iniciar sesión cuenta1 tras 3 fallos?: False
¿Sigue activa cuenta2?: True
¿Puede iniciar sesión cuenta2?: True
Nuevo email cuenta1: ana.garcia@formacion.local
Validación correcta (error capturado): Email inválido: 'ana@gmail.com'. Debe contener '@' y terminar en '@formacion.local'.

=== 4. ATRIBUTOS DE CLASE Y NAME MANGLING ===
Atributo de clase desde la clase: formacion.local
Atributo de clase desde cuenta1: formacion.local
Atributo de clase desde cuenta2: formacion.local
Hash privado de cuenta1 (vía name mangling): hash_secreto_123
NOTA DE SEGURIDAD: El doble guion bajo solo renombra el atributo internamente (_Clase__atributo) para evitar colisiones accidentales; NO es cifrado ni seguridad real.