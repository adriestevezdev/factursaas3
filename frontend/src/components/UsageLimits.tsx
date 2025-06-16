'use client'

import { useEffect, useState } from 'react'
import { Progress } from '@/components/ui/progress'
import { AlertCircle } from 'lucide-react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { useBillingService } from '@/services/billing'

interface UsageLimitsProps {
  currentCount: number
  resourceType: 'clientes' | 'facturas'
}

const PLAN_LIMITS = {
  free_user: {
    clientes: 5,
    facturas: 10,
  },
  starter: {
    clientes: 50,
    facturas: 100,
  },
  pro: {
    clientes: -1, // Unlimited
    facturas: -1, // Unlimited
  },
}

export function UsageLimits({ currentCount, resourceType }: UsageLimitsProps) {
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
  
  const limits = PLAN_LIMITS[userPlan as keyof typeof PLAN_LIMITS] || PLAN_LIMITS.free_user
  const limit = limits[resourceType]
  
  // Don't show for unlimited plans or while loading
  if (loading || limit === -1) return null
  
  const percentage = (currentCount / limit) * 100
  const isNearLimit = percentage >= 80
  const isAtLimit = currentCount >= limit
  
  return (
    <div className="bg-white rounded-lg border p-4">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-medium text-gray-700">
          Límite de {resourceType === 'clientes' ? 'Clientes' : 'Facturas'}
        </h3>
        {isNearLimit && (
          <AlertCircle className="w-4 h-4 text-yellow-500" />
        )}
      </div>
      
      <div className="space-y-2">
        <Progress value={percentage} className="h-2" />
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-600">
            {currentCount} de {limit} {resourceType === 'facturas' ? 'este mes' : ''}
          </span>
          {isAtLimit && (
            <Link href="/pricing">
              <Button size="sm" variant="outline">
                Mejorar plan
              </Button>
            </Link>
          )}
        </div>
      </div>
      
      {isNearLimit && !isAtLimit && (
        <p className="text-xs text-yellow-600 mt-2">
          Te estás acercando al límite de tu plan
        </p>
      )}
    </div>
  )
}