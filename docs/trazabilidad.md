# Trazabilidad del desarrollo del sistema de reservas

## 1. Registro de episodios de delegación

Los resúmenes de instrucciones que siguen describen las intervenciones según la trazabilidad y los archivos disponibles. No son transcripciones literales. El repositorio no contiene enlaces archivados a sesiones o conversaciones.

### D-01. Análisis de requisitos, planificación y definición de decisiones de diseño

**Objetivo:** analizar los requisitos de la consigna, elaborar un plan de implementación antes de comenzar a escribir código y definir las decisiones de diseño necesarias para orientar el desarrollo. Se buscó distinguir los requisitos obligatorios de las recomendaciones del agente, identificar los aspectos pendientes y establecer verificaciones para las funcionalidades previstas.

**Primer extracto real del prompt:**

> Antes de escribir código, analizá los requisitos siguientes y proponé un plan de implementación por etapas.

También se solicitó que el agente identificara una arquitectura mínima, las decisiones pendientes, las tareas verificables, las pruebas correspondientes a cada requisito y las decisiones que debían revisarse y aprobarse por una persona. Se indicó expresamente que no debía escribir código, modificar archivos ni afirmar haber ejecutado pruebas durante esa intervención.

**Acción del agente:** inspeccionó el estado del repositorio y leyó `README.md`, `docs/especificacion.md` y `docs/trazabilidad.md`. A partir del análisis, propuso una aplicación local en Python, con interfaz de línea de comandos (CLI), persistencia mediante SQLite y separación de responsabilidades entre la interfaz, la lógica de negocio y la persistencia. También enumeró decisiones de diseño pendientes y elaboró un plan de implementación por etapas con sus respectivas verificaciones.

**Decisión humana y segundo extracto literal de la instrucción:**

La propuesta se utilizó como base para definir la arquitectura inicial. En una interacción posterior, se aceptó explícitamente la recomendación de utilizar Python, una CLI, SQLite y una arquitectura mínima con separación de responsabilidades. La instrucción fue:

> Acepto la recomendación de utilizar Python, una interfaz de línea de comandos (CLI), SQLite y una arquitectura mínima que separe interfaz, lógica de negocio y persistencia.

Además, se aprobaron los intervalos semiabiertos `[inicio, fin)`, el formato inicial `AAAA-MM-DD HH:MM`, el uso de la hora local de Corrientes, el rechazo de solicitantes vacíos después de eliminar los espacios exteriores, la identificación de las reservas mediante un ID único y la conservación del historial sin borrado automático.

Se solicitó comparar estas decisiones con los requisitos originales, actualizar el plan, señalar los aspectos que aún quedaban pendientes y no modificar archivos ni escribir código durante esa etapa.

El agente comparó las decisiones con los requisitos y no identificó contradicciones. Actualizó el plan de trabajo y señaló que todavía era necesario precisar el identificador de la zona horaria, la ubicación de la base de datos y el formato definitivo de la CLI.

Para resolver esos puntos, se proporcionó la siguiente instrucción:

> En base a los aspectos que quedan pendientes:
>
> - Identificador IANA de la zona horaria: Utiliza `/America/Argentina/Cordoba` para representar la hora local de corrientes.
> - Ubicación exacta de `data/reservas.db`: Puedes crear el directorio `data/` con el archivo reservas.db que es donde almacenaremos la base de datos.
> - Formato final de la CLI: Será un menú interactivo de manera que sea más amigable para el usuario final.
>
> No realices modificaciones en archivos, ni crees nuevos archivos aún. Confirmame y actualiza el plan de ejecución primero.

Con esta instrucción quedaron definidas la zona horaria `America/Argentina/Cordoba`, la ubicación de la base de datos en `data/reservas.db` y una interfaz CLI basada en un menú interactivo. También se reiteró que el agente debía actualizar el plan y confirmar las decisiones sin crear ni modificar archivos en esa intervención.

**Resultado y evidencia:** la planificación y las decisiones iniciales de diseño se reflejaron en la evolución de `docs/especificacion.md` y `docs/trazabilidad.md`. Los commits `0f07cf3` y `d33f71f` permiten consultar la evolución documental relacionada con esta etapa. La implementación posterior permite contrastar las decisiones aprobadas con el código del proyecto.

**Verificación y límites:** las intervenciones incluidas en este episodio corresponden al análisis, la planificación y la definición de criterios, no a la implementación de las funcionalidades. Las instrucciones documentadas permiten identificar los requerimientos planteados y las decisiones humanas expresadas, pero no demuestran por sí solas que el agente haya actualizado correctamente el plan ni que las decisiones se hayan implementado. Para verificar esos resultados es necesario contrastar las respuestas del agente con los documentos versionados y el código del proyecto. La respuesta inicial también declaró que no se había escrito código, modificado archivos ni ejecutado pruebas durante esa intervención.

### D-02 — Preparación de la estructura inicial

- **Tipo y objetivo:** episodio de delegación orientado a preparar el esqueleto inicial de la aplicación en Python, establecer la separación entre interfaz, lógica de negocio y persistencia, y realizar una verificación mínima sin implementar las operaciones completas de reservas.

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

- **Acciones realizadas por el agente:** Copilot revisó la especificación, la trazabilidad, el archivo `.gitignore` y la estructura del repositorio. Preparó el paquete `src/reservas/`, con módulos iniciales para la interfaz de consola (`cli.py`), la lógica de negocio (`service.py`) y la persistencia (`repository.py`). También creó los puntos de entrada del paquete, agregó `data/.gitkeep`, ajustó las reglas de `.gitignore` y creó `tests/test_structure.py` como prueba de humo. No agregó dependencias externas ni implementó las operaciones completas de reservas.

- **Resultado y verificación técnica:** la CLI quedó como punto de entrada provisional, ejecutable mediante `python -m reservas` con `src` configurado en `PYTHONPATH`. Según el registro de ejecución, `python -m unittest discover -s tests -v` finalizó correctamente con una prueba de humo y la invocación del módulo también se ejecutó. Estas comprobaciones verificaron el esqueleto inicial, no las funcionalidades de reservas.

- **Decisión y supervisión humana:** la trazabilidad disponible registra la aprobación del esqueleto y la continuación hacia la implementación funcional. Sin embargo, la revisión humana final de los cambios de esta intervención debe distinguirse de las pruebas ejecutadas por el agente. No se atribuye a este episodio una revisión adicional que no esté documentada.

- **Adaptación del proceso:** se dividió el desarrollo en etapas y se limitó esta intervención a preparar la estructura, dejando la lógica funcional para una delegación posterior. La instrucción estableció expresamente ese límite y exigió informar las verificaciones sin inventar resultados. La respuesta registrada mantuvo el alcance previsto y dejó las operaciones de reservas sin implementar.

- **Evidencias verificables:** el commit `fff2336` (`docs: Actualizando trazabilidad del proyecto. src: Redefiniendo estructura del proyecto`) incorporó el esqueleto inicial, junto con `data/.gitkeep`, las modificaciones de `.gitignore`, `tests/test_structure.py` y la actualización de la trazabilidad. El commit posterior `b090669` (`Implementación lógica del sistema. Redacción del README.md.`) reemplazó la prueba de estructura por pruebas funcionales. Por eso, `tests/test_structure.py` ya no está presente en el árbol actual; su existencia histórica puede comprobarse en `fff2336`. Los archivos actuales de `src/reservas/` incluyen cambios posteriores y no representan exclusivamente el resultado de D-02.

- **Estado y límites:** completado como preparación estructural. La prueba de humo y el punto de entrada se ejecutaron según el registro disponible. La persona responsable autorizó continuar con la implementación funcional. Esta decisión no implica que se haya realizado una revisión técnica independiente adicional de todos los cambios de D-02.

### D-03 — Implementación de la lógica central de reservas

- **Tipo y objetivo:** episodio de delegación para implementar y verificar el catálogo, la disponibilidad, la creación y cancelación de reservas, las validaciones y la persistencia descritas en [docs/especificacion.md](./especificacion.md).

- **Contexto y referencias:** estructura creada en D-02, arquitectura aprobada, especificación vigente y requisito de utilizar bases de prueba aisladas, conservar el historial de cancelaciones y no crear commits automáticamente.

- **Instrucciones proporcionadas:** se realizaron dos intervenciones con Copilot. La primera solicitó implementar las operaciones definidas en la especificación, mantener separadas la lógica de negocio, la persistencia SQLite y la interfaz de consola, agregar pruebas automatizadas, ejecutar la suite, corregir los errores encontrados y actualizar la trazabilidad, dejando pendiente la aceptación humana. La segunda solicitó revisar la implementación sin modificar archivos, contrastarla con la especificación, ejecutar nuevamente las pruebas e informar problemas concretos y una recomendación de aprobación. Los prompts completos están disponibles en el historial de la interacción, pero no se conservaron como archivos independientes del repositorio.

- **Implementación realizada:** se incorporaron modelos de equipo y reserva; validación del formato y de la zona horaria; rechazo de fechas inválidas y horas locales inexistentes o ambiguas; validaciones de equipo, solicitante e intervalo; consulta y creación con una regla común de superposición; persistencia SQLite; cancelación no destructiva y operaciones mediante la CLI. La dependencia [requirements.txt](../requirements.txt), que declara `tzdata`, se añadió porque el entorno Windows no encontraba los datos IANA. Estos cambios están incluidos en `b090669`.

- **Errores durante el desarrollo:** durante la primera ejecución de la suite se detectó que el catálogo SQLite no quedaba confirmado y que una fecha seleccionada para probar una hora ambigua no correspondía a una transición ambigua de la zona horaria. Según el registro de la intervención, se corrigieron la transacción y el ejemplo de prueba. No se conservaron logs independientes de esos fallos; las correcciones y el estado final pueden contrastarse con el código y las pruebas disponibles.

- **Pruebas automatizadas:** [tests/test_reservations.py](../tests/test_reservations.py) utiliza directorios y archivos SQLite temporales. La implementación registró 17 pruebas aprobadas. Durante la revisión posterior se ejecutó nuevamente:

  ```powershell
  $env:PYTHONPATH = (Resolve-Path .\src).Path
  .\.venv\Scripts\python.exe -m unittest discover -s tests -v
  ```

  El resultado observado fue `Ran 17 tests ... OK`. Esta ejecución verificó la suite automatizada, pero no repitió las verificaciones manuales realizadas anteriormente.

- **Verificaciones manuales reportadas:** la trazabilidad registra que la persona responsable creó reservas de ejemplo para equipos del catálogo, cerró y volvió a iniciar la aplicación y comprobó que la disponibilidad reflejaba la reserva persistida. También reporta pruebas de reservas pasadas, equipos desconocidos e intervalos inválidos. Los datos se describen como ejemplos de prueba, no como datos personales. No se encontró una captura o salida de consola independiente archivada y estas verificaciones no se repitieron durante la revisión posterior.

- **Revisión posterior:** Copilot inspeccionó la implementación, las pruebas, las dependencias, el README y la especificación, y volvió a ejecutar la suite sin modificar archivos. Informó que las reglas principales estaban cubiertas y señaló que la prueba de persistencia reabre el repositorio sobre una base temporal, pero no inicia dos procesos CLI independientes. También identificó inicialmente la falta de instrucciones de instalación y ejecución en el README; posteriormente se completó esa documentación.

- **Revisión documental:** el [README.md](../README.md) incluido en `b090669` documenta el entorno, las dependencias, la ejecución, las pruebas, la persistencia y los límites del sistema. La versión actual del README, publicada en la rama `main`, incorpora además una sección de reinicialización de la base de datos. La incorporación de esta sección y su relación con los cambios posteriores deben determinarse a partir del historial de Git.

- **Aceptación humana:** la trazabilidad registra que la persona responsable consideró que el trabajo estaba correctamente encaminado y autorizó marcarlo como completado. Esta aceptación se documenta en la trazabilidad y en la interacción disponible, no en un artefacto independiente del repositorio.

- **Evidencias verificables:** `src/reservas/`, [tests/test_reservations.py](../tests/test_reservations.py), [requirements.txt](../requirements.txt), [README.md](../README.md), [docs/especificacion.md](./especificacion.md), los resultados registrados de las ejecuciones de pruebas y el commit `b090669`. El commit permite verificar los cambios incluidos en esa versión. El README publicado permite consultar la documentación actual; las verificaciones manuales que no cuentan con registros independientes deben evaluarse por separado.

- **Estado y límites:** completado según la aceptación humana registrada. La suite automatizada pasó en la revisión posterior. Las pruebas verifican la reapertura del repositorio sobre una base temporal, pero no lanzan dos procesos CLI independientes. Las comprobaciones manuales anteriores se documentan como reportadas, no como repetidas durante la revisión. No se creó un commit automáticamente.

## 2. Implementación, verificación y aceptación humana

### Estado observable en el código

En la versión actual del repositorio, la aplicación permite listar el catálogo, consultar disponibilidad, crear reservas y cancelar por ID mediante el menú CLI. El repositorio usa SQLite en `data/reservas.db` por defecto y la lógica aplica el formato `AAAA-MM-DD HH:MM` y la zona IANA `America/Argentina/Cordoba`. Las funciones existentes, las validaciones y los casos automatizados pueden revisarse en:

- [src/reservas/cli.py](../src/reservas/cli.py)
- [src/reservas/service.py](../src/reservas/service.py)
- [src/reservas/repository.py](../src/reservas/repository.py)
- [src/reservas/models.py](../src/reservas/models.py)
- [tests/test_reservations.py](../tests/test_reservations.py)

El [README.md](../README.md) declara que no hay opción en el menú para consultar el historial completo, administración del catálogo, interfaz gráfica, acceso remoto, autenticación real, pagos, notificaciones ni integraciones externas. Esta lista describe las funcionalidades incluidas y las limitaciones declaradas del proyecto. Los requisitos de referencia son los establecidos en la consigna del desafío y desarrollados en `docs/especificacion.md`. Las funcionalidades adicionales mencionadas como fuera de alcance no deben interpretarse como requisitos nuevos.

### Ejecución de pruebas registrada en esta revisión

Comando ejecutado desde PowerShell, en la raíz del repositorio:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Resultado observado: **17 pruebas ejecutadas, 17 aprobadas (`OK`)**. La suite usa SQLite temporal; no se inspeccionó ni se usó la base real `data/reservas.db`.

Las verificaciones manuales de persistencia y validaciones que aparecen en D-03 son declaraciones registradas de la persona responsable. No se realizaron nuevamente durante la revisión de trazabilidad.

## 3. Evidencias y trazabilidad en Git

### Commits relacionados

La siguiente tabla relaciona los episodios de delegación documentados con los commits que permiten revisar la evolución del repositorio. Los episodios D-01 y D-02 originales se unificaron en el nuevo D-01, ya que corresponden a etapas consecutivas de análisis, planificación y definición de decisiones de diseño.

| Episodio / alcance | Commit verificado | Archivos relevantes comprobados |
|---|---|---|
| Estructura inicial vacía del repositorio | `0ddc4a2` — `inicializar estructura del proyecto` | Añadió `.gitignore`, `README.md`, `docs/especificacion.md` y `docs/trazabilidad.md` como archivos iniciales vacíos. |
| **D-01. Análisis de requisitos, planificación y definición de decisiones de diseño** | `0f07cf3` — `docs: Refinando las especificaciones del proyecto` | Incorporó contenido a `docs/especificacion.md` y el primer registro de trazabilidad correspondiente a la planificación inicial. |
| **D-01. Análisis de requisitos, planificación y definición de decisiones de diseño** | `d33f71f` — `docs: cerrar decisiones iniciales de diseño` | Actualizó `docs/trazabilidad.md` para registrar la aceptación de la arquitectura y las decisiones iniciales de diseño. Este commit complementa la evidencia del episodio D-01. |
| **D-02. Preparación de la estructura inicial** | `fff2336` — `docs: Actualizando trazabilidad del proyecto. src: Redefiniendo estructura del proyecto` | Añadió la estructura de módulos bajo `src/reservas/`, el archivo `data/.gitkeep` y el archivo histórico `tests/test_structure.py`. También actualizó `.gitignore` y el registro de trazabilidad. |
| **D-03. Implementación y verificación del sistema** | `b090669` — `Implementación lógica del sistema. Redacción del README.md.` | Incorporó los modelos, el servicio, el repositorio y las pruebas automatizadas; modificó la CLI, `README.md` y la trazabilidad, añadió `requirements.txt` y eliminó `tests/test_structure.py`. |

Los commits permiten verificar los cambios incorporados al repositorio y su secuencia temporal. Sin embargo, no demuestran por sí solos el contenido completo de las conversaciones con el agente, las respuestas generadas ni las aprobaciones expresadas durante las interacciones. Los extractos de instrucciones y las decisiones humanas se documentan en los episodios correspondientes de este archivo; no debe interpretarse que todos los prompts originales están archivados de forma independiente.

La verificación de la implementación y de las pruebas automatizadas se detalla en el episodio D-03. Las verificaciones manuales de persistencia y validaciones se identifican como realizadas por la persona responsable, sin atribuirles una ejecución independiente durante la revisión documental.