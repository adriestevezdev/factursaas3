# Plan de Implementación - FacturSaaS MVP

## ✅ Fase 1: Infraestructura Base (COMPLETADA)

### 1. ✅ Configurar Docker Compose
- ✅ PostgreSQL con volumen persistente
- ✅ Backend FastAPI con Dockerfile.dev
- ✅ Frontend Next.js (OBLIGATORIO en Docker con Dockerfile.dev)
- ✅ Usar `npm install` en lugar de `npm ci` para desarrollo

### 2. ✅ Estructura Backend FastAPI con Autenticación Clerk
- ✅ Crear estructura de carpetas (app/, models/, api/, db/, middleware/)
- ✅ Configurar FastAPI básico con CORS
- ✅ Integrar Clerk para autenticación (middleware preparado)
- ✅ Configurar SQLAlchemy y conexión a PostgreSQL
- ✅ Crear modelos base con `user_id` vinculado a Clerk

### 3. ✅ Configurar Frontend Next.js con Clerk
- ✅ Instalar @clerk/nextjs
- ✅ Configurar ClerkProvider en layout
- ✅ Proteger rutas con middleware
- ✅ Configurar Axios/Fetch para llamadas API con auth headers
- ✅ Layout base con navegación y componente de usuario

---

## 📋 Fase 2: Funcionalidades Core con Autenticación

### 1. CRUD de Clientes (Protegido por Usuario)
- [✅] **API endpoints en Backend:**
  - [✅] GET /api/clientes - Solo clientes del usuario autenticado
  - [✅] POST /api/clientes - Asignar automáticamente `user_id`
  - [✅] PUT /api/clientes/{id} - Verificar que el cliente pertenece al usuario
  - [✅] DELETE /api/clientes/{id} - Verificar pertenencia
- [✅] **Schemas Pydantic para validación**
- [✅] **Interfaz en Frontend:**
  - [✅] Lista filtrada por usuario actual
  - [✅] Formularios protegidos con `useAuth()`
  - [✅] Componentes de tabla y formularios

### 2. CRUD de Productos/Servicios (Protegido por Usuario)
- [✅] **API endpoints con validación de pertenencia**
- [✅] **Interfaz con datos del usuario actual**
- [✅] **Gestión de tipos de IVA**

### 3. Poblar Base de Datos con Datos de Ejemplo ✅
- [x] **Crear script de seed (backend/app/db/seed.py)** ✅
  - [x] Datos de ejemplo de clientes (8 registros con datos realistas españoles) ✅
  - [x] Datos de ejemplo de productos/servicios (15 registros con precios y IVA) ✅
  - [x] Datos de ejemplo de facturas (12 registros con diferentes estados) ✅
  - [x] Usar un user_id de prueba consistente (`user_test_seed_12345`) ✅
- [x] **Crear comando para ejecutar el seed** ✅
  - [x] Endpoints REST: POST/DELETE/PUT `/api/seed/` ✅
  - [x] Script ejecutable via Docker ✅
  - [x] Documentar cómo ejecutar el seed en CLAUDE.md ✅
- [x] **Endpoints de estadísticas del dashboard** ✅
  - [x] GET /api/dashboard/stats para contar clientes, productos, facturas ✅
  - [x] Autenticación con Clerk JWT mejorada ✅

---

## 🧾 Fase 3: Sistema de Facturación Multi-tenant

### 1. Backend de Facturas ✅
- [x] **Modelos de Factura y LineaFactura con SQLAlchemy** ✅
- [x] **Migración de Alembic para tablas facturas y lineas_factura** ✅
- [x] **Schemas Pydantic para validación** ✅
- [x] **Endpoints CRUD con validación multi-tenant** ✅
  - [x] GET /api/facturas - Lista facturas del usuario
  - [x] GET /api/facturas/{id} - Detalle de factura
  - [x] POST /api/facturas - Crear factura
  - [x] PUT /api/facturas/{id} - Actualizar factura
  - [x] DELETE /api/facturas/{id} - Eliminar factura
- [x] **Numeración automática de facturas por usuario** ✅
- [x] **Validación que cliente y productos pertenecen al usuario** ✅
- [x] **Cálculo automático de totales e IVA** ✅

### 2. Frontend de Facturas ✅
- [x] Lista de facturas con tabla y filtros ✅
  - [x] Tabla con información de facturas
  - [x] Filtro por estado
  - [x] Acciones de ver, editar y eliminar
- [x] Formulario de creación/edición ✅
  - [x] Selección de cliente
  - [x] Gestión de líneas de factura
  - [x] Cálculo automático de totales
  - [x] Selección de productos con auto-completado de datos
- [x] Vista detallada de factura ✅
  - [x] Información completa del cliente
  - [x] Detalle de líneas y totales
  - [x] Visualización de notas
- [x] Gestión de estados de factura ✅
  - [x] Cambio de estado desde la vista detallada
  - [x] Indicadores visuales por estado

---

## 🚀 Fase 4: Mejoras con Contexto de Usuario

### 1. Generación de PDF
- [ ] Plantilla personalizable por usuario
- [ ] Logo de empresa del usuario

### 2. Dashboard con métricas por usuario
- [ ] Facturas del mes
- [ ] Clientes activos
- [ ] Productos más vendidos
- [ ] Gráficos de evolución

### 3. Configuración de perfil empresarial
- [ ] Datos fiscales de la empresa
- [ ] Logo y personalización
- [ ] Configuración de numeración de facturas

---

## 🔐 Arquitectura de Seguridad Clerk + CRUD

### Frontend (Next.js):
- ClerkProvider envuelve la app
- Middleware protege rutas privadas
- useUser() para datos del usuario
- Headers con Bearer token en API calls

### Backend (FastAPI):
- Middleware verifica JWT de Clerk
- Extrae `userId` del token
- Todos los modelos incluyen `user_id`
- Queries filtradas por `user_id`
- Validación de pertenencia en updates/deletes

### Base de Datos:
- Índices en columnas `user_id`
- Foreign keys para integridad
- Sin datos de usuarios (gestionados por Clerk)

---

## 📝 Notas de Implementación

- **Multi-tenancy**: Cada recurso está aislado por `user_id`
- **Seguridad**: Doble verificación (JWT + pertenencia de recursos)
- **Escalabilidad**: Preparado para múltiples usuarios desde el inicio
- **Mantenibilidad**: Separación clara entre autenticación (Clerk) y autorización (app)