import { useApiClient } from '@/lib/api-client';

export interface DashboardStats {
  clients: number;
  products: number;
  invoices: number;
  user_id: string;
}

export function useDashboardService() {
  const api = useApiClient();

  return {
    getStats: async () => {
      return api.get<DashboardStats>('/dashboard/stats');
    },
  };
}