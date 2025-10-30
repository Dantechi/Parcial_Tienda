🛒 Sistema de Gestión de Tienda Online – FastAPI

     Descripción General

Este proyecto implementa una API REST desarrollada con FastAPI y SQLModel, para la gestión de categorías y productos en una tienda online.
Cumple los criterios de evaluación del parcial de Desarrollo de Software, incluyendo CRUD completo, relaciones 1:N, validaciones, filtros, reglas de negocio y documentación Swagger.

Funcionalidades Principales

    Categorías

✅ Crear categoría (nombre, descripción)

✅ Listar categorías activas

✅ Obtener categoría junto con sus productos

✅ Actualizar datos de la categoría

✅ Desactivar categoría (eliminación lógica)

🔁 Cascada: al desactivar una categoría, sus productos quedan inactivos

    Productos

✅ Crear producto asociado a una categoría

✅ Listar productos (con filtros por stock, precio y categoría)

✅ Obtener producto con su categoría

✅ Actualizar datos de producto

✅ Desactivar producto (lógica)

✅ Restar stock al comprar producto (sin permitir negativos)

Lógica de Negocio Implementada

Nombre de categoría único – no se permiten duplicados.

Stock no puede ser negativo – se valida en creación, actualización y compra.

Cada producto pertenece a una categoría existente – validación en la relación 1:N.

Desactivación en cascada – si una categoría se desactiva, sus productos también.

Filtros dinámicos – búsqueda de productos por precio, stock o categoría.

Validaciones Pydantic – para asegurar consistencia de datos.

Manejo de errores centralizado – con códigos 400, 404, 409.

    Tecnologías Usadas

| Componente       | Descripción                         |
| ---------------- | ----------------------------------- |
| **Python 3.11+** | Lenguaje principal                  |
| **FastAPI**      | Framework para construir la API     |
| **SQLModel**     | ORM basado en SQLAlchemy y Pydantic |
| **SQLite**       | Base de datos local                 |
| **Uvicorn**      | Servidor ASGI para ejecución        |

    Estructura del Proyecto

   tienda_online/
├── main.py                # Punto de entrada de la aplicación
├── db.py                  # Configuración de base de datos
├── models.py              # Modelos SQLModel y Pydantic
├── routers/
│   ├── categorias.py      # Endpoints para categorías
│   └── productos.py       # Endpoints para productos
├── exceptions.py          # Manejo centralizado de errores
├── requirements.txt       # Dependencias del proyecto
├── .gitignore             # Ignorar archivos temporales y base local
└── README.md              # Documentación principal

    Instalación y Ejecución

1️⃣ Clonar el repositorio

git clone https://github.com/Dantechi/Parcial_Tienda.git
cd tienda-online

2️⃣ Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate   # En Linux 
.venv\Scripts\activate      # En Windows

3️⃣ Instalar dependencias
pip install -r requirements.txt

4️⃣ Ejecutar la aplicación
fastapi dev main.py

5️⃣ Abrir en el navegador

 http://127.0.0.1:8000/docs

para acceder a la documentación Swagger interactiva.

    Ejemplos de Endpoints

Categorías

| Método  | Endpoint                      | Descripción                       |
| ------- | ----------------------------- | --------------------------------- |
| `POST`  | `/categorias/`                | Crear categoría                   |
| `GET`   | `/categorias/`                | Listar categorías activas         |
| `GET`   | `/categorias/{id}`            | Obtener categoría y sus productos |
| `PUT`   | `/categorias/{id}`            | Actualizar categoría              |
| `PATCH` | `/categorias/{id}/desactivar` | Desactivar categoría              |

    Códigos de Error Implementados

| Código  | Descripción                                   |
| ------- | --------------------------------------------- |
| **200** | OK – respuesta exitosa                        |
| **201** | Recurso creado correctamente                  |
| **400** | Error de validación o regla de negocio        |
| **404** | Recurso no encontrado                         |
| **409** | Conflicto (nombre duplicado, acción inválida) |

    Commits del Proyecto (15 atómicos)

| #  | Descripción breve                                |
| -- | ------------------------------------------------ |
| 1  | Estructura base del proyecto y configuración DB  |
| 2  | Creación de modelos `Categoria` y `Producto`     |
| 3  | Router de categorías – creación y listado        |
| 4  | Obtener categoría con productos relacionados     |
| 5  | Actualizar categoría                             |
| 6  | Desactivar categoría (cascada)                   |
| 7  | Router de productos – creación básica            |
| 8  | Validación categoría existente al crear producto |
| 9  | Listar productos activos                         |
| 10 | Obtener producto con su categoría                |
| 11 | Actualizar producto                              |
| 12 | Desactivar producto                              |
| 13 | Restar stock al comprar producto                 |
| 14 | Filtros dinámicos (stock, precio, categoría)     |
| 15 | Validaciones finales y manejo global de errores  |

    Autor:

Nombre: Pablo Esteban Rincon Quinones - 67001014
Materia: Desarrollo de Software
Profesor: Sergio Galvis
Institución: Universidad Catolica De Colombia 