# Práctica Integradora RA1 (Criterios d, e y f): Gestor de Sesiones de Aula

## 1. Explicación del modelo
El módulo `sesion_aula.py` modela las sesiones de uso de aulas en un centro de formación mediante la clase `SesionAula`[cite: 45]. Cada instancia almacena los datos propios de la sesión (`aula`, `profesor`, `alumnos`, `log_path`) y el estado del fichero de registro (`_log`, `_cerrada`), mientras que la clase mantiene datos comunes (`centro`, `total_sesiones`)[cite: 45]. El protocolo de gestor de contexto (`__enter__` y `__exit__`) garantiza la apertura y el cierre ordenado del archivo de registro[cite: 40, 45, 46].

## 2. Diferencia entre clase e instancia
* **Clase (`SesionAula`):** Es la plantilla o molde que define la estructura, las validaciones de construcción, los métodos y los atributos compartidos (`centro = "CFGS Python"` y `total_sesiones`)[cite: 27, 45]. En Python, la propia clase también es un objeto (`type(SesionAula)` es `<class 'type'>`)[cite: 27, 28].
* **Instancia (`sesion_1`, `sesion_2`):** Es cada objeto concreto fabricado a partir de la clase, con su propia identidad (`sesion_1 is sesion_2` es `False`) y su propio espacio de nombres en `__dict__`[cite: 27, 28, 30]. Si se asigna un atributo con el mismo nombre que un atributo de clase en una instancia (por ejemplo, `sesion_1.centro = "Campus Norte"`), se crea un atributo de instancia que "tapa" al de clase solo para ese objeto[cite: 29].

## 3. Explicación de `__init__`, `__new__` y `__del__`
* **`__new__`:** Es el método de creación que construye y devuelve la nueva instancia antes de inicializarla (heredado de `object` si no se sobrescribe)[cite: 28, 33].
* **`__init__`:** Es el inicializador que recibe la instancia ya creada (`self`)[cite: 33, 34]. Valida que `aula`, `profesor` y `log_path` no estén vacíos y que `alumnos` sea un entero positivo, normaliza las cadenas y los contadores, e incrementa `SesionAula.total_sesiones`[cite: 35, 45].
* **`__del__`:** Es el destructor, invocado cuando el objeto va a ser destruido al perder sus referencias[cite: 39]. En esta práctica se limita a mostrar un aviso si `_cerrada` es `False` y protege su ejecución con `try...except` para evitar fallos durante el apagado del intérprete[cite: 46].

## 4. Justificación del uso de `with` y limitaciones de `__del__`
* **Por qué usar `with`:** La sentencia `with` invoca `__enter__` al entrar y garantiza que `__exit__` se ejecute al salir del bloque, tanto si todo va bien como si se produce una excepción[cite: 40, 41]. Esto asegura el cierre determinista del fichero y el registro del error sin silenciarlo (`return False`)[cite: 40, 41, 46].
* **Limitaciones de `__del__`:** En Python el momento exacto de ejecución de `__del__` no está garantizado (depende del conteo de referencias, posibles ciclos en el recolector de basura o el estado del apagado del intérprete), y las excepciones dentro de `__del__` se ignoran[cite: 39]. Por ello, no debe emplearse como mecanismo principal para liberar recursos como ficheros[cite: 39, 41, 46].

## 5. Ejemplo de ejecución
Al ejecutar `python sesion_aula.py`, se obtiene una salida equivalente a:

```text
=== 1. INSTANCIACIÓN, TIPOS Y __dict__ ===
type(SesionAula): <class 'type'>
type(sesion_1): <class 'sesion_aula.SesionAula'>
isinstance(sesion_1, SesionAula): True
sesion_1 is sesion_2: False
sesion_1.__dict__: {'aula': 'Aula 101', 'profesor': 'Laura Gómez', 'alumnos': 24, 'log_path': 'sesion_101.log', '_log': None, '_cerrada': False}
sesion_2.__dict__: {'aula': 'Aula 204', 'profesor': 'Carlos Ruiz', 'alumnos': 18, 'log_path': 'sesion_204.log', '_log': None, '_cerrada': False}

=== 2. ATRIBUTO DE CLASE VS ATRIBUTO DE INSTANCIA ===
SesionAula.centro: CFGS Python
sesion_1.centro: CFGS Python
sesion_2.centro: CFGS Python
Tras asignar sesion_1.centro = 'Campus Norte':
  sesion_1.centro: Campus Norte
  sesion_2.centro: CFGS Python
  SesionAula.centro: CFGS Python

=== 3. USO DE 'with' Y REGISTRO NORMAL ===
¿sesion_1._cerrada tras salir de with?: True

=== 4. EXCEPCIÓN DENTRO DE 'with' (VERIFICACIÓN DE __exit__) ===
Excepción capturada fuera del bloque with: Fallo de red simulado en el aula
¿sesion_2._cerrada tras error en with?: True

=== 5. TOTAL DE SESIONES CREADAS ===
SesionAula.total_sesiones: 3

=== 6. AVISO DE __del__ SI NO SE USA 'with' ===
Aviso (__del__): la sesión del aula 'Aula 302' (sesion_302.log) no se cerró mediante 'with'.