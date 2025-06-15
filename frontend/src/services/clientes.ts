import { useApiClient } from '@/lib/api-client';
import { Cliente, ClienteCreate, ClienteUpdate } from '@/types';

export function useClientesService() {
  const api = useApiClient();

  return {
    getAll: async (skip = 0, limit = 100) => {
      return api.get<Cliente[]>(`/api/clientes?skip=${skip}&limit=${limit}`);
    },

    getById: async (id: number) => {
      return api.get<Cliente>(`/api/clientes/${id}`);
    },

    create: async (data: ClienteCreate) => {
      return api.post<Cliente>('/api/clientes', data);
    },

    update: async (id: number, data: ClienteUpdate) => {
      return api.put<Cliente>(`/api/clientes/${id}`, data);
    },

    delete: async (id: number) => {
      return api.delete<void>(`/api/clientes/${id}`);
    },
  };
}