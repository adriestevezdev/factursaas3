from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routers import clientes, productos, seed, dashboard

app = FastAPI(
    title="FacturSaaS API",
    description="API para sistema de facturación multi-tenant",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(clientes.router)
app.include_router(productos.router)
app.include_router(seed.router)
app.include_router(dashboard.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FacturSaaS API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}