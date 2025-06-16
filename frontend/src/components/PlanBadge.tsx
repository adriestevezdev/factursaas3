'use client'

import { useEffect, useState } from 'react'
import { Badge } from '@/components/ui/badge'
import { Crown, Zap, User } from 'lucide-react'
import { useBillingService } from '@/services/billing'

const PLAN_CONFIG = {
  free_user: {
    name: 'Free',
    icon: User,
    variant: 'secondary' as const,
  },
  starter: {
    name: 'Starter',
    icon: Zap,
    variant: 'default' as const,
  },
  pro: {
    name: 'Pro',
    icon: Crown,
    variant: 'destructive' as const,
  },
}

export function PlanBadge() {
  const [userPlan, setUserPlan] = useState<string>('free_user')
  const [loading, setLoading] = useState(true)
  const billingService = useBillingService()
  
  useEffect(() => {
    const fetchPlan = async () => {
      try {
        const planInfo = await billingService.getUserPlan()
        setUserPlan(planInfo.plan)
      } catch (error) {
        console.error('Error fetching plan:', error)
      } finally {
        setLoading(false)
      }
    }
    
    fetchPlan()
  }, [billingService])
  
  const planConfig = PLAN_CONFIG[userPlan as keyof typeof PLAN_CONFIG] || PLAN_CONFIG.free_user
  const Icon = planConfig.icon
  
  if (loading) {
    return (
      <Badge variant="secondary" className="flex items-center gap-1">
        <User className="w-3 h-3" />
        ...
      </Badge>
    )
  }
  
  return (
    <Badge variant={planConfig.variant} className="flex items-center gap-1">
      <Icon className="w-3 h-3" />
      {planConfig.name}
    </Badge>
  )
}