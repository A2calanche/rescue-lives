# RescueNet

RescueNet es una aplicación desarrollada con Django para gestionar información de personas afectadas durante situaciones de emergencia.

Permite registrar reportes de personas afectadas, consultar ubicaciones reportadas y verificar el estado del servicio.

---

## Requisitos

- Python: **Definir versión del equipo** (pendiente de confirmar)
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

> **Nota:** El archivo `requirements.txt` aún no existe. Una vez instalado Django, generarlo con:

```bash
pip freeze > requirements.txt
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

> **Nota:** Si `migrate` falla debido a la configuración de `INSTALLED_APPS`, reportarlo al responsable correspondiente y continuar con la documentación mientras se corrige.

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

### GET `/api/health/`

Verifica que el servicio esté disponible.

**Respuesta**

```json
{
  "status": "ok",
  "app": "rescue"
}
```

---

### POST `/api/reports/`

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

**Respuesta (201)**

```json
{
  "person_id": "...",
  "status": "MISSING",
  "location_id": "..."
}
```

---

### GET `/api/locations/nearby/`

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

Actualmente el proyecto no utiliza variables de entorno.

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
- Configurar variables de entorno para producción.

### Notas
- `POST /api/reports/` está exento de protección CSRF (pensado para consumo API vía curl/cliente externo).
  Pendiente: definir estrategia de autenticación antes de producción.