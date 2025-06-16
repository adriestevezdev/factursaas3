'use client'

import { useUser } from '@clerk/nextjs'
import { Badge } from '@/components/ui/badge'
import { Crown, Zap, User } from 'lucide-react'

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
  const { user } = useUser()
  
  // Get the user's plan from metadata
  const userPlan = user?.publicMetadata?.plan as string || 'free_user'
  const planConfig = PLAN_CONFIG[userPlan as keyof typeof PLAN_CONFIG] || PLAN_CONFIG.free_user
  
  const Icon = planConfig.icon
  
  return (
    <Badge variant={planConfig.variant} className="flex items-center gap-1">
      <Icon className="w-3 h-3" />
      {planConfig.name}
    </Badge>
  )
}