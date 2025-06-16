'use client';

import FacturaForm from '@/components/facturas/FacturaForm';
import AppLayout from '@/components/AppLayout';

export default function NuevaFacturaPage() {
  return (
    <AppLayout>
      <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold">Nueva Factura</h1>
        <p className="text-gray-600 mt-1">Crea una nueva factura para tus clientes</p>
      </div>

      <FacturaForm />
      </div>
    </AppLayout>
  );
}