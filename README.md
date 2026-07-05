# RescueNet

RescueNet es una aplicación desarrollada con Django para gestionar información de personas afectadas durante situaciones de emergencia.

Permite registrar reportes de personas afectadas, consultar ubicaciones reportadas y verificar el estado del servicio.

---

## Requisitos

- Python: **3+**
- Django: **6.0.6**

---

## Instalación

Clonar el repositorio:

```bash
git clone <url-del-repo>
cd a2calanche-recue-live
```

Crear un entorno virtual:

```bash
python -m venv venv
```

Activarlo:

Linux/macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Instalar Django:

```bash
pip install django
```

> **Nota:** El archivo `requirements.txt` contiene todas las dependencias, instalarlo con el siguiente comando
```bash
pip install -r requirements.txt
```

---

## Ejecutar el proyecto

Aplicar migraciones:

```bash
python manage.py migrate
```

Iniciar el servidor:

```bash
python manage.py runserver
```


---

## Ejecutar pruebas

```bash
python manage.py test
```

---

## Estructura del proyecto

```
a2calanche-recue-live/
│
├── manage.py
├── config/
└── rescue/
```

### `config/`

Contiene la configuración principal del proyecto Django:

- `settings.py` → Configuración general del proyecto.
- `urls.py` → Enrutamiento principal.
- `asgi.py` → Configuración ASGI.
- `wsgi.py` → Configuración WSGI.

### `rescue/`

Aplicación principal de RescueNet:

- `models.py` → Modelos de datos.
- `views.py` → Vistas de la API.
- `services.py` → Lógica de negocio.
- `urls.py` → Endpoints de la aplicación.
- `tests.py` → Pruebas unitarias.
- `apps.py` → Configuración de la aplicación.

---

## API

### Authentication

La API requiere una API Key en el header `X-API-Key` para aceptar solicitudes de creación de reportes.

Además, si la API va a ser consumida desde un navegador, debe configurarse `CORS_ALLOWED_ORIGINS` para permitir los orígenes esperados.

**Header**

```http
X-API-Key: your_api_key
```

**Ejemplo**

```bash
curl -X POST http://localhost:8000/api/v1/reports/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{
    "first_name": "Juan",
    "last_name": "Pérez",
    "latitude": 10.5,
    "longitude": -66.9
  }'
```

> Nota: si la variable de entorno `RESCUE_API_KEY` no está configurada, la API rechazará las peticiones con `401` por seguridad.

### GET `/api/v1/health/`

Verifica que el servicio esté disponible.

**Respuesta**

```json
{
  "status": "ok",
  "app": "rescue"
}
```

---

### POST `/api/v1/reports/`

Crea un nuevo reporte de una persona afectada junto con su ubicación.

**Recibe**

```json
{
  "first_name": "Juan",
  "last_name": "Pérez",
  "document_id": "12345678",
  "age": 30,
  "current_status": "MISSING",
  "medical_conditions": "",
  "reference_photo_url": "https://...",
  "latitude": 10.48,
  "longitude": -66.90,
  "address_description": "Centro de acopio",
  "is_verified": false
}
```

**Valores válidos para `current_status`**

- `MISSING`
- `FOUND`
- `RESCUED`
- `EVACUATED`
- `DECEASED`

**Respuesta exitosa exitosa (201)**

```json
{
  "person_id": "...",
  "status": "MISSING",
  "location_id": "..."
}
```

**Errores posibles (400)**

Si el payload viene vacío o los datos no son válidos, la API responderá con un error `400`.

```json
{
  "error": "Payload vacío"
}
```

---

### GET `/api/v1/locations/nearby/`

Obtiene un listado de las ubicaciones registradas.

**Respuesta**

```json
[
  {
    "person_id": "...",
    "full_name": "Juan Pérez",
    "status": "MISSING",
    "latitude": "10.480600",
    "longitude": "-66.903600"
  }
]
```

---

## Variables de entorno

La API requiere que `RESCUE_API_KEY` esté definida para funcionar. Si no se configura, las peticiones se rechazarán con `401`.

```env
RESCUE_API_KEY=your_api_key
```

Para permitir peticiones desde un navegador, también se recomienda configurar los orígenes permitidos:

```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

Archivo de ejemplo opcional:

```env
# .env.example
RESCUE_API_KEY=change_me
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

> Nota: `RESCUE_API_KEY` es obligatoria para levantar la API correctamente; `CORS_ALLOWED_ORIGINS` es necesario cuando se consumirá desde frontends en navegador.

En futuras versiones se moverán valores sensibles como:

```text
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
DATABASE_URL=
```

---

## Pendientes

- Confirmar la versión oficial de Python utilizada por el equipo.
- Mover `SECRET_KEY`, `DEBUG` y `ALLOWED_HOSTS` a variables de entorno para producción.

### Notas
- `POST /api/v1/reports/` está exento de protección CSRF (pensado para consumo API vía curl/cliente externo).
  Pendiente: definir estrategia de autenticación antes de producción.