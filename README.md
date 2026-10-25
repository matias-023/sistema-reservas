# Sistema local de reservas de laboratorio

Aplicación local de consola para consultar y gestionar reservas del equipamiento de laboratorio. Utiliza Python, SQLite y un menú interactivo; las reservas activas y canceladas se conservan en una base de datos local.

## Alcance

El sistema incluye el inventario inicial MIC-01 y MIC-02 (microscopios digitales), OSC-01 (osciloscopio), MUL-01 (multímetro) y FUE-01 (fuente de alimentación). Permite consultar equipos y disponibilidad, crear reservas y cancelar reservas mediante su ID.

Los intervalos usan el formato `AAAA-MM-DD HH:MM` y la zona horaria IANA `America/Argentina/Cordoba`, que representa la hora local utilizada en Corrientes. Se permiten reservas pasadas y no se establece una duración máxima.

## Requisitos previos

- Windows y PowerShell.
- Python 3.10 o posterior.

Ejecutá los comandos siguientes desde la carpeta raíz del repositorio.

## Preparar el entorno e instalar dependencias

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

El archivo `requirements.txt` declara `tzdata`, necesario para que Python pueda resolver la zona horaria IANA en Windows.

## Ejecutar la aplicación

Con el entorno virtual activado, configurá `PYTHONPATH` para que Python encuentre el paquete ubicado en `src/` y ejecutá el módulo:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
python -m reservas
```

El menú permite:

1. Consultar los equipos registrados.
2. Consultar la disponibilidad de un equipo para un intervalo.
3. Crear una reserva indicando equipo, solicitante, inicio y fin.
4. Cancelar una reserva mediante su ID.
0. Salir.

Las fechas deben ingresarse como `AAAA-MM-DD HH:MM`, con reloj de 24 horas y sin segundos. Las horas locales inválidas, inexistentes o ambiguas se rechazan; no se ajustan automáticamente.

## Ejecutar las pruebas automatizadas

Con el entorno virtual activado y desde la raíz del repositorio:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
python -m unittest discover -s tests -v
```

Las pruebas crean bases SQLite temporales; no usan la base local de la aplicación.

## Persistencia de datos

La aplicación crea y utiliza `data\reservas.db`, con una ruta fija relativa a la raíz del proyecto. Los datos permanecen al cerrar y volver a iniciar la aplicación. Las cancelaciones cambian el estado de la reserva y conservan su registro; no hay borrado automático del historial.

## Limitaciones y fuera de alcance

- La interfaz disponible es una CLI local; no hay interfaz gráfica ni acceso remoto.
- El menú no incluye una opción para listar o consultar el historial completo, aunque las reservas activas y canceladas se conservan en la base de datos.
- No se pueden administrar los equipos del catálogo inicial desde la aplicación.
- No incluye autenticación real, pagos, notificaciones ni integraciones externas.
