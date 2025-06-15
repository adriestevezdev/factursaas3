// Cliente types
export interface Cliente {
  id: number;
  nombre: string;
  nif?: string;
  direccion?: string;
  ciudad?: string;
  codigo_postal?: string;
  pais: string;
  email?: string;
  telefono?: string;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface ClienteCreate {
  nombre: string;
  nif?: string;
  direccion?: string;
  ciudad?: string;
  codigo_postal?: string;
  pais?: string;
  email?: string;
  telefono?: string;
}

export interface ClienteUpdate {
  nombre?: string;
  nif?: string;
  direccion?: string;
  ciudad?: string;
  codigo_postal?: string;
  pais?: string;
  email?: string;
  telefono?: string;
}

// Producto types
export interface Producto {
  id: number;
  nombre: string;
  descripcion?: string;
  precio: number;
  tipo_iva: number;
  es_servicio: boolean;
  codigo?: string;
  activo: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface ProductoCreate {
  nombre: string;
  descripcion?: string;
  precio: number;
  tipo_iva?: number;
  es_servicio?: boolean;
  codigo?: string;
  activo?: boolean;
}

export interface ProductoUpdate {
  nombre?: string;
  descripcion?: string;
  precio?: number;
  tipo_iva?: number;
  es_servicio?: boolean;
  codigo?: string;
  activo?: boolean;
}