# FacturSaaS - Sistema de Facturación Multi-tenant

Sistema de facturación SaaS con autenticación Clerk, construido con FastAPI y Next.js.

## Requisitos Previos

- Docker y Docker Compose
- Cuenta en [Clerk](https://clerk.com) para obtener las claves de API

## Configuración Inicial

1. **Clonar el repositorio** (si aplica)

2. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   ```
   
   Edita el archivo `.env` y añade tus claves de Clerk:
   - `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`: Tu clave pública de Clerk
   - `CLERK_SECRET_KEY`: Tu clave secreta de Clerk

3. **Levantar los servicios con Docker Compose**
   ```bash
   docker-compose up -d
   ```

   Esto iniciará:
   - PostgreSQL en puerto 5432
   - Backend FastAPI en http://localhost:8000
   - Frontend Next.js en http://localhost:3000

## Estructura del Proyecto

```
factursaas2/
├── frontend/          # Aplicación Next.js
│   ├── src/
│   └── Dockerfile.dev
├── backend/           # API FastAPI
│   ├── app/
│   │   ├── api/      # Endpoints
│   │   ├── models/   # Modelos SQLAlchemy
│   │   ├── schemas/  # Schemas Pydantic
│   │   ├── db/       # Configuración DB
│   │   └── middleware/ # Auth con Clerk
│   └── Dockerfile.dev
└── docker-compose.yml
```

## Arquitectura de Seguridad

- **Autenticación**: Manejada completamente por Clerk
- **Multi-tenancy**: Cada recurso tiene un `user_id` que se valida contra el token JWT
- **API**: Todos los endpoints están protegidos y filtran datos por usuario

## Desarrollo

### Backend (FastAPI)

El backend se recarga automáticamente con cambios. Para ver los logs:
```bash
docker-compose logs -f backend
```

API Docs disponibles en: http://localhost:8000/docs

### Frontend (Next.js)

El frontend tiene hot-reload activado. Para ver los logs:
```bash
docker-compose logs -f frontend
```

### Base de Datos

Para acceder a PostgreSQL:
```bash
docker-compose exec postgres psql -U postgres -d factursaas
```

## Siguientes Pasos

1. Configurar Clerk en el frontend (ClerkProvider)
2. Crear las primeras migraciones con Alembic
3. Implementar CRUD de Clientes
4. Implementar CRUD de Productos
5. Sistema de Facturación