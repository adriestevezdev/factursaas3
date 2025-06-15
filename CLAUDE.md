# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development
- `docker compose up -d`: Start all services (PostgreSQL, FastAPI backend, Next.js frontend)
- `docker compose logs -f backend`: View backend logs
- `docker compose logs -f frontend`: View frontend logs
- `docker compose exec postgres psql -U postgres -d factursaas`: Access PostgreSQL database

### Frontend (Next.js)
- `npm run dev`: Development server (runs inside Docker)
- `npm run build`: Production build
- `npm run lint`: Run ESLint

### Backend (FastAPI)
- API automatically reloads on changes when running in Docker
- API documentation available at http://localhost:8000/docs
- Database migrations managed with Alembic

## Architecture

### Multi-tenant SaaS Invoice Platform
This is a multi-tenant invoicing SaaS built with FastAPI backend and Next.js frontend, using Clerk for authentication.

**Key Architecture Principles:**
- **Multi-tenancy**: All data models include `user_id` field for tenant isolation
- **Authentication**: Clerk handles all auth; backend validates JWT tokens and extracts `user_id`
- **Data Isolation**: Every API endpoint filters data by the authenticated user's `user_id`

### Core Models
- **Cliente**: Customer management with user_id isolation
- **Producto**: Product/service catalog per user
- **Factura**: Invoice with line items
- **LineaFactura**: Invoice line items linking products to invoices

### Backend Structure
- **Models**: SQLAlchemy models with `UserOwnedMixin` and `TimestampMixin` base classes
- **Middleware**: Clerk JWT validation in `app/middleware/auth.py`
- **Database**: PostgreSQL with Alembic migrations
- **Multi-tenant**: All endpoints use `get_current_user()` dependency to filter by `user_id`

### Frontend Structure
- **Next.js 15.3.3** with TypeScript and Tailwind CSS
- **Clerk Integration**: Authentication provider setup required
- **Pages**: Dashboard, client management, product management, invoice creation/management

## Environment Setup
Requires `.env` file with:
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`: Clerk public key
- `CLERK_SECRET_KEY`: Clerk secret key
- `DATABASE_URL`: PostgreSQL connection (auto-configured in Docker)

## Ports
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Database: localhost:5432
- Adminer (DB admin): http://localhost:8080

## Task Management
**IMPORTANT**: Always review the `todolist.md` file to track project progress. When implementing new functionality, add a checkmark (✅) to completed tasks in `todolist.md` to differentiate them from pending tasks. This helps maintain clear visibility of project status and completed work.