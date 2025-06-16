export enum EstadoFactura {
  BORRADOR = 'borrador',
  ENVIADA = 'enviada',
  PAGADA = 'pagada',
  CANCELADA = 'cancelada'
}

export interface LineaFactura {
  id?: number;
  factura_id?: number;
  producto_id: number;
  descripcion?: string;
  cantidad: number;
  precio_unitario: number;
  tipo_iva: number;
  subtotal?: number;
}

export interface Factura {
  id?: number;
  numero?: string;
  fecha: string;
  cliente_id: number;
  cliente_nombre?: string;
  subtotal?: number;
  total_iva?: number;
  total?: number;
  estado: EstadoFactura;
  notas?: string;
  user_id?: string;
  created_at?: string;
  updated_at?: string;
  lineas: LineaFactura[];
}

export interface FacturaListItem {
  id: number;
  numero: string;
  fecha: string;
  cliente_id: number;
  cliente_nombre: string;
  total: number;
  estado: EstadoFactura;
  created_at: string;
}

export interface FacturaFormData {
  cliente_id: number;
  fecha: string;
  estado: EstadoFactura;
  notas?: string;
  lineas: LineaFactura[];
}