# Trazabilidad del desarrollo del sistema de reservas

## 1. Registro de episodios de delegación

Los extractos entre comillas son literales. Cuando el prompt completo no se conserva, el episodio lo indica como resumen. No se adjuntan conversaciones completas. El repositorio no contiene enlaces archivados a sesiones o conversaciones.

### D-01. Análisis de requisitos, planificación y definición de decisiones de diseño

**Objetivo y requisito:** analizar los requisitos de la consigna, elaborar un plan de implementación antes de comenzar a escribir código y definir las decisiones de diseño necesarias para orientar el desarrollo. Se buscó distinguir los requisitos obligatorios de las recomendaciones del agente, identificar los aspectos pendientes y establecer verificaciones para las funcionalidades previstas. Requisitos de referencia: las decisiones aprobadas corresponden a RN-02, RN-03, RN-07, RN-09, RP-01 y RP-02 de [docs/especificacion.md](./especificacion.md).

**Contexto suministrado y primer extracto literal del prompt:**

> Antes de escribir código, analizá los requisitos siguientes y proponé un plan de implementación por etapas.

También se solicitó que el agente identificara una arquitectura mínima, las decisiones pendientes, las tareas verificables, las pruebas correspondientes a cada requisito y las decisiones que debían revisarse y aprobarse por una persona. Se indicó expresamente que no debía escribir código, modificar archivos ni afirmar haber ejecutado pruebas durante esa intervención.

**Acción del agente:** inspeccionó el estado del repositorio y leyó `README.md`, `docs/especificacion.md` y `docs/trazabilidad.md`. A partir del análisis, propuso una aplicación local en Python, con interfaz de línea de comandos (CLI), persistencia mediante SQLite y separación de responsabilidades entre la interfaz, la lógica de negocio y la persistencia. También enumeró decisiones de diseño pendientes y elaboró un plan de implementación por etapas con sus respectivas verificaciones.

**Decisión humana: ACEPTAR la propuesta y fijar las decisiones pendientes.** Fundamento verificable: la consigna admite una consola o una API local como interfaz y no exige interfaz gráfica, por lo que una CLI con SQLite local es compatible con el alcance. Segundo extracto literal de la instrucción:

> Acepto la recomendación de utilizar Python, una interfaz de línea de comandos (CLI), SQLite y una arquitectura mínima que separe interfaz, lógica de negocio y persistencia.

Además, se aprobaron los intervalos semiabiertos `[inicio, fin)`, el formato inicial `AAAA-MM-DD HH:MM`, el uso de la hora local de Corrientes, el rechazo de solicitantes vacíos después de eliminar los espacios exteriores, la identificación de las reservas mediante un ID único y la conservación del historial sin borrado automático.

Se solicitó comparar estas decisiones con los requisitos originales, actualizar el plan, señalar los aspectos que aún quedaban pendientes y no modificar archivos ni escribir código durante esa etapa. El agente comparó las decisiones con los requisitos y no identificó contradicciones. Actualizó el plan de trabajo y señaló que todavía era necesario precisar el identificador de la zona horaria, la ubicación de la base de datos y el formato definitivo de la CLI.

Para resolver esos puntos, se proporcionó la siguiente instrucción (extracto literal):

> En base a los aspectos que quedan pendientes:
>
> - Identificador IANA de la zona horaria: Utiliza `/America/Argentina/Cordoba` para representar la hora local de corrientes.
> - Ubicación exacta de `data/reservas.db`: Puedes crear el directorio `data/` con el archivo reservas.db que es donde almacenaremos la base de datos.
> - Formato final de la CLI: Será un menú interactivo de manera que sea más amigable para el usuario final.
>
> No realices modificaciones en archivos, ni crees nuevos archivos aún. Confirmame y actualiza el plan de ejecución primero.

Con esta instrucción quedaron definidas la zona horaria `America/Argentina/Cordoba`, la ubicación de la base de datos en `data/reservas.db` y una interfaz CLI basada en un menú interactivo. También se reiteró que el agente debía actualizar el plan y confirmar las decisiones sin crear ni modificar archivos en esa intervención.

**Resultado y evidencia:** la planificación y las decisiones iniciales de diseño quedaron registradas en la evolución de `docs/especificacion.md` y `docs/trazabilidad.md`. El commit `0f07cf3` (`docs: Refinando las especificaciones del proyecto`) incorporó contenido a la especificación y el primer registro de trazabilidad de la planificación inicial. El commit `d33f71f` (`docs: cerrar decisiones iniciales de diseño`) actualizó la trazabilidad para registrar la aceptación de la arquitectura y las decisiones iniciales.

**Verificación y límites:** este episodio es de análisis y planificación; no implementó funcionalidades, y la respuesta inicial del agente declaró que no escribió código, no modificó archivos ni ejecutó pruebas. Las decisiones aprobadas se pueden contrastar con la versión entregada:

- Formato y zona horaria (RN-03): `TIME_ZONE_NAME` y `DATETIME_FORMAT` en `src/reservas/service.py`.
- Intervalos semiabiertos (RN-07): la consulta `start_at < ? AND end_at > ?` en `src/reservas/repository.py`.
- Solicitante sin espacios exteriores (RN-02): `requester.strip()` en `create_reservation`, `src/reservas/service.py`.
- Base local (RP-01): `data/reservas.db` en `src/reservas/repository.py`.
- Cancelación sin borrado (RN-09, RP-02): el `UPDATE ... SET status = 'cancelled'` en `src/reservas/repository.py`.

### D-02 — Preparación de la estructura inicial

- **Tipo y objetivo:** episodio de delegación orientado a preparar el esqueleto inicial de la aplicación en Python, establecer la separación entre interfaz, lógica de negocio y persistencia, y realizar una verificación mínima sin implementar las operaciones completas de reservas. Requisito de referencia: la decisión de separación mínima entre interfaz, lógica y persistencia ([docs/especificacion.md](./especificacion.md)) y la carpeta `data/` prevista en RP-01.

- **Contexto y referencias:** la arquitectura propuesta en D-01, las decisiones aprobadas y registradas en [docs/especificacion.md](./especificacion.md), y la estructura existente del repositorio.

- **Instrucción proporcionada (extracto literal):**

  > Tomá como referencia `docs/especificacion.md` y prepará la estructura inicial del proyecto.
  >
  > Antes de modificar archivos:
  >
  > 1. Explicá brevemente la arquitectura propuesta.
  > 2. Indicá la responsabilidad de cada módulo.
  > 3. Explicá cómo se separarán la lógica de reservas, la persistencia y la interfaz.
  > 4. Indicá cómo se ejecutarán las pruebas.
  > 5. Revisá la estructura actual del repositorio para evitar duplicar archivos o modificar documentación innecesariamente.
  >
  > Después de presentar el plan, implementá únicamente la estructura inicial, las dependencias necesarias y los archivos de configuración imprescindibles.
  >
  > Respetá las decisiones aprobadas, no implementes todavía todas las funcionalidades, no agregues dependencias sin justificar su necesidad y actualizá `docs/trazabilidad.md` sin inventar acciones, pruebas, commits ni evidencias.

- **Acciones realizadas por el agente:** Copilot revisó la especificación, la trazabilidad, el archivo `.gitignore` y la estructura del repositorio. Preparó el paquete `src/reservas/`, con módulos iniciales para la interfaz de consola (`cli.py`), la lógica de negocio (`service.py`) y la persistencia (`repository.py`), y los archivos `__init__.py` y `__main__.py` del paquete. También agregó `data/.gitkeep`, ajustó las reglas de `.gitignore` y creó `tests/test_structure.py` como prueba de humo. No agregó dependencias externas ni implementó las operaciones completas de reservas.

- **Resultado y verificación técnica:** la CLI quedó como punto de entrada provisional, ejecutable mediante `python -m reservas` con `src` configurado en `PYTHONPATH`. Según lo informado por el agente, `python -m unittest discover -s tests -v` finalizó correctamente con una prueba de humo y la invocación del módulo también se ejecutó. Estas comprobaciones verificaron el esqueleto inicial, no las funcionalidades de reservas.

- **Decisión humana: ACEPTAR.** Revisé: la lista de archivos y el tamaño de los cambios del commit `fff2336` con `git show --stat`. Son 9 archivos (53 inserciones, 2 eliminaciones), los módulos de `src/reservas/` agregan entre 1 y 5 líneas y el commit no incluye `requirements.txt` ni otras dependencias. Motivo: el commit contenía solo la estructura y respetaba el límite de no implementar funcionalidades ni agregar dependencias. Autoricé continuar con la implementación funcional (D-03).

- **Adaptación específica del proceso (plan antes de código, alcance acotado):** se dividió el desarrollo en etapas y se limitó esta intervención a preparar la estructura, dejando la lógica funcional para una delegación posterior. La instrucción exigió presentar el plan antes de modificar archivos ("Antes de modificar archivos: …") e implementar "únicamente la estructura inicial". La respuesta registrada mantuvo el alcance previsto y dejó las operaciones de reservas sin implementar. Evidencia: commit `fff2336` y el extracto de la instrucción de arriba.

- **Evidencias verificables:** el commit `fff2336` (`docs: Actualizando trazabilidad del proyecto. src: Redefiniendo estructura del proyecto`) incorporó el esqueleto inicial, junto con `data/.gitkeep`, las modificaciones de `.gitignore`, `tests/test_structure.py` y la actualización de la trazabilidad. El commit posterior `b090669` (`Implementación lógica del sistema. Redacción del README.md.`) reemplazó la prueba de estructura por pruebas funcionales. Por eso, `tests/test_structure.py` ya no está presente en el árbol actual; su existencia histórica puede comprobarse en `fff2336`. Los archivos actuales de `src/reservas/` incluyen cambios posteriores y no representan exclusivamente el resultado de D-02.

- **Estado y límites:** completado como preparación estructural. La prueba de humo y el punto de entrada se ejecutaron según lo informado por el agente. Autoricé continuar con la implementación funcional (D-03) tras la revisión descrita arriba.

### D-03 — Implementación de la lógica central de reservas

- **Tipo y objetivo:** episodio de delegación para implementar y verificar el catálogo, la disponibilidad, la creación y cancelación de reservas, las validaciones y la persistencia descritas en [docs/especificacion.md](./especificacion.md). Cubre RF-01, RF-02, RF-03, RF-04, RN-01 a RN-09 y RP-02.

- **Contexto y referencias:** estructura creada en D-02, arquitectura aprobada, especificación vigente y requisito de utilizar bases de prueba aisladas, conservar el historial de cancelaciones y no crear commits automáticamente.

- **Instrucciones proporcionadas:** se realizaron dos intervenciones con Copilot. La primera solicitó implementar las operaciones definidas en la especificación, mantener separadas la lógica de negocio, la persistencia SQLite y la interfaz de consola, agregar pruebas automatizadas, ejecutar la suite, corregir los errores encontrados y actualizar la trazabilidad, dejando pendiente la aceptación humana. La segunda solicitó revisar la implementación sin modificar archivos, contrastarla con la especificación, ejecutar nuevamente las pruebas e informar problemas concretos y una recomendación de aprobación. Los prompts completos están disponibles en el historial de la interacción, pero no se conservaron como archivos independientes del repositorio.

 Extractos literales de la primera instrucción (el prompt completo no se adjunta):

  > Respetá la arquitectura existente y mantené separadas:
  >
  > - La lógica de negocio y las reglas de validación.
  > - La persistencia SQLite.
  > - La interfaz de consola.
  > - Usá una base de datos temporal o aislada cuando corresponda.
  > - Revisá que la lógica de disponibilidad y la de creación apliquen las mismas reglas para detectar conflictos.
  > - No marques como completada la verificación humana: dejala pendiente hasta que yo revise los cambios.
  > - No realices un commit automáticamente. Primero quiero revisar el resultado.

- **Implementación realizada:** se incorporaron modelos de equipo y reserva; validación del formato y de la zona horaria; rechazo de fechas inválidas y horas locales inexistentes o ambiguas; validaciones de equipo, solicitante e intervalo; consulta y creación con una regla común de superposición; persistencia SQLite; cancelación no destructiva y operaciones mediante la CLI. La dependencia [requirements.txt](../requirements.txt), que declara `tzdata`, se añadió porque el entorno Windows no encontraba los datos IANA. Estos cambios están incluidos en `b090669`.

- **Errores durante el desarrollo:** durante la primera ejecución de la suite se detectó que el catálogo SQLite no quedaba confirmado y que una fecha seleccionada para probar una hora ambigua no correspondía a una transición ambigua de la zona horaria. Según el registro de la intervención, el agente corrigió la transacción y el ejemplo de prueba. No se conservaron logs independientes de esos fallos; las correcciones y el estado final pueden contrastarse con el código y las pruebas disponibles.

- **Pruebas automatizadas:** [tests/test_reservations.py](../tests/test_reservations.py) utiliza directorios y archivos SQLite temporales. La implementación registró 17 pruebas aprobadas. Durante la revisión posterior se ejecutó nuevamente:

  ```powershell
  $env:PYTHONPATH = (Resolve-Path .\src).Path
  .\.venv\Scripts\python.exe -m unittest discover -s tests -v
  ```

  El resultado observado fue `Ran 17 tests ... OK`. Esa ejecución la realizó el agente.

  Ejecución propia sobre la versión entregada: el 2026-10-26 ejecuté `python -m unittest discover -s tests -v` con Python 3.14.0 sobre el commit `a52681ff16ab0c0c4cb953a33dd97c9567e9e7f0` (en ese momento había cambios sin commitear solo en `README.md` y `docs/trazabilidad.md`; `src/` y `tests/` no tenían modificaciones). Resultado observado: `Ran 17 tests in 1.500s ... OK`. El registro completo está en la sección 2 de este archivo.

- **Verificaciones manuales:** probé la aplicación a mano: intenté reservar un equipo que no figura en el inventario y reservar un equipo en un horario ya ocupado, y el sistema rechazó ambos casos. Usé datos de ejemplo, no datos personales. No se archivó una captura ni la salida de consola de esas pruebas. No ejecuté un procedimiento manual de persistencia con reinicio de la aplicación; esa verificación se cubre con las pruebas automáticas descritas en la sección 2.

- **Revisión posterior (realizada por el agente, no es revisión humana):** Copilot inspeccionó la implementación, las pruebas, las dependencias, el README y la especificación, y volvió a ejecutar la suite sin modificar archivos. Informó que las reglas principales estaban cubiertas y señaló que la prueba de persistencia reabre el repositorio sobre una base temporal, pero no inicia dos procesos CLI independientes. También identificó inicialmente la falta de instrucciones de instalación y ejecución en el README; posteriormente se completó esa documentación.

- **Revisión documental:** el [README.md](../README.md) incluido en `b090669` documenta el entorno, las dependencias, la ejecución, las pruebas, la persistencia y los límites del sistema. 

- **Decisión humana: ACEPTAR sin correcciones humanas.** Ejecuté la suite completa sobre el commit `a52681f` (17 pruebas, `OK`; ver sección 2) y probé la aplicación a mano: intenté reservar un equipo que no figura en el inventario y reservar un equipo en un horario ya ocupado, y el sistema rechazó ambos casos. Motivo: cada regla de la especificación tenía una prueba automática que pasaba y el comportamiento manual coincidió con ese resultado. Autoricé marcar el episodio como completado después de esa revisión. 

- **Evidencias verificables:** commit `b090669`; [tests/test_reservations.py](../tests/test_reservations.py):
  - `test_rejects_overlapping_active_reservation_for_same_equipment` (RN-07)
  - `test_availability_and_creation_share_overlap_rules` (RF-01, RN-07)
  - `test_accepts_consecutive_reservations` (RN-07)
  - `test_accepts_simultaneous_reservations_for_different_equipment` (RN-07)
  - `test_cancellation_releases_interval_and_preserves_history` (RN-08, RN-09)
  - `test_persists_reservations_when_repository_is_reopened` (RP-02)
  - `test_rejects_nonexistent_local_time_for_creation_and_query` y `test_rejects_ambiguous_local_time_for_creation_and_query` (RN-05)
  - `test_cli_routes_equipment_booking_availability_and_cancellation` (RF-04, CP-17)

  También [requirements.txt](../requirements.txt), [README.md](../README.md) y [docs/especificacion.md](./especificacion.md).

- **Estado y límites:** completado según la decisión humana registrada arriba. La suite automatizada pasó en la revisión posterior del agente y en mi ejecución propia. Las pruebas verifican la reapertura del repositorio sobre una base temporal, pero no lanzan dos procesos CLI independientes. No se creó un commit automáticamente durante la implementación.

## 2. Implementación, verificación y aceptación humana

### Estado observable en el código

En la versión actual del repositorio, la aplicación permite listar el catálogo, consultar disponibilidad, crear reservas y cancelar por ID mediante el menú CLI. El repositorio usa SQLite en `data/reservas.db` por defecto y la lógica aplica el formato `AAAA-MM-DD HH:MM` y la zona IANA `America/Argentina/Cordoba`. Las funciones existentes, las validaciones y los casos automatizados pueden revisarse en:

- [src/reservas/cli.py](../src/reservas/cli.py)
- [src/reservas/service.py](../src/reservas/service.py)
- [src/reservas/repository.py](../src/reservas/repository.py)
- [src/reservas/models.py](../src/reservas/models.py)
- [tests/test_reservations.py](../tests/test_reservations.py)

El [README.md](../README.md) declara que no hay opción en el menú para consultar el historial completo, administración del catálogo, interfaz gráfica, acceso remoto, autenticación real, pagos, notificaciones ni integraciones externas. Esta lista describe las funcionalidades incluidas y las limitaciones declaradas del proyecto. Los requisitos de referencia son los establecidos en la consigna del desafío y desarrollados en `docs/especificacion.md`. Las funcionalidades adicionales mencionadas como fuera de alcance no deben interpretarse como requisitos nuevos.

### Ejecución de pruebas

Ejecución propia sobre la versión entregada:

- **Fecha:** 2026-10-26
- **Commit:** `a52681ff16ab0c0c4cb953a33dd97c9567e9e7f0`
- **Estado del árbol:** cambios sin commitear solo en `README.md` y `docs/trazabilidad.md`; `src/` y `tests/` sin modificaciones.
- **Python:** 3.14.0 (Windows, PowerShell, entorno virtual `.venv`)
- **Comando:**

  ```powershell
  $env:PYTHONPATH = (Resolve-Path .\src).Path
  python -m unittest discover -s tests -v
  ```

- **Resultado observado:** `Ran 17 tests in 1.500s` — `OK` (17 aprobadas, 0 fallos, 0 errores).

La ejecución previa del agente, durante su revisión de D-03, usó el mismo comando y dio el mismo resultado (`Ran 17 tests ... OK`).

La suite usa SQLite temporal y no usa la base real `data/reservas.db`. La persistencia de reservas activas y canceladas se verifica con `test_persists_reservations_when_repository_is_reopened` y `test_cancellation_releases_interval_and_preserves_history`, que reabren el repositorio sobre el mismo archivo. Esas pruebas no lanzan dos procesos CLI independientes.

## 3. Evidencias y trazabilidad en Git

### Commits relacionados

La siguiente tabla relaciona los episodios de delegación documentados con los commits que permiten revisar la evolución del repositorio.

| Episodio / alcance | Commit verificado | Archivos relevantes comprobados |
|---|---|---|
| Estructura inicial vacía del repositorio | `0ddc4a2` — `inicializar estructura del proyecto` | Añadió `.gitignore`, `README.md`, `docs/especificacion.md` y `docs/trazabilidad.md` como archivos iniciales vacíos. |
| **D-01. Análisis de requisitos, planificación y definición de decisiones de diseño** | `0f07cf3` — `docs: Refinando las especificaciones del proyecto` | Incorporó contenido a `docs/especificacion.md` y el primer registro de trazabilidad correspondiente a la planificación inicial. |
| **D-01. Análisis de requisitos, planificación y definición de decisiones de diseño** | `d33f71f` — `docs: cerrar decisiones iniciales de diseño` | Actualizó `docs/trazabilidad.md` para registrar la aceptación de la arquitectura y las decisiones iniciales de diseño. Este commit complementa la evidencia del episodio D-01. |
| **D-02. Preparación de la estructura inicial** | `fff2336` — `docs: Actualizando trazabilidad del proyecto. src: Redefiniendo estructura del proyecto` | Añadió la estructura de módulos bajo `src/reservas/`, el archivo `data/.gitkeep` y el archivo histórico `tests/test_structure.py`. También actualizó `.gitignore` y el registro de trazabilidad. |
| **D-03. Implementación y verificación del sistema** | `b090669` — `Implementación lógica del sistema. Redacción del README.md.` | Incorporó los modelos, el servicio, el repositorio y las pruebas automatizadas; modificó la CLI, `README.md` y la trazabilidad, añadió `requirements.txt` y eliminó `tests/test_structure.py`. |

Los commits permiten verificar los cambios incorporados al repositorio y su secuencia temporal. Sin embargo, no demuestran por sí solos el contenido completo de las conversaciones con el agente, las respuestas generadas ni las aprobaciones expresadas durante las interacciones. Los extractos de instrucciones y las decisiones humanas se documentan en los episodios correspondientes de este archivo; no debe interpretarse que todos los prompts originales están archivados de forma independiente.

Las verificaciones manuales y los resultados de las pruebas automáticas se registran en las secciones 2 y D-03 de este archivo.