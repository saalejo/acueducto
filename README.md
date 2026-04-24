# Acueducto y Alcantarillado Sonadora Garzonas

Water utility billing system for the Acueducto y Alcantarillado Sonadora Garzonas cooperative. Manages customers, meter readings, consumption records, and DIAN electronic invoicing via the Apidian gateway.

## Requirements

- Python 3.11+
- SQLite (default) or PostgreSQL

## Setup

### 1. Clone and create virtual environment

```bash
git clone <repo-url>
cd acueducto
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here

# Email (Mailtrap or SMTP)
EMAIL_HOST=smtp.mailtrap.io
EMAIL_HOST_USER=your-user
EMAIL_HOST_PASSWORD=your-password
EMAIL_PORT=587
```

### 4. Run migrations

```bash
python3 manage.py migrate
```

## Running locally

### Development server

```bash
python3 manage.py runserver
```

### Production server (gunicorn)

```bash
gunicorn acueducto.wsgi:application --bind 0.0.0.0:8080
```

The app will be available at `http://localhost:8000` (dev) or `http://localhost:8080` (gunicorn).

## Running with Docker

```bash
# Build
docker build -t acueducto .

# Run — provide your .env values as -e flags or use --env-file
docker run -p 8080:8080 --env-file .env acueducto
```

The app will be available at `http://localhost:8080`.

## Management commands

```bash
# Electronic invoicing workflow
python3 manage.py preparar_facturas           # Create Factura records from unfactured Movimientos
python3 manage.py facturar_by_id <id>         # Submit a single invoice to DIAN via Apidian
python3 manage.py consultar <id>              # Query DIAN status for an invoice
python3 manage.py generar_pdf <id>            # Generate PDF for an invoice
python3 manage.py notificar <id>              # Email PDF+XML to customer

# Danger: deletes all Control/Consumo/Movimiento/Subsidio records
python3 manage.py borrar
```

## Project structure

```
acueducto/          # Django project settings
util/               # Core domain: customers, readings, consumption, billing
facturacion_electronica/  # DIAN electronic invoicing
static/spa/         # Pre-built frontend SPA
deployment/         # Kubernetes manifests
```

## Key URLs

| Path | Description |
|------|-------------|
| `/upload` | Import data from Excel files |
| `/exportar` | Export data |
| `/admin` | Django admin |
| `/api/` | REST API consumed by the SPA |
