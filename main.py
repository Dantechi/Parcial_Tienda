from fastapi import FastAPI
from sqlmodel import SQLModel
from db import engine
from routers import categorias, productos

# ==========================================================
# 🚀 SISTEMA DE GESTIÓN DE TIENDA ONLINE - FASTAPI
# ==========================================================
# Este sistema permite gestionar categorías y productos de una tienda online.
# Cumple con los requisitos CRUD, validaciones, relaciones 1:N, filtros y reglas de negocio.
# Documentación Swagger: http://127.0.0.1:8000/docs
# ==========================================================

app = FastAPI(
    title="API Tienda Online",
    description="Sistema de gestión de productos y categorías con SQLModel y FastAPI.",
    version="1.0.0",
)

from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from exceptions import (
    validation_exception_handler,
    not_found_exception_handler,
    conflict_exception_handler,
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, not_found_exception_handler)
app.add_exception_handler(Exception, conflict_exception_handler)


# ==========================================================
# 🧩 CREACIÓN DE TABLAS AL INICIAR
# ==========================================================
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


# ==========================================================
# 🧭 INCLUSIÓN DE RUTAS
# ==========================================================
app.include_router(categorias.router)
app.include_router(productos.router)


# ==========================================================
# 🌐 ENDPOINT RAÍZ
# ==========================================================
@app.get("/")
def root():
    """
    Endpoint raíz de verificación.
    """
    return {"message": "🛒 API de Tienda Online funcionando correctamente"}
