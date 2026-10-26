# Sistema local de reservas de laboratorio

## 1. Especificación breve

Este proyecto documenta e implementa una aplicación local de consola para consultar y gestionar reservas del inventario inicial de equipamiento de laboratorio: MIC-01 y MIC-02 (microscopios digitales), OSC-01 (osciloscopio), MUL-01 (multímetro) y FUE-01 (fuente de alimentación).

Las reglas descritas para el proyecto establecen que:

- Las fechas se ingresan como `AAAA-MM-DD HH:MM`, en reloj de 24 horas, con la zona `America/Argentina/Cordoba` utilizada como hora local de Corrientes.
- Se rechazan equipos desconocidos, solicitantes vacíos, fechas u horas inválidas e intervalos cuyo inicio sea igual o posterior al fin.
- Los intervalos son semiabiertos `[inicio, fin)`: dos reservas consecutivas pueden compartir el límite; equipos distintos pueden reservarse simultáneamente; las reservas activas del mismo equipo no pueden superponerse.
- Las reservas pasadas se permiten. Las horas locales inexistentes o ambiguas se rechazan sin ajustarlas automáticamente.
- Cancelar conserva el registro histórico y libera el horario; las reservas activas y canceladas persisten en SQLite.

Los criterios documentados de aceptación incluyen creación válida, validación de entradas, conflictos y consecutividad, reservas simultáneas de equipos distintos, cancelación con conservación del historial y persistencia tras reiniciar. Estas reglas y pruebas se describen en [docs/especificacion.md](docs/especificacion.md); no se dispone aquí del PDF de una consigna original para verificar equivalencia con ese material.

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

[docs/trazabilidad.md](docs/trazabilidad.md) registra el uso de GitHub Copilot en modo Agent como asistente de programación en Visual Studio Code, elegido para delegar y documentar el trabajo. Allí se detallan el entorno, las instrucciones recuperables, la supervisión humana y sus límites de evidencia. No están disponibles el identificador del modelo, la versión exacta de Python usada, ni una configuración versionada o transcripción completa de los prompts.

## 4. Registro de decisiones y delegación

[docs/trazabilidad.md](docs/trazabilidad.md) contiene los episodios D-01 a D-04, las decisiones humanas registradas, las verificaciones declaradas y la relación con commits. [docs/especificacion.md](docs/especificacion.md) recoge las reglas y decisiones de diseño del sistema. Esos documentos distinguen lo que consta en archivos y Git de la información que no puede verificarse independientemente.
