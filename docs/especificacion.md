# Especificación: sistema local de reservas de equipamiento

## 1. Objetivo y alcance

Desarrollar una aplicación local sencilla para consultar disponibilidad y gestionar reservas de equipamiento de laboratorio mediante un menú interactivo de línea de comandos (CLI). La aplicación persistirá las reservas en una base SQLite local.

El sistema permitirá crear reservas, comprobar si un equipo puede reservarse en un intervalo y cancelar reservas conservando sus registros. El alcance no incluye autenticación real, pagos, notificaciones ni integraciones externas. Tampoco se incorporan funciones adicionales no solicitadas, como administrar el catálogo de equipos.

## 2. Inventario inicial

| Identificador | Equipo |
|---|---|
| MIC-01 | Microscopio digital |
| MIC-02 | Microscopio digital |
| OSC-01 | Osciloscopio |
| MUL-01 | Multímetro |
| FUE-01 | Fuente de alimentación |

## 3. Requisitos funcionales del desafío original

### RF-01 — Consultar disponibilidad

El usuario podrá consultar si un equipo del inventario inicial está disponible para un intervalo. La consulta rechazará entradas inválidas y aplicará las mismas reglas de validación y conflicto que la creación de una reserva. El formato de fecha y hora y la zona horaria se especifican como decisiones de diseño en la sección 6.

**Casos de prueba asociados**

- **CP-01:** consultar un equipo conocido en un intervalo válido sin conflictos; informar que está disponible.
- **CP-02:** consultar un intervalo que se superpone con una reserva activa del mismo equipo; informar que no está disponible.
- **CP-03:** consultar un intervalo que comienza exactamente cuando termina una reserva activa; informar que está disponible.
- **CP-04:** consultar un intervalo inválido, una fecha imposible, una hora inválida, una hora local inexistente o ambigua, o un equipo desconocido; rechazar la consulta con un mensaje claro y sin corregir ni desplazar la hora automáticamente.
- **CP-05:** comprobar que una reserva cancelada no impide informar disponibilidad.

### RF-02 — Crear una reserva

El usuario podrá crear una reserva indicando el identificador del equipo, el nombre del solicitante, la fecha y hora de inicio y la fecha y hora de fin. Si los datos son válidos y no existe conflicto, el sistema guardará la reserva activa y proporcionará su ID único.

**Casos de prueba asociados**

- **CP-06:** crear una reserva válida y comprobar que queda registrada como activa y se informa un ID.
- **CP-07:** intentar reservar un equipo desconocido; rechazar la operación.
- **CP-08:** intentar reservar con el solicitante vacío o compuesto solo por espacios; rechazar la operación.
- **CP-09:** intentar reservar con un formato distinto de `AAAA-MM-DD HH:MM` (por ejemplo, sin minutos o con segundos), una fecha imposible, una hora inválida o un intervalo inválido; rechazar la operación.
- **CP-09a:** intentar reservar con una hora local inexistente o ambigua por cambios en las reglas horarias; rechazar la operación con un mensaje claro y sin corregir ni desplazar la hora automáticamente.
- **CP-10:** intentar crear una reserva superpuesta con otra activa del mismo equipo; rechazar la operación.
- **CP-11:** crear reservas consecutivas para el mismo equipo; aceptar ambas.
- **CP-12:** crear reservas simultáneas para equipos diferentes; aceptar ambas.

### RF-03 — Cancelar una reserva

El usuario podrá cancelar una reserva mediante su ID. La cancelación conservará el registro y cambiará su estado para que deje de bloquear el intervalo. Un ID inexistente o una reserva ya cancelada no modificará el historial y se informará el motivo.

**Casos de prueba asociados**

- **CP-13:** cancelar una reserva activa; comprobar que se conserva el registro con estado cancelado.
- **CP-14:** después de cancelar, consultar o reservar el mismo intervalo y comprobar que ya no está bloqueado por esa reserva.
- **CP-15:** intentar cancelar un ID inexistente; informar el motivo sin alterar los registros.
- **CP-16:** intentar cancelar una reserva ya cancelada; informar el motivo y conservar su estado e historial sin cambios.

### RF-04 — Operar mediante menú interactivo

La aplicación ofrecerá un menú CLI para consultar los equipos del inventario, consultar disponibilidad, crear una reserva, cancelar mediante ID y salir.
**Casos de prueba asociados**

- **CP-17:** recorrer cada opción disponible del menú y comprobar que invoca la operación correspondiente.
- **CP-18:** introducir una opción no válida; informar el error sin crear, cancelar ni alterar reservas.
- **CP-19:** seleccionar salir y comprobar que la aplicación finaliza normalmente.

## 4. Reglas de negocio

### RN-01 — Equipos válidos

Antes de comparar, el identificador se normaliza: se eliminan los espacios exteriores y se convierte a mayúsculas (por ejemplo, `mic-01` equivale a `MIC-01`). Esta normalización es una decisión de implementación, no un requisito del desafío original.

**Caso asociado:** CP-07; para la consulta, CP-04.

### RN-02 — Solicitante no vacío

Se eliminarán los espacios al principio y al final del nombre. Se rechazará el valor si queda vacío.

**Caso asociado:** CP-08.

### RN-03 — Formato y zona horaria

**Decisión de diseño acordada:** la entrada de fecha y hora tendrá el formato `AAAA-MM-DD HH:MM`, con reloj de 24 horas, incluyendo minutos y sin segundos. Por ejemplo: `2026-10-26 14:30`. Representará la hora local utilizada en Corrientes, Argentina, mediante la zona IANA `America/Argentina/Cordoba`.

**Casos asociados:** CP-04, CP-09, CP-09a y CP-17.

### RN-04 — Intervalo válido

El inicio debe ser anterior al fin. Se rechazarán fechas u horas inválidas y los intervalos cuyo inicio sea igual o posterior al fin.

**Casos asociados:** CP-04, CP-09 y CP-09a.

### RN-05 — Horas locales inexistentes o ambiguas

**Decisión de diseño acordada:** si una fecha y hora local resulta inexistente o ambigua debido a cambios en las reglas horarias de la zona, se rechazará con un mensaje claro. La aplicación nunca la corregirá ni la desplazará automáticamente. Esta regla se aplica tanto a la creación de reservas como a la consulta de disponibilidad.

**Casos asociados:** CP-04 y CP-09a.

### RN-06 — Reservas pasadas

**Decisión de diseño acordada:** se permiten reservas pasadas; no se rechazarán únicamente por ser anteriores a la fecha actual.

**Caso asociado:** CP-06, usando un intervalo pasado válido.

### RN-07 — Intervalos semiabiertos y conflictos

Los intervalos se interpretarán como `[inicio, fin)`. Dos reservas activas del mismo equipo entran en conflicto cuando se superponen; una reserva que comienza exactamente al terminar otra no entra en conflicto. Equipos distintos no entran en conflicto por coincidir en el tiempo. La interpretación semiabierta es una decisión de diseño acordada para permitir reservas consecutivas.

**Casos asociados:** CP-02, CP-03, CP-10, CP-11 y CP-12.

### RN-08 — Efecto de la cancelación

Las reservas canceladas no bloquearán la disponibilidad ni impedirán crear otra reserva para el intervalo que ocupaban.

**Casos asociados:** CP-05 y CP-14.

### RN-09 — Cancelación no destructiva

Cancelar cambiará el estado de la reserva, pero no eliminará su registro. **Decisión de diseño acordada:** los intentos de cancelar un ID inexistente o ya cancelado no alterarán los datos e informarán el motivo.

**Casos asociados:** CP-13, CP-15 y CP-16.

## 5. Requisitos de persistencia

### RP-01 — Almacenamiento local

La aplicación utilizará SQLite en `data/reservas.db`. La ruta se resolverá respecto de una ubicación fija de la aplicación, no del directorio actual desde el que se ejecute la CLI.

**Caso de prueba:** iniciar la aplicación desde distintos directorios y comprobar que ambas ejecuciones usan la misma base de datos.

### RP-02 — Persistencia de estados e historial

Las reservas activas y canceladas se conservarán al cerrar y volver a iniciar la aplicación. No habrá borrado automático del historial.

**Casos de prueba asociados**

- **CP-20:** crear una reserva, cerrar y volver a iniciar la aplicación; comprobar que continúa registrada y activa.
- **CP-21:** cancelar una reserva, cerrar y volver a iniciar; comprobar que continúa registrada y cancelada.

## 6. Requisitos originales y decisiones de diseño acordadas

Los requisitos funcionales de la sección 3 y las reglas de negocio sobre equipos válidos, entradas e intervalos válidos, conflictos, cancelación y persistencia se derivan del desafío original. Las siguientes decisiones completan aspectos no especificados allí; no deben interpretarse como requisitos originales:

- Python, CLI con menú interactivo y SQLite.
- Separación mínima entre interfaz, lógica de negocio y persistencia.
- Formato de entrada `AAAA-MM-DD HH:MM`, con reloj de 24 horas, minutos y sin segundos; hora local utilizada en Corrientes, Argentina, mediante `America/Argentina/Cordoba`.
- Rechazar con un mensaje claro horas locales inexistentes o ambiguas y nunca corregirlas o desplazarlas automáticamente.
- Se permiten reservas pasadas.
- Se recortan espacios exteriores del solicitante y se rechaza el nombre vacío resultante.
- Se usa un ID único para cancelar; ID inexistente o ya cancelado produce un mensaje y no modifica los datos.
- La base se guarda en `data/reservas.db`, en una ruta estable relativa a la ubicación de la aplicación.
- Se conservan reservas activas y canceladas sin borrado automático.
- No se impondrá una duración máxima porque el desafío no la establece.
- No se impondrá un límite de anticipación porque el desafío no lo establece.
- El menú incluye la consulta de los equipos del inventario precargado.
- El identificador de equipo se normaliza (espacios exteriores y mayúsculas) antes de validarlo.

No quedan decisiones pendientes identificadas para la especificación actual.