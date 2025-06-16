'use client';

import { useState, useEffect } from 'react';
import { useFacturasService } from '@/services/facturas';
import { FacturaListItem, EstadoFactura } from '@/types/factura';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Plus, Eye, Edit, Trash2, FileText } from 'lucide-react';
import Link from 'next/link';
// import { format } from 'date-fns';
// import { es } from 'date-fns/locale';

const estadoColors = {
  [EstadoFactura.BORRADOR]: 'bg-gray-500',
  [EstadoFactura.ENVIADA]: 'bg-blue-500',
  [EstadoFactura.PAGADA]: 'bg-green-500',
  [EstadoFactura.CANCELADA]: 'bg-red-500',
};

const estadoLabels = {
  [EstadoFactura.BORRADOR]: 'Borrador',
  [EstadoFactura.ENVIADA]: 'Enviada',
  [EstadoFactura.PAGADA]: 'Pagada',
  [EstadoFactura.CANCELADA]: 'Cancelada',
};

export default function FacturasPage() {
  const [facturas, setFacturas] = useState<FacturaListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedEstado, setSelectedEstado] = useState<EstadoFactura | ''>('');
  const facturasService = useFacturasService();

  useEffect(() => {
    loadFacturas();
  }, [selectedEstado]);

  const loadFacturas = async () => {
    try {
      setLoading(true);
      const params = selectedEstado ? { estado: selectedEstado } : {};
      const data = await facturasService.getAll(params);
      setFacturas(data);
    } catch (error) {
      console.error('Error loading facturas:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Está seguro de eliminar esta factura?')) {
      try {
        await facturasService.delete(id);
        await loadFacturas();
      } catch (error) {
        console.error('Error deleting factura:', error);
      }
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR'
    }).format(amount);
  };

  return (
    <div className="container mx-auto py-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold">Facturas</h1>
          <p className="text-gray-600 mt-1">Gestiona las facturas de tus clientes</p>
        </div>
        <Link href="/facturas/nueva">
          <Button>
            <Plus className="mr-2 h-4 w-4" />
            Nueva Factura
          </Button>
        </Link>
      </div>

      <Card className="mb-6 p-4">
        <div className="flex items-center gap-4">
          <label className="text-sm font-medium">Filtrar por estado:</label>
          <select
            value={selectedEstado}
            onChange={(e) => setSelectedEstado(e.target.value as EstadoFactura | '')}
            className="px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option value="">Todos</option>
            {Object.values(EstadoFactura).map((estado) => (
              <option key={estado} value={estado}>
                {estadoLabels[estado]}
              </option>
            ))}
          </select>
        </div>
      </Card>

      <Card>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="border-b">
              <tr className="text-left">
                <th className="p-4 font-medium">Número</th>
                <th className="p-4 font-medium">Fecha</th>
                <th className="p-4 font-medium">Cliente</th>
                <th className="p-4 font-medium">Total</th>
                <th className="p-4 font-medium">Estado</th>
                <th className="p-4 font-medium">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={6} className="p-4 text-center text-gray-500">
                    Cargando facturas...
                  </td>
                </tr>
              ) : facturas.length === 0 ? (
                <tr>
                  <td colSpan={6} className="p-4 text-center text-gray-500">
                    No se encontraron facturas
                  </td>
                </tr>
              ) : (
                facturas.map((factura) => (
                  <tr key={factura.id} className="border-b hover:bg-gray-50">
                    <td className="p-4 font-medium">{factura.numero}</td>
                    <td className="p-4">
                      {new Date(factura.fecha).toLocaleDateString('es-ES')}
                    </td>
                    <td className="p-4">{factura.cliente_nombre}</td>
                    <td className="p-4 font-medium">{formatCurrency(factura.total)}</td>
                    <td className="p-4">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium text-white ${
                          estadoColors[factura.estado]
                        }`}
                      >
                        {estadoLabels[factura.estado]}
                      </span>
                    </td>
                    <td className="p-4">
                      <div className="flex gap-2">
                        <Link href={`/facturas/${factura.id}`}>
                          <Button variant="ghost" size="sm">
                            <Eye className="h-4 w-4" />
                          </Button>
                        </Link>
                        <Link href={`/facturas/${factura.id}/editar`}>
                          <Button variant="ghost" size="sm">
                            <Edit className="h-4 w-4" />
                          </Button>
                        </Link>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDelete(factura.id)}
                        >
                          <Trash2 className="h-4 w-4 text-red-500" />
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}