'use client';

import AppLayout from '@/components/AppLayout';

export default function Productos() {
  return (
    <AppLayout>
      <div className="px-4 py-6 sm:px-0">
        <div className="border-b border-gray-200 pb-4">
          <h1 className="text-3xl font-bold leading-tight text-gray-900">
            Productos
          </h1>
          <p className="mt-2 max-w-4xl text-sm text-gray-500">
            Gestiona tu catálogo de productos y servicios
          </p>
        </div>

        <div className="mt-8">
          <div className="bg-white shadow rounded-lg p-6">
            <p className="text-gray-500 text-center">
              Funcionalidad en desarrollo - Próximamente
            </p>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}