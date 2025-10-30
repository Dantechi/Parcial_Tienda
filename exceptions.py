from fastapi import Request
from fastapi.responses import JSONResponse

# ==========================================================
# ⚠️ MANEJO CENTRALIZADO DE ERRORES
# ==========================================================

async def validation_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=400,
        content={"error": "Error de validación de datos", "details": str(exc)},
    )


async def not_found_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Recurso no encontrado", "details": str(exc)},
    )


async def conflict_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=409,
        content={"error": "Conflicto de datos", "details": str(exc)},
    )
