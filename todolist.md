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

### 3. ⏳ Configurar Frontend Next.js con Clerk
- ⏳ Instalar @clerk/nextjs
- ⏳ Configurar ClerkProvider en layout
- ⏳ Proteger rutas con middleware
- ⏳ Configurar Axios/Fetch para llamadas API con auth headers
- ⏳ Layout base con navegación y componente de usuario

---

## 📋 Fase 2: Funcionalidades Core con Autenticación

### 1. CRUD de Clientes (Protegido por Usuario)
- [ ] **API endpoints en Backend:**
  - [ ] GET /api/clientes - Solo clientes del usuario autenticado
  - [ ] POST /api/clientes - Asignar automáticamente `user_id`
  - [ ] PUT /api/clientes/{id} - Verificar que el cliente pertenece al usuario
  - [ ] DELETE /api/clientes/{id} - Verificar pertenencia
- [ ] **Schemas Pydantic para validación**
- [ ] **Interfaz en Frontend:**
  - [ ] Lista filtrada por usuario actual
  - [ ] Formularios protegidos con `useAuth()`
  - [ ] Componentes de tabla y formularios

### 2. CRUD de Productos/Servicios (Protegido por Usuario)
- [ ] **API endpoints con validación de pertenencia**
- [ ] **Interfaz con datos del usuario actual**
- [ ] **Gestión de tipos de IVA**

---

## 🧾 Fase 3: Sistema de Facturación Multi-tenant

### 1. Crear Factura con Seguridad
- [ ] **Validar que cliente y productos pertenecen al usuario**
- [ ] Formulario con selección de SUS clientes
- [ ] Añadir líneas de SUS productos
- [ ] Cálculo automático de totales e IVA
- [ ] Numeración automática de facturas por usuario

### 2. Lista y Vista de Facturas
- [ ] **Filtrado automático por `user_id`**
- [ ] Estados: borrador, enviada, pagada
- [ ] Vista detallada con verificación de pertenencia
- [ ] Búsqueda y filtros avanzados

---

## 🚀 Fase 4: Mejoras con Contexto de Usuario

### 1. Generación de PDF
- [ ] Plantilla personalizable por usuario
- [ ] Logo de empresa del usuario
- [ ] Envío por email

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