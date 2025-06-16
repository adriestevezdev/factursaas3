import { PricingTable } from '@clerk/nextjs'

export default function PricingPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Elige el plan perfecto para tu negocio
          </h1>
          <p className="text-xl text-gray-600">
            Gestiona tus facturas de forma profesional con FacturSaaS
          </p>
        </div>
        
        <PricingTable />
      </div>
    </div>
  )
}