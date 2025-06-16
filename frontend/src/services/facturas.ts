import { useApiClient } from '@/lib/api-client';
import { Factura, FacturaListItem, FacturaFormData, EstadoFactura } from '@/types/factura';

interface FacturasQueryParams {
  skip?: number;
  limit?: number;
  estado?: EstadoFactura;
  cliente_id?: number;
  fecha_desde?: string;
  fecha_hasta?: string;
}

export function useFacturasService() {
  const api = useApiClient();

  return {
    getAll: async (params: FacturasQueryParams = {}) => {
      const queryParams = new URLSearchParams();
      if (params.skip !== undefined) queryParams.append('skip', params.skip.toString());
      if (params.limit !== undefined) queryParams.append('limit', params.limit.toString());
      if (params.estado) queryParams.append('estado', params.estado);
      if (params.cliente_id) queryParams.append('cliente_id', params.cliente_id.toString());
      if (params.fecha_desde) queryParams.append('fecha_desde', params.fecha_desde);
      if (params.fecha_hasta) queryParams.append('fecha_hasta', params.fecha_hasta);
      
      return api.get<FacturaListItem[]>(`/api/facturas?${queryParams.toString()}`);
    },

    getById: async (id: number) => {
      return api.get<Factura>(`/api/facturas/${id}`);
    },

    create: async (data: FacturaFormData) => {
      return api.post<Factura>('/api/facturas', data);
    },

    update: async (id: number, data: Partial<FacturaFormData>) => {
      return api.put<Factura>(`/api/facturas/${id}`, data);
    },

    delete: async (id: number) => {
      return api.delete<void>(`/api/facturas/${id}`);
    },
  };
}