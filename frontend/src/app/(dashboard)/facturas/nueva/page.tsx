'use client';

import FacturaForm from '@/components/facturas/FacturaForm';

export default function NuevaFacturaPage() {
  return (
    <div className="container mx-auto py-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold">Nueva Factura</h1>
        <p className="text-gray-600 mt-1">Crea una nueva factura para tus clientes</p>
      </div>

      <FacturaForm />
    </div>
  );
}