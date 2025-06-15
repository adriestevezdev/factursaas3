import { useApiClient } from '@/lib/api-client';
import { Producto, ProductoCreate, ProductoUpdate } from '@/types';

export function useProductosService() {
  const api = useApiClient();

  return {
    getAll: async (skip = 0, limit = 100, soloActivos = true) => {
      return api.get<Producto[]>(`/api/productos?skip=${skip}&limit=${limit}&solo_activos=${soloActivos}`);
    },

    getById: async (id: number) => {
      return api.get<Producto>(`/api/productos/${id}`);
    },

    create: async (data: ProductoCreate) => {
      return api.post<Producto>('/api/productos', data);
    },

    update: async (id: number, data: ProductoUpdate) => {
      return api.put<Producto>(`/api/productos/${id}`, data);
    },

    delete: async (id: number) => {
      return api.delete<void>(`/api/productos/${id}`);
    },
  };
}