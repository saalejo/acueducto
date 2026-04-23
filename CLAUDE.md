# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A Colombian water utility billing system for the Acueducto y Alcantarillado Sonadora Garzonas cooperative. It manages customers, meter readings, consumption records, and integrates with DIAN (Colombian tax authority) for electronic invoicing via the Apidian gateway.

## Commands

```bash
# Run dev server
python3 manage.py runserver

# Migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Tests
python3 manage.py test

# Electronic invoicing workflow
python3 manage.py preparar_facturas           # Create Factura records from unfactured Movimientos
python3 manage.py facturar_by_id <id>         # Submit a single invoice to DIAN via Apidian
python3 manage.py consultar <id>              # Query DIAN status for an invoice
python3 manage.py generar_pdf <id>            # Generate PDF for an invoice
python3 manage.py notificar <id>              # Email PDF+XML to customer

# Danger: deletes all Control/Consumo/Movimiento/Subsidio records
python3 manage.py borrar
```

## Architecture

Two Django apps:

### `util` — Water utility management
Handles the core domain: customers (`Cliente`), monthly consumption records (`Consumo`), accounting movements (`Movimiento`), subsidies (`Subsidio`), and mobile meter reading routes (`Ruta` → `Lectura`).

Data entry is primarily through file import (`/upload` endpoint) using django-import-export `Resource` classes. After import, `preparar_facturas()` is automatically called to create invoices from new movements.

PDF bill generation uses ReportLab with `Elemento` model records that define text placement (x, y, font, size, formula) on the canvas. The `formula` field on `Elemento` is evaluated to produce the text content.

Key signals in `util/signals.py`:
- `after_save_dispositivo` — auto-generates a token for new mobile devices
- `after_save_ruta` — auto-creates `Lectura` records for all matching `Consumo` rows in the route's vereda
- `after_save_consumo` — converts Excel date floats to `DD/MM/YYYY` strings
- `after_save_cliente` — strips dots and whitespace from the NIT field

### `facturacion_electronica` — DIAN electronic invoicing
Converts `Movimiento` records into DIAN-compliant electronic invoices and submits them to the Apidian API.

**Invoice lifecycle:**
1. `preparar_facturas()` — creates `Factura` objects from unfactured `Movimiento`s, sets `Movimiento.facturado = True`
2. `facturar()` — renders `factura.json` template with invoice data → POSTs to Apidian → stores CUFE and DIAN response
3. `consultar()` — polls DIAN for acceptance status
4. `generarPdf()` — parses the DIAN XML response (via `untangle`) and renders a PDF using `Elemento` positions + consumption bar charts
5. `notify_mailtrap()` — sends PDF and XML attachments via SMTP (Mailtrap)

`Resolucion` holds the active DIAN resolution (prefix, number range, technical key). `Apidian` holds API credentials and certificate. `Entidad` holds the billing entity info derived from `Cliente`.

## Key model relationships

```
Movimiento ──FK──▶ Factura
Factura ◀──FK── Fila (line items)
Factura ◀──FK── Facturaimpuesto
Factura ◀──FK── Notadebito / Notacredito
Lectura ──FK──▶ Ruta ──FK──▶ Dispositivo
Lectura ──FK──▶ Consumo
```

`Consumo` and `Cliente` are linked by the `codcte` string field (not a Django FK).

## Environment

Secrets are loaded from `.env` (via `python-dotenv`) at startup. Required variables:
- `SECRET_KEY`
- `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_PORT`

The front-end is a pre-built SPA served from `/static/spa/index.html`. The Django views only expose the `/upload`, `/exportar`, and REST API endpoints used by the SPA.
