'use client';

import { SignInButton, useAuth } from '@clerk/nextjs';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import AppLayout from '@/components/AppLayout';

export default function Home() {
  const { isSignedIn, isLoaded } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isLoaded && isSignedIn) {
      router.push('/dashboard');
    }
  }, [isLoaded, isSignedIn, router]);

  if (!isLoaded) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando...</p>
        </div>
      </div>
    );
  }

  if (isSignedIn) {
    return null; // Will redirect to dashboard
  }

  return (
    <AppLayout>
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">FacturSaaS</h1>
            <p className="text-lg text-gray-600 mb-8">
              Sistema de facturación multi-tenant
            </p>
            <p className="text-sm text-gray-500 mb-8">
              Gestiona tus clientes, productos y facturas de forma sencilla y segura
            </p>
            <SignInButton mode="modal">
              <button className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 font-medium">
                Iniciar Sesión
              </button>
            </SignInButton>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
