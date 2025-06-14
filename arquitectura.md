# Vibe Invoice Platform

## MVP - Funcionalidades Core Simplificadas

### Frontend (Next.js)

- **Dashboard Principal**: Vista general con lista de facturas recientes
- **Gestión de Clientes**: CRUD básico (crear, ver, editar clientes)
- **Gestión de Productos**: CRUD básico para servicios/productos con precios
- **Crear Factura**: Formulario para nueva factura con:
  - Selección de cliente
  - Añadir productos/servicios
  - Cálculo automático de totales
  - Estados básicos (borrador, enviada, pagada)
- **Lista de Facturas**: Vista de todas las facturas con filtros básicos
- **Vista de Factura**: Detalle completo y opción de generar PDF

### Backend (FastAPI)

- **Models**: Cliente, Producto, Factura, LineaFactura
- **APIs REST** para:
  - Clientes (CRUD)
  - Productos (CRUD)
  - Facturas (CRUD + cambio de estado)
- **Base de datos**: PosgreSQL levantado por un docker-compose.yml
- **Generación PDF**: Librería para exportar facturas

### Estructura Técnica

- **Frontend**: Next.js 15.3.3, TypeScript, Tailwind CSS
- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Base de datos**: PostgreSQL (levantado por docker-compose.yml)
- **Autenticación**: Clerk OAuth (puedes ver el archivo CLERK_IMPLEMENTATION_GUIDE.md para implementarla) Si necesitas cualquier dato que te falte, solo preguntamelo.