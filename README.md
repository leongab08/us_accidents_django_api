# US Accidents Django API

Backend API con Django + PostgreSQL para consultar y analizar accidentes de trafico en EE. UU.

Incluye:
- API REST para listados y analitica.
- Integracion LLM (OpenAI) con tools (function calling) sobre datos reales.
- Inicializacion de base con esquema SQL y carga opcional desde CSV.

## 1) Estructura del proyecto

- `docker-compose.yml`: servicio PostgreSQL.
- `backend/manage.py`: entrypoint de Django.
- `backend/config/`: settings y rutas principales.
- `backend/presentacion/`: endpoints HTTP.
- `backend/negocio/`: servicios de negocio y schemas.
- `backend/persistencia/`: modelos ORM y repositorios.
- `backend/data/db/init/01_create_table.sql`: crea tabla + indices.
- `backend/data/db/init/02_load_data.sh`: carga CSV al crear volumen (si existe el archivo).
- `backend/data/US_Accidents_March23.csv`: dataset (opcional, ignorado por git).
- `.env.example`: variables de entorno base.

## 2) Requisitos

- Docker Desktop
- Python 3.11+ (se recomienda usar venv)
- PowerShell (comandos del README)

## 3) Configuracion rapida desde cero

### Paso A: crear `.env`

En la raiz del repo, crea `.env` copiando `.env.example`.

Variables minimas:

```env
POSTGRES_DB=accidents_db
POSTGRES_USER=accidents_user
POSTGRES_PASSWORD=accidents_pass
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
```

Nota: Django carga este `.env` automaticamente desde `backend/config/settings.py`.

### Paso B: levantar PostgreSQL

Desde la raiz del proyecto:

```powershell
docker compose up -d postgres
```

Verificar que la tabla existe:

```powershell
docker compose exec -T postgres psql -U accidents_user -d accidents_db -c "\dt"
```

Ver conteo:

```powershell
docker compose exec -T postgres psql -U accidents_user -d accidents_db -c "SELECT COUNT(*) AS total_rows FROM us_accidents;"
```

### Paso C: levantar Django

Desde la carpeta `backend`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Si `OPENAI_API_KEY` esta vacia, los endpoints LLM responderan error (los endpoints de analitica siguen funcionando).

## 4) Probar endpoints

Base URL local:

`http://127.0.0.1:8000`

### Salud y listado

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/health/
Invoke-RestMethod "http://127.0.0.1:8000/api/accidents/?limit=20&offset=0&state=CA&severity=2"
```

### Analitica

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/api/analytics/top-states/?limit=10"
Invoke-RestMethod http://127.0.0.1:8000/api/analytics/day-night/
Invoke-RestMethod http://127.0.0.1:8000/api/analytics/hourly/
Invoke-RestMethod http://127.0.0.1:8000/api/analytics/weekday/
```

### LLM con tools

Catalogo de tools:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/llm/tools/
```

Pregunta en lenguaje natural:

```powershell
$body = @{ question = "En que estado ocurren mas accidentes?" } | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/llm/ask/ -Method POST -ContentType "application/json" -Body $body
```

## 5) Carga de datos: con CSV y sin CSV

### Modo con CSV

Si existe `backend/data/US_Accidents_March23.csv`, al crear el volumen de PostgreSQL por primera vez:
- se crea `us_accidents`
- se ejecuta `COPY`
- se carga todo el dataset

### Modo sin CSV

Si el CSV no existe, el script `02_load_data.sh` omite la carga automaticamente.
Esto te deja la base lista con el esquema para insertar datos por API/SQL mas adelante.

## 6) Esquema actual de la tabla (replicable sin CSV)

SQL completo usado por el proyecto:

```sql
CREATE TABLE IF NOT EXISTS us_accidents (
	id TEXT PRIMARY KEY,
	source TEXT NULL,
	severity SMALLINT NULL,
	start_time TIMESTAMP NULL,
	end_time TIMESTAMP NULL,
	start_lat DOUBLE PRECISION NULL,
	start_lng DOUBLE PRECISION NULL,
	end_lat DOUBLE PRECISION NULL,
	end_lng DOUBLE PRECISION NULL,
	distance_mi DOUBLE PRECISION NULL,
	description TEXT NULL,
	street TEXT NULL,
	city TEXT NULL,
	county TEXT NULL,
	state VARCHAR(2) NULL,
	zipcode TEXT NULL,
	country VARCHAR(2) NULL,
	timezone TEXT NULL,
	airport_code TEXT NULL,
	weather_timestamp TIMESTAMP NULL,
	temperature_f DOUBLE PRECISION NULL,
	wind_chill_f DOUBLE PRECISION NULL,
	humidity_pct DOUBLE PRECISION NULL,
	pressure_in DOUBLE PRECISION NULL,
	visibility_mi DOUBLE PRECISION NULL,
	wind_direction TEXT NULL,
	wind_speed_mph DOUBLE PRECISION NULL,
	precipitation_in DOUBLE PRECISION NULL,
	weather_condition TEXT NULL,
	amenity BOOLEAN NULL,
	bump BOOLEAN NULL,
	crossing BOOLEAN NULL,
	give_way BOOLEAN NULL,
	junction BOOLEAN NULL,
	no_exit BOOLEAN NULL,
	railway BOOLEAN NULL,
	roundabout BOOLEAN NULL,
	station BOOLEAN NULL,
	stop BOOLEAN NULL,
	traffic_calming BOOLEAN NULL,
	traffic_signal BOOLEAN NULL,
	turning_loop BOOLEAN NULL,
	sunrise_sunset TEXT NULL,
	civil_twilight TEXT NULL,
	nautical_twilight TEXT NULL,
	astronomical_twilight TEXT NULL
);

CREATE INDEX IF NOT EXISTS idx_us_accidents_start_time ON us_accidents (start_time);
CREATE INDEX IF NOT EXISTS idx_us_accidents_state ON us_accidents (state);
CREATE INDEX IF NOT EXISTS idx_us_accidents_city ON us_accidents (city);
CREATE INDEX IF NOT EXISTS idx_us_accidents_severity ON us_accidents (severity);
CREATE INDEX IF NOT EXISTS idx_us_accidents_start_lat_lng ON us_accidents (start_lat, start_lng);
```

## 7) Reset completo de base

```powershell
docker compose down -v
docker compose up -d postgres
```

Recuerda: los scripts de init solo se ejecutan cuando el volumen se crea de nuevo.
