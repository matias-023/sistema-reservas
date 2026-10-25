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
