# Trazabilidad del desarrollo del sistema de reservas

## 1. Preparación del agente

### 1.1. Entorno y agente utilizado

Para el desarrollo del sistema de reservas se utilizó **GitHub Copilot en modo Agent, integrado en Visual Studio Code**, como agente de programación asistida por inteligencia artificial.

La información recuperada del entorno de trabajo es la siguiente:

| Elemento | Información |
|---|---|
| Editor | Visual Studio Code 1.143.1 |
| Lenguaje de programación | Python 3.14 |
| Agente | GitHub Copilot en modo Agent |
| Modelo informado | `gpt-6-luna` |
| Herramientas y permisos | Lectura y modificación de archivos, y ejecución de pruebas |
| Revisión humana | Revisión de diferencias (*diff*), aprobación de cambios y ejecución de pruebas |

La versión de la extensión de GitHub Copilot todavía está pendiente de recopilación. Asimismo, el identificador del modelo se registra tal como fue recuperado y queda pendiente de contrastar con la información mostrada por la herramienta. Las versiones del entorno se documentan según los datos disponibles, sin asumir que se ha conservado una evidencia independiente de cada una.

### 1.2. Función y contexto proporcionado

El agente se empleó como asistente de programación para desarrollar una aplicación local de reservas de equipamiento de laboratorio. El objetivo del proceso no se limitó a obtener código funcional, sino que también contempló documentar la delegación de tareas, la verificación de resultados y las decisiones tomadas durante el desarrollo.

Como contexto inicial, se informó al agente que se trataba de un desafío académico y que se utilizaría GitHub Copilot en modo Agent para asistir en la implementación y registrar el proceso de trabajo.

El primer prompt recuperado estableció que, antes de escribir código o modificar archivos, el agente debía analizar los requisitos y proponer un plan de implementación por etapas. La solicitud incluyó el equipamiento inicial, los requisitos funcionales, las reglas de negocio, las pruebas obligatorias y las restricciones del sistema.

En particular, se le solicitó:

- Proponer una arquitectura mínima y una tecnología adecuada.
- Identificar las decisiones técnicas que requerían una definición explícita.
- Dividir la implementación en tareas pequeñas y verificables.
- Relacionar cada requisito con pruebas que permitieran comprobar su cumplimiento.
- Identificar las decisiones que debían ser revisadas y aprobadas por una persona.

También se indicó expresamente que no debía escribir código ni modificar archivos durante esa primera etapa, que no debía inventar requisitos y que debía diferenciar entre requisitos proporcionados, recomendaciones y decisiones pendientes.

Los prompts originales están disponibles en el historial de GitHub Copilot. Su recopilación y vinculación con los episodios de delegación constituyen una tarea pendiente para completar la trazabilidad del proceso.

### 1.3. Herramientas y supervisión humana

Según la información recuperada, el agente contó con capacidades para leer y modificar archivos del proyecto y ejecutar pruebas. La revisión humana se contempló mediante la inspección de los cambios propuestos, su aprobación y la ejecución de pruebas para verificar el comportamiento de la aplicación.

Estos mecanismos se consideran parte del proceso de control del desarrollo asistido. Sin embargo, la descripción de los mecanismos de supervisión no implica, por sí sola, que todos los cambios hayan sido revisados ni que todas las pruebas hayan resultado satisfactorias. La aceptación de resultados específicos debe justificarse mediante los episodios de delegación, los cambios versionados y las evidencias de prueba correspondientes.

### 1.4. Evidencias pendientes

Para completar el registro de la preparación del agente, quedan pendientes las siguientes tareas:

- Recuperar la versión instalada de la extensión de GitHub Copilot.
- Contrastar el identificador del modelo con el dato que muestra la herramienta, si está disponible.
- Recopilar los prompts originales en orden cronológico y relacionarlos con las tareas delegadas.
- Identificar las instrucciones persistentes o configuraciones específicas del agente que efectivamente se utilizaron, si existieron.
- Precisar el contexto disponible para cada intervención relevante.
- Vincular los episodios de delegación con los archivos modificados, los commits, las pruebas y las decisiones de aceptación, corrección o rechazo.
- Documentar ejemplos concretos de revisión humana y, cuando corresponda, de adaptación de las instrucciones o del enfoque de trabajo.

Los elementos pendientes no se completarán mediante suposiciones. Si algún dato no puede recuperarse, se indicará expresamente como no disponible.

## 2. Registro de episodios de delegación

Los resúmenes de instrucciones que siguen describen las intervenciones según la trazabilidad y los archivos disponibles. No son transcripciones literales. El repositorio no contiene enlaces archivados a sesiones o conversaciones.

### D-01 — Análisis de requisitos y planificación

- **Tipo y objetivo:** episodio de delegación de análisis y planificación; proponer una arquitectura mínima y un plan verificable antes de implementar.
- **Contexto y referencias:** se proporcionó la descripción del desafío en la interacción de trabajo. El contenido del PDF original no está disponible aquí.
- **Instrucción disponible:** el registro resume la solicitud como analizar requisitos, recomendar arquitectura y tecnología, identificar decisiones pendientes, proponer etapas y pruebas, y no escribir código. El prompt textual original no está archivado.
- **Acciones y resultado:** la trazabilidad registra que el agente inspeccionó la estructura del repositorio y propuso Python, CLI, SQLite y separación entre interfaz, lógica de negocio y persistencia.
- **Decisión humana:** la persona responsable aceptó esa arquitectura y decidió usar las decisiones acordadas como base para implementar. La decisión está consignada en [docs/trazabilidad.md](./trazabilidad.md); no hay una captura independiente de esa conversación en el repositorio.
- **Evidencia verificable:** la decisión quedó documentada en [docs/trazabilidad.md](./trazabilidad.md). El commit `0f07cf3` introdujo la especificación y el primer registro D-01; `d33f71f` actualizó el registro para consignar la aceptación humana.
- **Estado y límites:** completado como análisis y planificación. No significa que el sistema estuviera implementado ni probado en esa etapa. El prompt original y la inspección inicial no tienen registros independientes disponibles.

### D-02 — Revisión de la especificación de fechas y duración

- **Tipo y objetivo:** episodio de delegación para revisar y corregir la especificación de fecha/hora, zona horaria, transiciones horarias y duración máxima.
- **Contexto y referencias:** la especificación en preparación y las decisiones de diseño comunicadas por la persona responsable.
- **Instrucción disponible:** el registro documenta que se identificó que `AAAA-MM-DD HH` no expresaba minutos, y que se solicitaron correcciones para usar `AAAA-MM-DD HH:MM`, rechazar horas locales inexistentes o ambiguas sin ajustes automáticos y no imponer una duración máxima. No se conserva el prompt original como texto independiente.
- **Acciones y resultado:** [docs/especificacion.md](./especificacion.md) quedó con formato `AAAA-MM-DD HH:MM`, zona `America/Argentina/Cordoba`, rechazo de horas locales inexistentes o ambiguas y sin duración máxima.
- **Decisión humana:** la persona responsable definió y aprobó esas decisiones, según el registro de D-02.
- **Evidencia verificable:** el commit `0f07cf3` (`docs: Refinando las especificaciones del proyecto`) añadió el contenido de la especificación y una primera entrada de trazabilidad. El commit `d33f71f` (`docs: cerrar decisiones iniciales de diseño`) añadió el registro D-02 y consignó el cierre humano de las decisiones. Antes de `0f07cf3`, Git muestra `docs/especificacion.md` como archivo vacío; por ello, la existencia del formato anterior se respalda en el registro del episodio, no en una versión histórica no vacía de la especificación.
- **Estado y límites:** completado según la aprobación registrada. No implica implementación ni pruebas de la aplicación.

### D-03 — Preparación de la estructura inicial

- **Tipo y objetivo:** episodio de delegación para preparar el esqueleto Python, la separación inicial de módulos y una verificación mínima sin implementar las operaciones de reservas.
- **Contexto y referencias:** la arquitectura aprobada en D-01, las decisiones registradas en [docs/especificacion.md](./especificacion.md) y el estado inicial del repositorio.
- **Instrucción disponible:** la trazabilidad resume que se pidió revisar la estructura, crear únicamente el esqueleto y la configuración imprescindible, y no implementar aún las funcionalidades completas. No se conserva una transcripción literal.
- **Acciones y resultado:** se creó [src/reservas/](../src/reservas/) con puntos de entrada y módulos iniciales para CLI, servicio y repositorio, se preparó `data/`, se ajustó `.gitignore` y se añadió una prueba de humo. El commit `fff2336` añadió esos archivos. El commit posterior `b090669` reemplazó la prueba de estructura por pruebas de reservas.
- **Decisión humana:** la persona responsable aprobó el esqueleto y autorizó completar D-03, según la trazabilidad disponible.
- **Evidencia verificable:** `fff2336` contiene los cambios del esqueleto, [data/.gitkeep](../data/.gitkeep), `.gitignore`, el archivo histórico `tests/test_structure.py` y la actualización del registro. Los archivos actuales bajo [src/reservas/](../src/reservas/) reflejan el desarrollo posterior, no solamente el esqueleto original.
- **Estado y límites:** completado como preparación estructural. La prueba de humo histórica ya no existe en el árbol actual; el commit muestra que sí estuvo presente.

### D-04 — Implementación de la lógica central de reservas

- **Tipo y objetivo:** episodio de delegación de implementación y verificación de catálogo, disponibilidad, creación, cancelación, validaciones y persistencia descritos en [docs/especificacion.md](./especificacion.md).
- **Contexto y referencias:** estructura creada en D-03, arquitectura aprobada, especificación vigente y petición de usar bases de prueba aisladas, conservar la historia de cancelaciones y no crear un commit automáticamente.
- **Instrucción disponible:** la trazabilidad resume que se pidió implementar las operaciones definidas, comprobar que consulta y creación compartieran la regla de conflicto, ejecutar pruebas y dejar la aceptación humana a la persona responsable. El prompt literal no se conserva como archivo.
- **Implementación realizada:** se incorporaron modelos de equipo y reserva; validación del formato y de la zona horaria; rechazo de fechas inválidas y horas locales inexistentes o ambiguas; validaciones de equipo, solicitante e intervalo; consulta y creación con regla común de superposición; persistencia SQLite; cancelación no destructiva; y operaciones CLI. La dependencia [requirements.txt](../requirements.txt), que declara `tzdata`, se añadió porque el entorno Windows no encontraba los datos IANA. Estos cambios están incluidos en `b090669`.
- **Errores durante el desarrollo:** la trazabilidad registra que una primera ejecución encontró que el catálogo SQLite no quedaba confirmado y que una fecha de prueba escogida no era ambigua según los datos de zona horaria. También registra la corrección de la transacción y del ejemplo de prueba. Los detalles no están respaldados por logs independientes archivados; el estado final se puede revisar en el código y las pruebas actuales.
- **Pruebas automatizadas:** [tests/test_reservations.py](../tests/test_reservations.py) usa directorios y archivos SQLite temporales. La trazabilidad del episodio registra 17 pruebas aprobadas. En la revisión de este documento se ejecutó de nuevo `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`, con `PYTHONPATH` configurado a `src`: el resultado real fue `Ran 17 tests ... OK`. Esto no repite las verificaciones manuales de la aplicación.
- **Verificaciones manuales reportadas:** la trazabilidad registra que la persona responsable creó reservas de ejemplo para equipos del catálogo, cerró y volvió a iniciar la aplicación y confirmó que la disponibilidad reflejaba la reserva persistida; también reporta pruebas de reserva pasada, equipo desconocido e intervalo inválido. Los datos se describen como ejemplos de prueba, no como datos personales. No se encontró una captura o salida de consola independiente archivada; no se repitieron esas pruebas manuales durante esta revisión.
- **Revisión documental:** tras una revisión adicional se completó el [README.md](../README.md) con instrucciones de entorno, dependencias, ejecución, pruebas, persistencia y límites. El README en `b090669` documenta esos pasos. La versión actual añade además una sección de reinicialización de la base que está modificada localmente y no está incluida en ese commit.
- **Aceptación humana:** el registro actual de D-04 indica que la persona responsable consideró que el trabajo estaba correctamente encaminado y autorizó marcarlo completado. Esa aceptación está registrada en la trazabilidad y en la interacción disponible, no en un artefacto independiente del repositorio.
- **Estado y límites:** completado según la aceptación humana registrada. La suite actual pasó en esta revisión. Las pruebas automatizadas verifican la reapertura del repositorio sobre una base temporal; no lanzan dos procesos CLI independientes. Las verificaciones manuales anteriores se documentan como reportadas, no como repetidas ahora.

## 3. Implementación, verificación y aceptación humana

### Estado observable en el código

La implementación actual permite listar el catálogo, consultar disponibilidad, crear reservas y cancelar por ID mediante el menú CLI. El repositorio usa SQLite en `data/reservas.db` por defecto y la lógica aplica el formato `AAAA-MM-DD HH:MM` y la zona IANA `America/Argentina/Cordoba`. Las funciones existentes, las validaciones y los casos automatizados pueden revisarse en:

- [src/reservas/cli.py](../src/reservas/cli.py)
- [src/reservas/service.py](../src/reservas/service.py)
- [src/reservas/repository.py](../src/reservas/repository.py)
- [src/reservas/models.py](../src/reservas/models.py)
- [tests/test_reservations.py](../tests/test_reservations.py)

El [README.md](../README.md) declara que no hay opción en el menú para consultar el historial completo, administración del catálogo, interfaz gráfica, acceso remoto, autenticación real, pagos, notificaciones ni integraciones externas. Esta lista describe el alcance documentado del proyecto, no requisitos del PDF ausente.

### Ejecución de pruebas registrada en esta revisión

Comando ejecutado desde PowerShell, en la raíz del repositorio:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Resultado observado: **17 pruebas ejecutadas, 17 aprobadas (`OK`)**. La suite usa SQLite temporal; no se inspeccionó ni se usó la base real `data/reservas.db`.

Las verificaciones manuales de persistencia y validaciones que aparecen en D-04 son declaraciones registradas de la persona responsable. No se realizaron nuevamente durante la revisión de trazabilidad.

## 4. Evidencias y trazabilidad en Git

### Commits relacionados

| Episodio / alcance | Commit verificado | Archivos relevantes comprobados |
|---|---|---|
| Estructura inicial vacía | `0ddc4a2` — `inicializar estructura del proyecto` | Añadió `.gitignore`, [README.md](../README.md), [docs/especificacion.md](./especificacion.md) y [docs/trazabilidad.md](./trazabilidad.md) como archivos vacíos. |
| Especificación y primer registro D-01 | `0f07cf3` — `docs: Refinando las especificaciones del proyecto` | Añadió el contenido de [docs/especificacion.md](./especificacion.md) y el primer registro D-01 en [docs/trazabilidad.md](./trazabilidad.md). |
| Cierre de decisiones D-01 y registro D-02 | `d33f71f` — `docs: cerrar decisiones iniciales de diseño` | Actualizó [docs/trazabilidad.md](./trazabilidad.md), incluyendo aceptación de arquitectura y decisiones iniciales. |
| Estructura de D-03 | `fff2336` — `docs: Actualizando trazabilidad del proyecto. src: Redefiniendo estructura del proyecto` | Añadió estructura bajo [src/reservas/](../src/reservas/), [data/.gitkeep](../data/.gitkeep) y el archivo histórico `tests/test_structure.py`; actualizó `.gitignore` y la trazabilidad. |
| Implementación D-04 y README inicial | `b090669` — `Implementación lógica del sistema. Redacción del README.md.` | Añadió modelos, servicio, repositorio, pruebas y [requirements.txt](../requirements.txt); modificó la CLI, [README.md](../README.md) y trazabilidad; eliminó `tests/test_structure.py`. |

Los commits confirman qué archivos cambiaron, no el contenido de prompts, las salidas de cada conversación ni las aprobaciones verbales. Los mensajes e instrucciones originales de Copilot no están guardados como archivos o enlaces en el repositorio.