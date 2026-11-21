# API REST de Gestión de Inventario con FastAPI

Una API RESTful moderna, rápida y robusta construida con **FastAPI** y **Pydantic** para la gestión integral del inventario de productos. Incluye validación estricta de datos, operaciones CRUD completas, filtrado avanzado y suite de pruebas unitarias automatizadas con **pytest**.

---

## 🚀 Características

- 📦 **CRUD Completo:** Crear, obtener (lista y por ID), actualizar (total y parcial) y eliminar productos.
- ✅ **Validación de Datos con Pydantic:** Validación automática de precios positivos (`price > 0`), cantidades no negativas (`stock >= 0`), y campos requeridos.
- 🔍 **Filtros Avanzados y Búsqueda:** Filtrado por categoría, rango de precios (`min_price`, `max_price`), búsqueda textual y paginación (`skip`, `limit`).
- 🧪 **Pruebas Unitarias:** Cobertura completa de casos de exito y de error con `pytest` y `httpx` (17 pruebas integradas).
- 📖 **Documentación Interactiva:** Documentación OpenAPI integrada accesible desde Swagger UI (`/docs`) y ReDoc (`/redoc`).

---

## 🛠️ Tecnologías Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web asíncrono y de alto rendimiento.
- **[Pydantic v2](https://docs.pydantic.dev/)**: Validación de esquemas y tipos de datos.
- **[Uvicorn](https://www.uvicorn.org/)**: Servidor ASGI ligero y ultrarrápido.
- **[Pytest](https://docs.pytest.org/)**: Framework de pruebas unitarias en Python.

---

## 📂 Estructura del Proyecto

```text
fastapi-inventory-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada de la aplicación FastAPI
│   ├── database.py          # Repositorio/Base de datos en memoria
│   ├── schemas.py           # Modelos de validación Pydantic
│   └── routers/
│       ├── __init__.py
│       └── products.py      # Endpoints CRUD para la gestión de productos
├── tests/
│   ├── __init__.py
│   └── test_products.py     # Suite de pruebas unitarias con pytest
├── .gitignore
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Documentación del proyecto
```

---

## ⚙️ Instalación y Configuración

### Prerrequisitos

- Python 3.10 o superior instalado.

### Pasos

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/gchavezdev2026/fastapi-inventory-api.git
   cd fastapi-inventory-api
   ```

2. **Crear y activar un entorno virtual:**

   - Linux / macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

3. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Ejecución del Servidor

Para iniciar el servidor de desarrollo local con recarga automática:

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en: `http://127.0.0.1:8000`

---

## 🌐 Documentación Interactiva

Una vez ejecutado el servidor, accede a la documentación interactiva desde tu navegador:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Ejecución de Pruebas Unitarias

Para ejecutar toda la suite de pruebas unitarias automatizadas:

```bash
pytest -v
```

---

## 📌 Referencia de Endpoints API

| Método | Endpoint | Descripción | Estado HTTP |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | Información general de la API | `200 OK` |
| **GET** | `/api/v1/products/` | Obtener lista de productos (soporta filtros) | `200 OK` |
| **GET** | `/api/v1/products/{id}` | Obtener producto por ID | `200 OK` / `404` |
| **POST** | `/api/v1/products/` | Crear un nuevo producto | `201 Created` / `422` |
| **PUT** | `/api/v1/products/{id}` | Actualización completa de producto | `200 OK` / `404` / `422` |
| **PATCH** | `/api/v1/products/{id}` | Actualización parcial de producto | `200 OK` / `404` / `422` |
| **DELETE** | `/api/v1/products/{id}` | Eliminar producto por ID | `204 No Content` / `404` |

---

## 📝 Ejemplos de Petición JSON

### Crear un Producto (`POST /api/v1/products/`)

```json
{
  "name": "Monitor Gamer 144Hz",
  "description": "Monitor LED Full HD de 24 pulgadas con 1ms de respuesta",
  "price": 219.99,
  "stock": 15,
  "category": "Electrónica"
}
```

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.
