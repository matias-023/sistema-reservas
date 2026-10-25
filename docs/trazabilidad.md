## D-01 — Análisis de requisitos y planificación

**Objetivo:** analizar los requisitos del desafío y definir una arquitectura mínima antes de comenzar la implementación.

**Herramienta:** GitHub Copilot en modo Agent, integrado en Visual Studio Code.

**Instrucción proporcionada:** prompt inicial de análisis de requisitos, arquitectura, decisiones pendientes y plan de pruebas.

**Acciones observadas:** el agente inspeccionó los archivos del repositorio, consultó el estado de Git y enumeró los archivos existentes. Después presentó un resumen de los requisitos, una propuesta de arquitectura y un plan de implementación por etapas.

**Resultado:** recomendó Python, una interfaz CLI, SQLite y la separación entre interfaz, lógica de negocio y persistencia. También identificó decisiones pendientes sobre fechas, zona horaria, cancelaciones e identificación de reservas.

**Verificación humana:** el solicitante revisó y aceptó la arquitectura propuesta: Python, interfaz CLI, SQLite y separación entre interfaz, lógica de negocio y persistencia. Las decisiones de diseño documentadas se utilizarán como base para la implementación.

**Decisión humana:** arquitectura aceptada; se usarán las decisiones de diseño acordadas como base de implementación.

**Evidencias:** prompt inicial y respuesta de Copilot conservados en la conversación. Repositorio inicial con commit previo a la implementación.

**Estado:** Completado. Este cierre registra el análisis y la aceptación de la propuesta; no implica que la aplicación se haya implementado o probado.

## D-02 — Revisión de la especificación de fechas y duración

**Objetivo:** corregir y completar la especificación funcional tras revisar el formato de fecha y hora y las reglas relacionadas con la zona horaria.

**Problema detectado durante la revisión:** en [docs/especificacion.md](./especificacion.md), el formato `AAAA-MM-DD HH` no contemplaba los minutos. Además, debía quedar explícito el tratamiento de horas locales inexistentes o ambiguas y la decisión sobre la duración máxima.

**Decisiones de diseño adoptadas y justificación:**

- Se reemplazó el formato por `AAAA-MM-DD HH:MM`, con reloj de 24 horas, minutos y sin segundos, para poder expresar minutos sin admitir precisión de segundos.
- Se mantuvo la zona IANA `America/Argentina/Cordoba`, que representa la hora local utilizada en Corrientes.
- Las horas locales inexistentes o ambiguas debido a cambios en las reglas horarias se rechazarán con un mensaje claro, sin correcciones ni desplazamientos automáticos. La regla aplica tanto a la creación de reservas como a las consultas de disponibilidad, para evitar interpretar de forma silenciosa una hora distinta de la ingresada.
- No se impondrá una duración máxima, ya que el desafío no establece esa restricción.

**Cambios realizados en la especificación:** se actualizó RN-03 y los casos de prueba asociados al formato; se agregó una regla para horas inexistentes o ambiguas y pruebas para creación y consulta; se cerró la decisión sobre duración máxima. Los requisitos originales y las decisiones de diseño acordadas permanecen identificados por separado.

**Verificación humana:** el solicitante detectó el problema, definió las decisiones anteriores y aprobó la especificación corregida, incluidos el formato `AAAA-MM-DD HH:MM`, la zona horaria `America/Argentina/Cordoba`, el rechazo de horas locales inexistentes o ambiguas sin ajustes automáticos y la ausencia de una duración máxima. No se ejecutaron pruebas de la aplicación, que todavía no está implementada.

**Estado:** Completado.

## D-03 — Preparación de la estructura inicial

**Objetivo:** preparar una estructura mínima para una aplicación local de consola en Python, respetando la arquitectura y las decisiones de diseño aprobadas en la especificación.

**Instrucción proporcionada:** tomar como referencia [docs/especificacion.md](./especificacion.md), revisar la estructura del repositorio y crear únicamente la estructura inicial, las dependencias necesarias y la configuración imprescindible; no implementar todavía todas las funcionalidades. Registrar esta intervención y no inventar pruebas, commits, acciones ni evidencias.

**Acciones realizadas:** se comprobó que `src/` y `tests/` estaban vacíos y se revisaron la especificación, el `.gitignore` y el estado existente del repositorio. Se creó el paquete `src/reservas` con módulos separados para CLI, lógica de negocio y persistencia SQLite; la CLI quedó como punto de entrada de demostración, sin operaciones de reservas implementadas. Se añadió `data/.gitkeep` para conservar el directorio local de datos, se ampliaron las reglas de `.gitignore` para cachés Python y archivos de base de datos, y se agregó una prueba de humo con `unittest`. No se añadieron dependencias externas.

**Resultado:** el paquete puede invocarse como módulo con `python -m reservas` una vez que `src` está en `PYTHONPATH`. La CLI informa que la aplicación está en construcción; la lógica de reservas y la persistencia todavía no están implementadas.

**Verificación ejecutada:** con `src` en `PYTHONPATH`, `C:\Users\usuario\AppData\Local\Programs\Python\Python314\python.exe -m unittest discover -s tests -v` completó correctamente una prueba de humo de la estructura (1 prueba). También se invocó `C:\Users\usuario\AppData\Local\Programs\Python\Python314\python.exe -m reservas` y se comprobó que ejecuta el punto de entrada preliminar. Estas verificaciones no prueban las funcionalidades de reservas.

**Verificación humana:** el solicitante aprobó la estructura inicial y autorizó marcar este episodio como completado para realizar el commit correspondiente.

**Evidencias:** [docs/especificacion.md](./especificacion.md), archivos del esqueleto en `src/reservas/`, `tests/test_structure.py`, `data/.gitkeep`, `.gitignore` y resultados observados de los comandos anteriores. No se creó ningún commit.

**Estado:** Completado.

## D-04 — Implementación de la lógica central de reservas

**Objetivo:** implementar consulta de equipos y disponibilidad, creación y cancelación de reservas, validaciones y reglas de intervalos conforme a [docs/especificacion.md](./especificacion.md).

**Instrucción proporcionada:** implementar la etapa central de reservas dentro de la arquitectura existente, aislar SQLite en pruebas reproducibles, ejecutar las pruebas, comprobar que disponibilidad y creación comparten la regla de conflicto y dejar pendiente la verificación humana. No crear un commit.

**Acciones realizadas:** se añadieron modelos de equipo y reserva; validación estricta del formato `AAAA-MM-DD HH:MM` con la zona IANA `America/Argentina/Cordoba`; detección y rechazo de horas locales inexistentes o ambiguas; reglas de solicitante, equipo e intervalo; una comprobación de superposición compartida por consulta y creación; persistencia SQLite local con catálogo inicial fijo y estados activo/cancelado; cancelación no destructiva y una CLI para las operaciones implementadas. Las operaciones atómicas de creación y cancelación quedaron encapsuladas en el repositorio para mantener separada la lógica de negocio de SQLite. Se añadió `tzdata` como dependencia porque `zoneinfo` del entorno Windows no encontraba los datos IANA requeridos. Se sustituyó la prueba del esqueleto por pruebas con bases SQLite temporales.

**Resultado:** [src/reservas/service.py](../src/reservas/service.py) gestiona las validaciones y reglas, [src/reservas/repository.py](../src/reservas/repository.py) almacena equipos y reservas, y [src/reservas/cli.py](../src/reservas/cli.py) ofrece las operaciones en consola. La verificación técnica está registrada abajo; la aceptación humana final permanece pendiente. No se creó ningún commit.

**Verificación ejecutada:** la primera ejecución de pruebas reveló que la conexión SQLite de inicialización no confirmaba el catálogo y que la fecha de ejemplo elegida no era ambigua según los datos IANA. Se corrigió la conexión para usar confirmación automática fuera de transacciones explícitas y se verificó el ejemplo histórico ambiguo con `America/Argentina/Cordoba`. Tras encapsular las operaciones atómicas en el repositorio, en PowerShell se definió `PYTHONPATH` como la ruta de `src` y se ejecutó `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`; la suite completó correctamente 17 pruebas. El análisis de problemas no informó errores en los módulos ni en la prueba. Las pruebas usan bases de datos temporales; cubren catálogo, creación, reservas pasadas, validaciones, conflictos, consecutividad, equipos simultáneos, cancelación e historial, IDs inexistentes o ya cancelados, persistencia, reglas de fecha/zona horaria en creación y consulta, y flujo CLI. No se creó ningún commit.

**Evidencias:** [docs/especificacion.md](./especificacion.md), archivos de aplicación y pruebas en `src/reservas/` y `tests/`, y el error observado al resolver `America/Argentina/Cordoba` sin datos tzdata en el entorno Python de Windows.

**Estado:** implementación preparada; verificación humana pendiente.

### Verificación manual realizada por el solicitante

**Entorno:** Windows, PowerShell, entorno virtual de Python (`.venv`).

**Pruebas realizadas y resultados:**

1. **Persistencia entre ejecuciones:** se creó una reserva para `MIC-02`, con inicio el 25/10/2026 a las 10:00 y fin a las 12:00 (ID 3). Después de cerrar y volver a iniciar la aplicación, se consultó la disponibilidad del mismo equipo e intervalo. El sistema informó `No disponible`, confirmando que la reserva persistió.
2. **Reservas con fechas anteriores:** se creó una reserva para `MIC-01`, correspondiente al 10/10/2026 de 09:00 a 11:00 (ID 4). La operación fue aceptada.
3. **Validación de equipos:** se intentó crear una reserva para `MIC-03`, equipo inexistente en el catálogo. La operación fue rechazada con el mensaje `El equipo MIC-03 no está registrado`.
4. **Validación del intervalo:** se intentó crear una reserva para `MIC-02` con inicio el 25/10/2026 a las 09:00 y fin a las 07:00. La operación fue rechazada porque el inicio debe ser anterior al fin.

**Resultado de la verificación:** los escenarios anteriores respondieron según lo esperado. Sumados a las pruebas automatizadas ejecutadas previamente (17 pruebas aprobadas), aportan evidencia del funcionamiento de las validaciones, la persistencia y las operaciones principales.

**Evidencia:** salida de consola de la ejecución manual registrada durante la verificación del solicitante.

**Estado de D-04:** implementación y pruebas realizadas; pendiente de aceptación final.

### Revisión adicional y corrección documental

**Objetivo:** verificar la implementación y detectar posibles omisiones antes de la aceptación humana de D-04.

**Acciones realizadas por el agente:** se revisaron los módulos de servicio, repositorio, modelos y CLI, las pruebas automatizadas, la especificación, el README y las dependencias. Se ejecutó nuevamente la suite automatizada, con 17 pruebas aprobadas. La revisión identificó que el README estaba vacío y que faltaban instrucciones de preparación del entorno, instalación de dependencias, ejecución de la aplicación y pruebas.

**Corrección documental:** se completó el README con la descripción del sistema, su alcance, los requisitos, los comandos de instalación y ejecución, las instrucciones para ejecutar las pruebas, la persistencia de los datos y las limitaciones conocidas.

**Verificación posterior:** tras completar el README, se ejecutó `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` con `PYTHONPATH` configurado a la ruta de `src`; las 17 pruebas finalizaron correctamente. `git diff --check` también finalizó sin errores. Se confirmó que el README documenta preparación del entorno virtual, instalación desde `requirements.txt`, ejecución, pruebas, menú, persistencia y limitaciones actuales. No se modificó la lógica de negocio en esta revisión documental.

**Limitaciones que permanecen fuera del alcance:** no hay interfaz gráfica, acceso remoto, administración del catálogo ni opción CLI para consultar el historial completo. No se implementan autenticación real, pagos, notificaciones ni integraciones externas. No se impone una duración máxima.

**Decisión de aceptación humana:** el solicitante expresó que considera que el trabajo está correctamente encaminado y autorizó marcar D-04 como completado.

**Evidencias:** [README.md](../README.md), [docs/especificacion.md](./especificacion.md), [docs/trazabilidad.md](./trazabilidad.md), módulos bajo `src/reservas/`, [tests/test_reservations.py](../tests/test_reservations.py), salida real de las 17 pruebas automatizadas y resultado de `git diff --check`. No se creó ningún commit.

**Estado de D-04:** Completado.