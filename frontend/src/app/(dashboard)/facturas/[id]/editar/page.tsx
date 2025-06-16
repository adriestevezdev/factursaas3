'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import FacturaForm from '@/components/facturas/FacturaForm';
import { useFacturasService } from '@/services/facturas';
import { Factura } from '@/types/factura';

export default function EditarFacturaPage() {
  const params = useParams();
  const facturasService = useFacturasService();
  const [factura, setFactura] = useState<Factura | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (params.id) {
      loadFactura(Number(params.id));
    }
  }, [params.id]);

  const loadFactura = async (id: number) => {
    try {
      const data = await facturasService.getById(id);
      setFactura(data);
    } catch (error) {
      console.error('Error loading factura:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto py-6">
        <p>Cargando factura...</p>
      </div>
    );
  }

  if (!factura) {
    return (
      <div className="container mx-auto py-6">
        <p>Factura no encontrada</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold">Editar Factura #{factura.numero}</h1>
        <p className="text-gray-600 mt-1">Modifica los datos de la factura</p>
      </div>

      <FacturaForm factura={factura} isEditing />
    </div>
  );
}