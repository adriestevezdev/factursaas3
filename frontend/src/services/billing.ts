import { useApiClient } from '@/lib/api-client'

export interface PlanInfo {
  plan: string
  limits: {
    clientes: number
    facturas_por_mes: number
    features: {
      pdf_export: boolean
      analytics: boolean
      custom_templates: boolean
    }
  }
  features: {
    pdf_export: boolean
    analytics: boolean
    custom_templates: boolean
  }
}

export interface UsageStats {
  plan: string
  usage: {
    clientes: number
    facturas_este_mes: number
  }
  limits: {
    clientes: number
    facturas_por_mes: number
  }
}

export function useBillingService() {
  const api = useApiClient()

  return {
    getUserPlan: async (): Promise<PlanInfo> => {
      return api.get<PlanInfo>('/api/billing/plan')
    },
    
    getUsageStats: async (): Promise<UsageStats> => {
      return api.get<UsageStats>('/api/billing/usage')
    },
    
    getAvailablePlans: async () => {
      return api.get('/api/billing/plans')
    }
  }
}