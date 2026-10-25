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

**Referencias:** [docs/especificacion.md](./especificacion.md). El commit existente `0f07c` (`docs: Refinando las especificaciones del proyecto`) incluye cambios en la especificación y en este archivo; no se creó un commit para este episodio.

**Estado:** Completado.
