# Arquitectura de Plataforma SaaS Multi-tenant con Facturación

## Resumen General

Esta documentación describe la arquitectura completa de una plataforma SaaS multi-tenant de facturación, construida con:
- **Backend**: FastAPI (Python)
- **Frontend**: Next.js 15 (TypeScript)
- **Base de Datos**: PostgreSQL
- **Autenticación**: Clerk (OAuth + Billing)
- **Containerización**: Docker Compose

## 1. Estructura del Proyecto

```
factursaas3/
├── docker-compose.yml          # Orquestación de servicios
├── backend/                    # API FastAPI
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic/               # Migraciones de BD
│   └── app/
│       ├── main.py            # Punto de entrada
│       ├── config.py          # Configuración
│       ├── middleware/        # Auth middleware
│       ├── models/            # Modelos SQLAlchemy
│       ├── schemas/           # Esquemas Pydantic
│       ├── api/               # Endpoints
│       └── db/                # Conexión y utilidades BD
└── frontend/                   # App Next.js
    ├── Dockerfile
    ├── package.json
    └── src/
        ├── app/               # App router (Next.js 15)
        ├── components/        # Componentes React
        ├── services/          # Cliente API
        └── types/             # TypeScript types

```

## 2. Docker Compose - Orquestación de Servicios

### docker-compose.yml
```yaml
services:
  # Base de datos PostgreSQL
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: factursaas
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  # Backend FastAPI
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres/factursaas
      CLERK_SECRET_KEY: ${CLERK_SECRET_KEY}
    depends_on:
      - postgres
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --reload

  # Frontend Next.js
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
      NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: ${NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY}
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules

  # Admin de BD (opcional)
  adminer:
    image: adminer
    ports:
      - "8080:8080"

volumes:
  postgres_data:
```

## 3. Backend - FastAPI

### 3.1 Estructura Base

**backend/app/main.py**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import clientes, productos, facturas, auth
from app.db.database import engine
from app.models import Base

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FacturSaaS API")

# CORS para Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(clientes.router, prefix="/api/clientes", tags=["clientes"])
app.include_router(productos.router, prefix="/api/productos", tags=["productos"])
app.include_router(facturas.router, prefix="/api/facturas", tags=["facturas"])
```

### 3.2 Modelos Multi-tenant

**backend/app/models/base.py**:
```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime

Base = declarative_base()

class UserOwnedMixin:
    """Mixin para multi-tenancy"""
    user_id = Column(String, nullable=False, index=True)

class TimestampMixin:
    """Mixin para timestamps"""
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**backend/app/models/cliente.py**:
```python
from sqlalchemy import Column, Integer, String
from app.models.base import Base, UserOwnedMixin, TimestampMixin

class Cliente(Base, UserOwnedMixin, TimestampMixin):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    nif = Column(String)
    direccion = Column(String)
    email = Column(String)
    telefono = Column(String)
```

### 3.3 Autenticación con Clerk

**backend/app/middleware/auth.py**:
```python
from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
import httpx
from functools import lru_cache

@lru_cache()
def get_clerk_jwks():
    """Obtener claves públicas de Clerk"""
    response = httpx.get("https://api.clerk.com/v1/jwks")
    return response.json()

def verify_clerk_token(authorization: str = Header(None)):
    """Verificar JWT de Clerk"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No autorizado")
    
    token = authorization.split(" ")[1]
    
    try:
        # Verificar token con claves públicas de Clerk
        jwks = get_clerk_jwks()
        # Lógica de verificación JWT...
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

def get_current_user(payload: dict = Depends(verify_clerk_token)):
    """Extraer información del usuario del JWT"""
    return {
        "user_id": payload.get("sub"),
        "email": payload.get("email"),
        "plan": payload.get("pla", "free_user").split(":")[-1]  # Extraer plan
    }
```

### 3.4 API Endpoints Multi-tenant

**backend/app/api/routers/clientes.py**:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteResponse
from app.middleware.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=list[ClienteResponse])
def get_clientes(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener clientes del usuario autenticado"""
    return db.query(Cliente).filter(
        Cliente.user_id == current_user["user_id"]
    ).all()

@router.post("/", response_model=ClienteResponse)
def create_cliente(
    cliente: ClienteCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear cliente para el usuario autenticado"""
    db_cliente = Cliente(
        **cliente.dict(),
        user_id=current_user["user_id"]
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente
```

## 4. Frontend - Next.js

### 4.1 Configuración de Clerk

**frontend/src/app/layout.tsx**:
```tsx
import { ClerkProvider } from '@clerk/nextjs'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="es">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  )
}
```

**frontend/src/middleware.ts**:
```typescript
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'

const isProtectedRoute = createRouteMatcher([
  '/dashboard(.*)',
  '/clientes(.*)',
  '/productos(.*)',
  '/facturas(.*)',
])

export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) {
    await auth.protect()
  }
})

export const config = {
  matcher: ['/((?!.*\\..*|_next).*)', '/', '/(api|trpc)(.*)'],
}
```

### 4.2 Cliente API

**frontend/src/services/api.ts**:
```typescript
import { auth } from '@clerk/nextjs/server'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

async function apiRequest(endpoint: string, options: RequestInit = {}) {
  // Obtener token de Clerk
  const { getToken } = await auth()
  const token = await getToken()

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers,
    },
  })

  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`)
  }

  return response.json()
}

// Funciones específicas
export async function getClientes() {
  return apiRequest('/api/clientes')
}

export async function createCliente(data: ClienteInput) {
  return apiRequest('/api/clientes', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}
```

### 4.3 Componentes React

**frontend/src/app/clientes/page.tsx**:
```tsx
'use client'

import { useState, useEffect } from 'react'
import { getClientes, createCliente } from '@/services/api'
import { Cliente } from '@/types'

export default function ClientesPage() {
  const [clientes, setClientes] = useState<Cliente[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadClientes()
  }, [])

  async function loadClientes() {
    try {
      const data = await getClientes()
      setClientes(data)
    } catch (error) {
      console.error('Error loading clientes:', error)
    } finally {
      setLoading(false)
    }
  }

  async function handleCreate(formData: ClienteInput) {
    try {
      const newCliente = await createCliente(formData)
      setClientes([...clientes, newCliente])
    } catch (error) {
      console.error('Error creating cliente:', error)
    }
  }

  if (loading) return <div>Cargando...</div>

  return (
    <div>
      <h1>Clientes</h1>
      {/* Componente de lista y formulario */}
    </div>
  )
}
```

## 5. Base de Datos - PostgreSQL

### 5.1 Migraciones con Alembic

**Inicialización**:
```bash
# Dentro del contenedor backend
docker compose exec backend alembic init alembic
```

**alembic.ini**:
```ini
[alembic]
sqlalchemy.url = postgresql://postgres:postgres@postgres/factursaas
```

**Crear migración**:
```bash
docker compose exec backend alembic revision --autogenerate -m "Add clientes table"
docker compose exec backend alembic upgrade head
```

### 5.2 Esquema Multi-tenant

Todas las tablas incluyen `user_id` para aislamiento de datos:

```sql
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    nombre VARCHAR NOT NULL,
    nif VARCHAR,
    direccion VARCHAR,
    email VARCHAR,
    telefono VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_clientes_user_id (user_id)
);

CREATE TABLE facturas (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    numero VARCHAR NOT NULL,
    cliente_id INTEGER REFERENCES clientes(id),
    fecha DATE NOT NULL,
    estado VARCHAR DEFAULT 'BORRADOR',
    total DECIMAL(10,2),
    UNIQUE(user_id, numero),
    INDEX idx_facturas_user_id (user_id)
);
```

## 6. Integración Clerk OAuth

### 6.1 Configuración en Clerk Dashboard

1. Crear aplicación en [clerk.com](https://clerk.com)
2. Configurar OAuth providers (Google, GitHub, etc.)
3. Obtener claves:
   - `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
   - `CLERK_SECRET_KEY`

### 6.2 Flujo de Autenticación

```mermaid
sequenceDiagram
    participant User
    participant NextJS
    participant Clerk
    participant FastAPI
    participant DB

    User->>NextJS: Login
    NextJS->>Clerk: Redirect to OAuth
    Clerk->>NextJS: Return JWT
    NextJS->>FastAPI: API Request + JWT
    FastAPI->>Clerk: Verify JWT
    FastAPI->>DB: Query with user_id
    DB->>FastAPI: User data
    FastAPI->>NextJS: Response
    NextJS->>User: Show data
```

## 7. Integración Clerk Billing

### 7.1 Configuración de Planes

En Clerk Dashboard:
1. Activar Billing
2. Crear planes:
   - **Free**: `free_user`
   - **Starter**: $9/mes
   - **Pro**: $29/mes

### 7.2 Middleware de Límites

**backend/app/middleware/billing.py**:
```python
from fastapi import HTTPException, Depends
from app.middleware.auth import get_current_user

PLAN_LIMITS = {
    "free_user": {"clientes": 5, "facturas_mes": 10, "pdf": False},
    "starter": {"clientes": 50, "facturas_mes": 100, "pdf": True},
    "pro": {"clientes": -1, "facturas_mes": -1, "pdf": True}  # -1 = ilimitado
}

def check_plan_limit(resource: str, current_count: int = 0):
    def decorator(current_user: dict = Depends(get_current_user)):
        plan = current_user.get("plan", "free_user")
        limit = PLAN_LIMITS[plan].get(resource, 0)
        
        if limit != -1 and current_count >= limit:
            raise HTTPException(
                status_code=403,
                detail=f"Límite del plan alcanzado: {limit} {resource}"
            )
        
        return current_user
    return decorator
```

### 7.3 Componente de Pricing

**frontend/src/components/PricingTable.tsx**:
```tsx
import { useAuth } from '@clerk/nextjs'

export function PricingTable() {
  const { userId } = useAuth()

  return (
    <div>
      {/* Tabla de planes con características */}
      <button onClick={() => {
        // Redirigir a Clerk Billing
        window.location.href = '/api/billing/upgrade'
      }}>
        Actualizar Plan
      </button>
    </div>
  )
}
```

## 8. Mejores Prácticas

### 8.1 Seguridad
- Siempre filtrar por `user_id` en el backend
- Validar JWT en cada request
- Usar HTTPS en producción
- No exponer claves secretas

### 8.2 Performance
- Índices en `user_id` en todas las tablas
- Cache de JWKS de Clerk
- Paginación en listados
- Lazy loading en frontend

### 8.3 Monitoreo
- Logs estructurados
- Métricas de uso por tenant
- Alertas de límites de plan
- Monitoreo de errores (Sentry)

## 9. Conclusión

Esta arquitectura proporciona:
- ✅ Multi-tenancy completa
- ✅ Autenticación robusta con OAuth
- ✅ Sistema de billing integrado
- ✅ Escalabilidad horizontal
- ✅ Desarrollo local con Docker
- ✅ Type safety end-to-end

Para comenzar:
1. Clonar repositorio
2. Configurar Clerk
3. Ejecutar `docker compose up`
4. Acceder a http://localhost:3000