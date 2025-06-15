'use client';

import { useUser } from '@clerk/nextjs';
import AppLayout from '@/components/AppLayout';

export default function Dashboard() {
  const { user } = useUser();

  return (
    <AppLayout>
      <div className="px-4 py-6 sm:px-0">
        <div className="border-b border-gray-200 pb-4">
          <h1 className="text-3xl font-bold leading-tight text-gray-900">
            Dashboard
          </h1>
          <p className="mt-2 max-w-4xl text-sm text-gray-500">
            Bienvenido de vuelta, {user?.firstName || 'Usuario'}
          </p>
        </div>

        <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-medium">C</span>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Total Clientes
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">0</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-medium">P</span>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Total Productos
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">0</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-yellow-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-medium">F</span>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Total Facturas
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">0</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-8">
          <div className="bg-white shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                Próximos pasos
              </h3>
              <div className="mt-5">
                <ul className="space-y-3">
                  <li className="flex items-start">
                    <div className="flex-shrink-0">
                      <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center">
                        <span className="w-2 h-2 bg-blue-600 rounded-full"></span>
                      </div>
                    </div>
                    <p className="ml-3 text-sm text-gray-700">
                      Añade tus primeros clientes en la sección{' '}
                      <strong>Clientes</strong>
                    </p>
                  </li>
                  <li className="flex items-start">
                    <div className="flex-shrink-0">
                      <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center">
                        <span className="w-2 h-2 bg-green-600 rounded-full"></span>
                      </div>
                    </div>
                    <p className="ml-3 text-sm text-gray-700">
                      Configura tu catálogo de productos y servicios en{' '}
                      <strong>Productos</strong>
                    </p>
                  </li>
                  <li className="flex items-start">
                    <div className="flex-shrink-0">
                      <div className="w-6 h-6 bg-yellow-100 rounded-full flex items-center justify-center">
                        <span className="w-2 h-2 bg-yellow-600 rounded-full"></span>
                      </div>
                    </div>
                    <p className="ml-3 text-sm text-gray-700">
                      Crea tu primera factura en la sección{' '}
                      <strong>Facturas</strong>
                    </p>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}