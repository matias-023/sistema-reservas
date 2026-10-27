# Sistema local de reservas de laboratorio

## 1. Especificación breve

**Problema.** La coordinación de un laboratorio registra los pedidos de equipos en mensajes y en una planilla. A veces se confirma la misma unidad para horarios superpuestos y otras veces una cancelación sigue bloqueando el horario. Se necesita consultar disponibilidad, reservar y cancelar sin perder el historial.

**Alcance.** Aplicación local de consola sobre un inventario precargado, donde cada ID es una unidad física distinta: MIC-01 y MIC-02 (microscopios digitales), OSC-01 (osciloscopio), MUL-01 (multímetro) y FUE-01 (fuente de alimentación). Cada reserva ocupa una sola unidad. Quedan fuera de alcance la administración del inventario, la autenticación, las notificaciones, los pagos, las integraciones externas y la interfaz gráfica.

**Reglas y supuestos.**

- Una reserva tiene ID, unidad, solicitante (nombre ficticio en ejemplos y pruebas), inicio y fin.
- Las fechas se ingresan como `AAAA-MM-DD HH:MM`, en reloj de 24 horas, con la zona `America/Argentina/Cordoba` utilizada como hora local de Corrientes.
- Se rechazan equipos desconocidos, solicitantes vacíos o formados solo por espacios, fechas u horas inválidas e intervalos cuyo inicio sea igual o posterior al fin.
- Los intervalos son semiabiertos `[inicio, fin)`: dos reservas consecutivas pueden compartir el límite; equipos distintos pueden reservarse simultáneamente; las reservas activas del mismo equipo no pueden superponerse.
- Una reserva activa ocupa el intervalo; una cancelada no bloquea la disponibilidad. La consulta de disponibilidad usa las mismas reglas que la creación.
- Las reservas pasadas se permiten. Las horas locales inexistentes o ambiguas se rechazan sin ajustarlas automáticamente.
- No se impone una duración máxima ni un límite de anticipación, porque la consigna no los establece.
- Cancelar conserva el registro histórico y libera el horario; las reservas activas y canceladas persisten en SQLite.

**Criterios de aceptación.**

- Crear una reserva válida y recibir su ID (CP-06).
- Rechazar equipo desconocido, solicitante vacío, formato, fecha u hora inválidos e intervalo inválido (CP-07, CP-08, CP-09, CP-09a).
- Rechazar la superposición del mismo equipo (CP-10) y aceptar reservas consecutivas (CP-11) y simultáneas de equipos distintos (CP-12).
- Cancelar conservando el registro y liberando el horario (CP-13, CP-14).
- Conservar reservas activas y canceladas al reiniciar (CP-20, CP-21).

Los requisitos, las reglas y los casos de prueba CP-01 a CP-21 están en [docs/especificacion.md](docs/especificacion.md).

## 2. Solución

### Estructura y decisiones técnicas

- `src/reservas/cli.py`: menú de consola.
- `src/reservas/service.py`: validaciones y reglas de reservas.
- `src/reservas/repository.py`: almacenamiento SQLite e inventario inicial (constante `EQUIPMENT`).
- `src/reservas/models.py`: modelos de equipos y reservas.
- `src/reservas/__main__.py`: punto de entrada de `python -m reservas`.
- `tests/test_reservations.py`: pruebas automatizadas.
- `docs/`: especificación y trazabilidad. `data/`: ubicación de la base local.

La aplicación utiliza Python, SQLite y `unittest`. `requirements.txt` declara `tzdata`, necesario para resolver la zona horaria IANA en Windows. La base local predeterminada es `data/reservas.db`. Las decisiones técnicas y sus motivos están en la sección 4.

### Requisitos previos e instalación

Se desarrolló y probó en Windows con PowerShell y Python 3.14.0. No se probó con otras versiones de Python ni con otros sistemas operativos. Ejecutá estos comandos desde la raíz del repositorio:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Equivalente para Linux o macOS (no probado en este entorno):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Ejecución

Con el entorno virtual activado, configurá `PYTHONPATH` para que Python encuentre el paquete bajo `src/` y ejecutá la aplicación:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
python -m reservas
```

En Linux o macOS: `export PYTHONPATH=src` y luego `python -m reservas` (no probado en este entorno).

El menú ofrece consultar equipos, consultar disponibilidad, crear una reserva, cancelar por ID y salir. Ejemplo ilustrativo de creación —suponiendo que el intervalo está libre—:

```text
Sistema de reservas
1. Consultar equipos
2. Consultar disponibilidad
3. Crear reserva
4. Cancelar reserva
0. Salir
Opcion: 3
Equipo: MIC-01
Solicitante: Ejemplo ficticio
Inicio (AAAA-MM-DD HH:MM): 2026-10-27 14:30
Fin (AAAA-MM-DD HH:MM): 2026-10-27 15:30
Reserva creada. ID: <id asignado>
```

Con esa reserva activa, un intervalo superpuesto se rechaza y uno consecutivo está disponible (mensajes según `cli.py` y `service.py`):

```text
Opcion: 3
Equipo: MIC-01
Solicitante: Otro ejemplo
Inicio (AAAA-MM-DD HH:MM): 2026-10-27 15:00
Fin (AAAA-MM-DD HH:MM): 2026-10-27 16:00
Error: El equipo ya tiene una reserva activa que se superpone con ese intervalo.

Opcion: 2
Equipo: MIC-01
Inicio (AAAA-MM-DD HH:MM): 2026-10-27 15:30
Fin (AAAA-MM-DD HH:MM): 2026-10-27 16:30
Disponible.
```

El texto del menú, las opciones, los prompts y el formato de confirmación corresponden a la CLI actual. El ID depende de los datos existentes en la base.

### Pruebas automatizadas

Desde la raíz del repositorio, con el entorno virtual activado:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
python -m unittest discover -s tests -v
```

Las pruebas usan bases SQLite temporales, no la base local de la aplicación. Última ejecución propia registrada: 2026-10-26, Python 3.14.0, 17 pruebas, resultado `OK`. El detalle (commit, comando y estado del árbol) está en la sección 2 de [docs/trazabilidad.md](docs/trazabilidad.md).

### Persistencia y reinicialización

La aplicación crea `data/reservas.db` si no existe, inicializa las tablas y carga el inventario inicial. La base no se versiona (`data/*.db` está en `.gitignore`), por lo que una copia nueva del repositorio arranca sin reservas. Las reservas activas y canceladas permanecen al cerrar y volver a iniciar; cancelar cambia el estado sin borrar el registro. No hay borrado automático del historial.

La persistencia se verifica con pruebas automáticas que reabren el repositorio sobre el mismo archivo SQLite (`test_persists_reservations_when_repository_is_reopened` y `test_cancellation_releases_interval_and_preserves_history`). No hay una prueba que lance dos procesos de la aplicación.

Para iniciar con una base nueva, cerrá la aplicación y apartá el archivo actual. **Al iniciar con una base nueva, las reservas almacenadas en la anterior dejan de estar disponibles en esa base.** Hacé una copia de seguridad si necesitás conservarlas. Desde PowerShell, en la raíz del repositorio:

```powershell
if (Test-Path .\data\reservas.db) {
    $backup = "reservas-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss').db"
    Move-Item .\data\reservas.db ".\data\$backup"
}
```

Al volver a ejecutar la aplicación, se crea e inicializa una base nueva; las reservas anteriores no se recuperan automáticamente. Para restaurarlas, cerrá la aplicación y devolvé el archivo de respaldo a `data/reservas.db`, apartando primero la base nueva si contiene datos que quieras conservar. No muevas ni elimines el archivo mientras la aplicación esté en ejecución.

### Limitaciones

- Es una CLI local; no incluye interfaz gráfica ni acceso remoto.
- El menú no ofrece listar reservas ni el historial, aunque el servicio conserva los registros en la base de datos. El ID de una reserva solo se informa al crearla.
- El inventario inicial se define en el código y no se administra desde la aplicación.
- No incluye autenticación real, pagos, notificaciones ni integraciones externas.
- No se valida que la reserva sea futura: se pueden registrar reservas con fechas ya pasadas.
- Ctrl+C o el fin de la entrada estándar durante el menú terminan el programa con un error de Python (no se manejan).
- Solo se probó en Windows con Python 3.14.0.

## 3. Preparación del agente

### 3.1. Entorno y agente utilizado

Para el desarrollo se utilizó **GitHub Copilot en modo Agent, integrado en Visual Studio Code**. Se eligió porque actúa directamente sobre el repositorio con herramientas reales (lectura y edición de archivos, ejecución de comandos y pruebas), como exige la consigna.

| Elemento | Información |
|---|---|
| Editor | Visual Studio Code 1.143.1 |
| Extensión | GitHub Copilot |
| Agente | GitHub Copilot en modo Agent |
| Modelo | `gpt-6-luna` (identificador tal como lo muestra la herramienta) |
| Lenguaje y entorno de ejecución | Python 3.14.0, Windows, PowerShell |
| Herramientas | Lectura y modificación de archivos; ejecución de comandos y pruebas |

### 3.2. Función y contexto proporcionado

El agente se utilizó como asistente de programación para desarrollar una aplicación local de reservas de equipamiento de laboratorio. Su función comprendió el análisis de requisitos, la propuesta de soluciones técnicas y la asistencia en la implementación y las pruebas, con revisión humana de los resultados.

Contexto suministrado: la consigna del desafío (D-01), `docs/especificacion.md` como referencia (D-02 y D-03), la estructura del repositorio y las decisiones aprobadas en cada etapa. Como contexto inicial se informó que el desarrollo correspondía a un desafío académico y que se documentaría el proceso.

Contexto excluido: el repositorio ignora `.venv` y la base local (`.gitignore`); los ejemplos y las pruebas usan solicitantes ficticios y bases SQLite temporales, por lo que el agente no necesitó datos reales. No se incluyen conversaciones completas, solo extractos de las instrucciones.

### 3.3. Herramientas, controles y supervisión humana

**Acciones permitidas:** lectura y modificación de archivos del repositorio, y ejecución de comandos y de la suite de pruebas.

**Controles previstos en las instrucciones:**

- No escribir código ni modificar archivos hasta aprobar el plan (D-01, D-02).
- No agregar dependencias sin justificarlas (D-02).
- No marcar como completada la verificación humana y no crear commits automáticamente (D-03).

**Controles aplicados por mí:**

- D-01: aceptación explícita de la propuesta y fijación de las decisiones pendientes.
- D-02: revisión del alcance del commit `fff2336` con `git show --stat`.
- D-03: ejecución propia de la suite de pruebas y pruebas manuales de la aplicación.

El detalle de qué se revisó en cada episodio está en [`docs/trazabilidad.md`](docs/trazabilidad.md). Lo que no figura allí no se afirma como revisado.

### 3.4. Instrucciones y configuración

El repositorio no contiene archivos de instrucciones persistentes para Copilot (por ejemplo `.github/copilot-instructions.md` o `AGENTS.md`). Las instrucciones se dieron como prompts en el chat; los extractos literales están en los episodios D-01 a D-03 de [`docs/trazabilidad.md`](docs/trazabilidad.md).

### 3.5. Adaptación específica y retención del progreso

**Adaptación: plan antes de código y revisión humana antes de aceptar.**

- En D-01 y D-02, las instrucciones exigieron presentar un plan y no modificar archivos hasta recibir aprobación. En D-01 el agente declaró que no escribió código ni modificó archivos.
- En D-03, la instrucción pidió no marcar como completada la verificación humana y no crear commits automáticamente. No se creó ningún commit automáticamente.
- Evidencia de uso: extractos literales y resultados en D-01 a D-03, y los commits `d33f71f`, `fff2336` y `b090669`.

**Retención del progreso:** las decisiones y el avance se conservan en `docs/trazabilidad.md` y `docs/especificacion.md`, versionados en Git. La evolución se puede consultar con `git log -- docs/`.

## 4. Registro de decisiones y delegación

### Decisiones significativas

| ID | Decisión | Motivo | Alternativa posible | Consecuencia | Evidencia |
|---|---|---|---|---|---|
| DEC-01 | SQLite en `data/reservas.db` | Persistir reservas activas y canceladas entre reinicios sin servicios externos; permite comprobar conflictos e insertar dentro de una misma transacción | Archivo JSON o CSV | La base no se versiona y una copia nueva arranca vacía; sin concurrencia distribuida (fuera de alcance) | D-01; `repository.py` |
| DEC-02 | Intervalos semiabiertos `[inicio, fin)` | Permitir reservas consecutivas, como en el ejemplo de la consigna (10:00–11:00 y 11:00–12:00) | Intervalos cerrados, que rechazarían ese caso | El instante final de una reserva queda libre | RN-07; `test_accepts_consecutive_reservations` |
| DEC-03 | Zona `America/Argentina/Cordoba` y formato `AAAA-MM-DD HH:MM` | Representar la hora local de Corrientes con un único formato sin segundos | UTC-3 fijo sin dependencia externa | Se requiere `tzdata` en Windows | D-01; `requirements.txt` |
| DEC-04 | Rechazar horas locales inexistentes o ambiguas | Evitar reservar silenciosamente en un instante distinto del pedido | Tomar la primera ocurrencia o desplazar la hora | La persona debe indicar otra hora; la regla solo se activa en fechas con transiciones horarias en la zona (las pruebas usan fechas de 2008) | RN-05; pruebas de hora inexistente y ambigua |
| DEC-05 | Se permiten reservas pasadas | La consigna no las prohíbe y pide documentar su tratamiento | Rechazarlas | Se pueden registrar reservas retroactivas; las pruebas usan fechas fijas y no dependen del reloj | RN-06; `test_allows_reservations_in_the_past` |
| DEC-06 | Sin duración máxima ni límite de anticipación | La consigna no los establece; evita requisitos ocultos | Límites configurables | Cualquier intervalo válido se acepta | `docs/especificacion.md` |
| DEC-07 | Cancelación no destructiva (estado `cancelled`) | La consigna exige conservar identificador y datos | Borrar el registro | El historial crece; solo las reservas activas bloquean | RN-08, RN-09; `test_cancellation_releases_interval_and_preserves_history` |
| DEC-08 | Misma regla de conflicto para consulta y creación | Requisito explícito de la consigna; evita que la consulta diga "disponible" y la creación rechace | Duplicar la lógica en cada operación | La creación repite la comprobación dentro de la transacción | `test_availability_and_creation_share_overlap_rules` |
| DEC-09 | Menú interactivo en lugar de subcomandos | Más amigable para el usuario final (decisión humana) | CLI con argumentos | Más difícil de automatizar; la prueba de CLI simula la entrada | D-01; `test_cli_routes_equipment_booking_availability_and_cancellation` |
| DEC-10 | Guardar los instantes en UTC | Comparar intervalos de forma consistente. Decisión de implementación del agente, no definida en la especificación | Guardar la hora local sin zona | Conversión al leer y al escribir | `repository.py` (`_to_utc_string`) |

### Episodios de delegación

| Episodio | Objetivo | Decisión humana | Evidencia |
|---|---|---|---|
| D-01 | Analizar requisitos y fijar decisiones de diseño antes de programar | Aceptar la propuesta (Python, CLI, SQLite) y fijar zona horaria, ubicación de la base y formato de la CLI | Commits `0f07cf3`, `d33f71f` |
| D-02 | Crear la estructura inicial sin lógica de reservas | Aceptar y autorizar la implementación funcional | Commit `fff2336` |
| D-03 | Implementar la lógica central, las pruebas y la revisión | Aceptar sin correcciones humanas, tras ejecutar la suite y probar manualmente | Commit `b090669`; ejecución propia con 17 pruebas `OK` |

El detalle de cada episodio (extractos literales de las instrucciones, acciones del agente, decisión humana y evidencias) está en [`docs/trazabilidad.md`](docs/trazabilidad.md). La [especificación](docs/especificacion.md) detalla los requisitos, las reglas y los casos de prueba.