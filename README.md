# Sistema local de reservas de laboratorio

## 1. Especificación breve

Este proyecto documenta e implementa una aplicación local de consola para consultar y gestionar reservas del inventario inicial de equipamiento de laboratorio: MIC-01 y MIC-02 (microscopios digitales), OSC-01 (osciloscopio), MUL-01 (multímetro) y FUE-01 (fuente de alimentación).

Las reglas descritas para el proyecto establecen que:

- Las fechas se ingresan como `AAAA-MM-DD HH:MM`, en reloj de 24 horas, con la zona `America/Argentina/Cordoba` utilizada como hora local de Corrientes.
- Se rechazan equipos desconocidos, solicitantes vacíos, fechas u horas inválidas e intervalos cuyo inicio sea igual o posterior al fin.
- Los intervalos son semiabiertos `[inicio, fin)`: dos reservas consecutivas pueden compartir el límite; equipos distintos pueden reservarse simultáneamente; las reservas activas del mismo equipo no pueden superponerse.
- Las reservas pasadas se permiten. Las horas locales inexistentes o ambiguas se rechazan sin ajustarlas automáticamente.
- Cancelar conserva el registro histórico y libera el horario; las reservas activas y canceladas persisten en SQLite.

Los criterios documentados de aceptación incluyen creación válida, validación de entradas, conflictos y consecutividad, reservas simultáneas de equipos distintos, cancelación con conservación del historial y persistencia tras reiniciar. Estas reglas y pruebas se describen en [docs/especificacion.md](docs/especificacion.md).

## 2. Solución

### Estructura y decisiones técnicas

- `src/reservas/cli.py`: menú de consola.
- `src/reservas/service.py`: validaciones y reglas de reservas.
- `src/reservas/repository.py`: almacenamiento SQLite.
- `src/reservas/models.py`: modelos de equipos y reservas.
- `tests/test_reservations.py`: pruebas automatizadas.

La aplicación utiliza Python, SQLite y `unittest`. `requirements.txt` declara `tzdata`, necesario para resolver la zona horaria IANA en Windows. La base local predeterminada es `data/reservas.db`.

### Requisitos previos e instalación

Se requiere Windows, PowerShell y Python 3.10 o posterior. Ejecutá estos comandos desde la raíz del repositorio:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Ejecución

Con el entorno virtual activado, configurá `PYTHONPATH` para que Python encuentre el paquete bajo `src/` y ejecutá la aplicación:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
python -m reservas
```

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

El texto del menú, las opciones, los prompts y el formato de confirmación corresponden a la CLI actual. El ID depende de los datos existentes en la base.

### Pruebas automatizadas

Desde la raíz del repositorio, con el entorno virtual activado:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
python -m unittest discover -s tests -v
```

Las pruebas usan bases SQLite temporales, no la base local de la aplicación. Este README no afirma que se hayan ejecutado pruebas recientemente.

### Persistencia y reinicialización

La aplicación crea `data/reservas.db` si no existe, inicializa las tablas y el catálogo. Las reservas activas y canceladas permanecen al cerrar y volver a iniciar; cancelar cambia el estado sin borrar el registro. No hay borrado automático del historial.

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
- El menú no ofrece listar el historial completo, aunque el servicio conserva los registros en la base de datos.
- El catálogo inicial no se administra desde la aplicación.
- No incluye autenticación real, pagos, notificaciones ni integraciones externas.

## 3. Preparación del agente

### 3.1. Entorno y agente utilizado

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

### 3.2. Función y contexto proporcionado

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

Los extractos de los prompts iniciales se incorporaron a los episodios D-01 y D-02 de este documento. Los textos completos se pueden consultar en el historial de GitHub Copilot, pero no se archivan íntegramente en el repositorio. Los episodios posteriores se distinguen según se disponga de un prompt literal o de un resumen de la intervención.

### 3.3. Herramientas y supervisión humana

Según la información recuperada, el agente contó con capacidades para leer y modificar archivos del proyecto y ejecutar pruebas. La revisión humana se contempló mediante la inspección de los cambios propuestos, su aprobación y la ejecución de pruebas para verificar el comportamiento de la aplicación.

Estos mecanismos se consideran parte del proceso de control del desarrollo asistido. Sin embargo, la descripción de los mecanismos de supervisión no implica, por sí sola, que todos los cambios hayan sido revisados ni que todas las pruebas hayan resultado satisfactorias. La aceptación de resultados específicos debe justificarse mediante los episodios de delegación, los cambios versionados y las evidencias de prueba correspondientes.

## 4. Registro de decisiones y delegación

El documento [docs/trazabilidad.md](docs/trazabilidad.md) registra los episodios de delegación D-01 a D-04, las decisiones tomadas, las intervenciones humanas y las evidencias asociadas a los cambios versionados.

La [especificación del sistema](docs/especificacion.md) complementa este registro con los requisitos funcionales, las reglas de negocio y las decisiones de diseño.
