import { useApiClient } from '@/lib/api-client';
import { PerfilEmpresa, PerfilEmpresaFormData } from '@/types/perfil-empresa';

export function usePerfilEmpresaService() {
  const api = useApiClient();

  return {
    get: async () => {
      return api.get<PerfilEmpresa | null>('/api/perfil-empresa');
    },

    create: async (data: PerfilEmpresaFormData) => {
      return api.post<PerfilEmpresa>('/api/perfil-empresa', data);
    },

    update: async (data: Partial<PerfilEmpresaFormData>) => {
      return api.put<PerfilEmpresa>('/api/perfil-empresa', data);
    },

    delete: async () => {
      return api.delete<void>('/api/perfil-empresa');
    },
  };
}