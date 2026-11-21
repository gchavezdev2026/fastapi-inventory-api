from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import products

app = FastAPI(
    title="API de Gestión de Inventarios",
    description="API RESTful construida con FastAPI para la gestión integral de inventario de productos.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/api/v1")


@app.get("/", tags=["General"])
def root():
    return {
        "message": "Bienvenido a la API de Gestión de Inventario",
        "version": "1.0.0",
        "documentation": "/docs"
    }
