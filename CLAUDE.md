# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development
- `docker compose up -d`: Start all services (PostgreSQL, FastAPI backend, Next.js frontend). Database migrations run automatically on startup.
- `docker compose logs -f backend`: View backend logs
- `docker compose logs -f frontend`: View frontend logs
- `docker compose down`: Stop all services
- `docker compose exec postgres psql -U postgres -d factursaas`: Access PostgreSQL database

### Database Operations
- **Create new migration**: `docker compose exec backend alembic revision -m "description"`
- **Run migrations**: `docker compose exec backend alembic upgrade head`
- **Rollback migration**: `docker compose exec backend alembic downgrade -1`
- **Check migration status**: `docker compose exec backend alembic current`

### Database Seeding
- **Create seed data**: `curl -X POST http://localhost:8000/seed/`
- **Delete seed data**: `curl -X DELETE http://localhost:8000/seed/`
- **Reset seed data**: `curl -X POST http://localhost:8000/seed/reset`
- **Check seed stats**: `curl http://localhost:8000/seed/stats`
- **Run seed script directly**: `docker compose exec backend python -m app.db.seed`
- **Clean seed data directly**: `docker compose exec backend python -m app.db.seed cleanup`

Note: Seed data creates 8 Spanish clients, 15 products/services, and 12 invoices with realistic data

### API Testing
- **Dashboard stats**: `curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:8000/dashboard/stats`
- **List clients**: `curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:8000/api/clientes`
- **List products**: `curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:8000/api/productos`
- **List invoices**: `curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:8000/api/facturas`
- **Billing endpoints**:
  - `curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:8000/api/billing/plan`
  - `curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:8000/api/billing/usage`
  - `curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:8000/api/billing/plans`
- **Test endpoints** (without auth):
  - `curl http://localhost:8000/dashboard/stats/test/user_test_seed_12345`
  - `curl http://localhost:8000/api/facturas/test/user_test_seed_12345`
- API documentation available at http://localhost:8000/docs

### Frontend (Next.js)
- `npm run dev`: Development server (runs inside Docker)
- `npm run build`: Production build
- `npm run lint`: Run ESLint
- `npm run type-check`: TypeScript type checking

### Backend (FastAPI)
- API automatically reloads on changes when running in Docker
- Python dependencies in `requirements.txt`
- Main entry point: `app/main.py`

## Architecture

### Multi-tenant SaaS Invoice Platform
This is a multi-tenant invoicing SaaS built with FastAPI backend and Next.js frontend, using Clerk for authentication.

**Key Architecture Principles:**
- **Multi-tenancy**: All data models include `user_id` field for tenant isolation
- **Authentication**: Clerk handles all auth; backend validates JWT tokens and extracts `user_id`
- **Data Isolation**: Every API endpoint filters data by the authenticated user's `user_id`

### Core Models
- **Cliente**: Customer management with user_id isolation (name, NIF, address, contact)
- **Producto**: Product/service catalog per user (name, price, IVA rate)
- **Factura**: Invoice with status tracking (BORRADOR, ENVIADA, PAGADA, CANCELADA)
- **LineaFactura**: Invoice line items linking products to invoices with quantity and pricing

### Backend Structure
- **Models**: SQLAlchemy models with `UserOwnedMixin` and `TimestampMixin` base classes
- **Middleware**: Clerk JWT validation in `app/middleware/auth.py`
- **Database**: PostgreSQL with Alembic migrations
- **Multi-tenant**: All endpoints use `get_current_user()` dependency to filter by `user_id`
- **API Routers**: Modular structure in `app/api/routers/` (clientes, productos, dashboard, seed)
- **Schemas**: Pydantic models for request/response validation in `app/schemas/`

### Frontend Structure
- **Next.js 15.3.3** with TypeScript and Tailwind CSS
- **Clerk Integration**: Authentication provider with protected routes
- **Components**: Reusable UI components with modal forms for CRUD operations
- **Services**: API client layer in `src/services/` for backend communication
- **Type Safety**: TypeScript interfaces matching backend schemas

## Environment Setup
Create `.env` file in root directory with:
```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_
CLERK_SECRET_KEY=sk_test_
```
Note: `DATABASE_URL` is auto-configured in Docker Compose

## Ports
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Database: localhost:5432
- Adminer (DB admin): http://localhost:8080

## Billing Plans Configuration

### Available Plans
- **Free** (free_user): 5 clientes, 10 facturas/mes, sin PDF
- **Starter** (starter - $9/mes): 50 clientes, 100 facturas/mes, exportación PDF
- **Pro** (pro - $29/mes): Ilimitado, todas las características

### Clerk Plan IDs
- Free: `free_user`
- Starter: `cplan_2yaGm3bYVgN4D3JEYwZOzTZSabD` (slug: starter)
- Pro: `cplan_2yaFQF2LIQow2BDQjtStX0zbVsg` (slug: pro)

## Important Implementation Patterns

### Multi-tenant Data Access
Every API endpoint MUST filter by user_id:
```python
# Always use get_current_user dependency
@router.get("/api/clientes")
async def get_clientes(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Cliente).filter(Cliente.user_id == current_user["user_id"]).all()
```

### Frontend API Calls
Use the API service layer for all backend communication:
```typescript
// Use services/api.ts methods
const clients = await getClientes();
const newClient = await createCliente(clientData);
```

## Current Project Status
- **Phase 1 (Infrastructure)**: ✅ Complete
- **Phase 2 (Core Features)**: ✅ Complete
  - ✅ Cliente CRUD with multi-tenant support
  - ✅ Producto CRUD with multi-tenant support  
  - ✅ Database seeding and dashboard stats
- **Phase 3 (Invoicing System)**: ✅ Complete
  - ✅ Factura backend API with full CRUD operations
  - ✅ Automatic invoice numbering per user
  - ✅ Multi-tenant validation and security
  - ✅ Frontend interface with full functionality:
    - List view with filters and actions
    - Create/Edit forms with line items management
    - Detailed view with status management
    - Automatic calculations for subtotals and taxes
- **Phase 4 (Business Features)**: ✅ Complete
  - ✅ PDF generation with ReportLab
  - ✅ Business profile configuration
- **Phase 5 (Monetization)**: 🚧 In Progress
  - ✅ Clerk Billing plan configuration (Free, Starter, Pro)
  - ✅ Backend billing middleware and limits
  - ✅ Frontend usage indicators and limits
  - ✅ Plan-based feature access (PDF export)
  - ⏳ Clerk PricingTable integration pending

## Task Management
**IMPORTANT**: Always review the `todolist.md` file to track project progress. When implementing new functionality, add a checkmark (✅) to completed tasks in `todolist.md` to differentiate them from pending tasks. This helps maintain clear visibility of project status and completed work.