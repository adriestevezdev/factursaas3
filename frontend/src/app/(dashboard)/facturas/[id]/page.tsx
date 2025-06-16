'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useFacturasService } from '@/services/facturas';
import { useClientesService } from '@/services/clientes';
import { Factura, EstadoFactura } from '@/types/factura';
import { Cliente } from '@/types';
import { Edit, ArrowLeft, Printer, Mail, Download } from 'lucide-react';
import Link from 'next/link';
import AppLayout from '@/components/AppLayout';
import toast from 'react-hot-toast';

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

export default function FacturaDetailPage() {
  const params = useParams();
  const router = useRouter();
  const facturasService = useFacturasService();
  const clientesService = useClientesService();
  
  const [factura, setFactura] = useState<Factura | null>(null);
  const [cliente, setCliente] = useState<Cliente | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (params.id) {
      loadFactura(Number(params.id));
    }
  }, [params.id]);

  const loadFactura = async (id: number) => {
    try {
      const facturaData = await facturasService.getById(id);
      setFactura(facturaData);
      
      // Load cliente details
      if (facturaData.cliente_id) {
        const clienteData = await clientesService.getById(facturaData.cliente_id);
        setCliente(clienteData);
      }
    } catch (error) {
      console.error('Error loading factura:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR'
    }).format(amount);
  };

  const handleUpdateEstado = async (newEstado: EstadoFactura) => {
    if (!factura) return;
    
    try {
      await facturasService.update(factura.id!, { estado: newEstado });
      setFactura({ ...factura, estado: newEstado });
    } catch (error) {
      console.error('Error updating estado:', error);
    }
  };

  const handleDownloadPdf = async () => {
    if (!factura) return;
    
    try {
      await facturasService.downloadPdf(factura.id!);
      toast.success('PDF descargado correctamente');
    } catch (error) {
      console.error('Error downloading PDF:', error);
      toast.error('Error al descargar el PDF');
    }
  };

  if (loading) {
    return (
      <AppLayout>
        <p>Cargando factura...</p>
      </AppLayout>
    );
  }

  if (!factura) {
    return (
      <AppLayout>
        <p>Factura no encontrada</p>
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <div>
      <div className="flex justify-between items-center mb-6">
        <div className="flex items-center gap-4">
          <Link href="/facturas">
            <Button variant="ghost" size="sm">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Volver
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold">Factura #{factura.numero}</h1>
            <p className="text-gray-600 mt-1">
              Fecha: {new Date(factura.fecha).toLocaleDateString('es-ES')}
            </p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={handleDownloadPdf}>
            <Download className="mr-2 h-4 w-4" />
            Descargar PDF
          </Button>
          <Button variant="outline" disabled>
            <Mail className="mr-2 h-4 w-4" />
            Enviar
          </Button>
          <Link href={`/facturas/${factura.id}/editar`}>
            <Button>
              <Edit className="mr-2 h-4 w-4" />
              Editar
            </Button>
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-6">
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Información del Cliente</h2>
            {cliente ? (
              <div className="space-y-2">
                <p><strong>Nombre:</strong> {cliente.nombre}</p>
                <p><strong>NIF:</strong> {cliente.nif || 'No especificado'}</p>
                <p><strong>Email:</strong> {cliente.email || 'No especificado'}</p>
                <p><strong>Teléfono:</strong> {cliente.telefono || 'No especificado'}</p>
                {cliente.direccion && (
                  <div>
                    <p><strong>Dirección:</strong></p>
                    <p className="ml-4">{cliente.direccion}</p>
                    {(cliente.ciudad || cliente.codigo_postal) && (
                      <p className="ml-4">
                        {cliente.codigo_postal} {cliente.ciudad}
                      </p>
                    )}
                    {cliente.pais && <p className="ml-4">{cliente.pais}</p>}
                  </div>
                )}
              </div>
            ) : (
              <p className="text-gray-500">Información del cliente no disponible</p>
            )}
          </Card>

          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Líneas de Factura</h2>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="border-b">
                  <tr className="text-left">
                    <th className="p-2">Descripción</th>
                    <th className="p-2 text-right">Cantidad</th>
                    <th className="p-2 text-right">Precio Unit.</th>
                    <th className="p-2 text-right">IVA %</th>
                    <th className="p-2 text-right">Subtotal</th>
                  </tr>
                </thead>
                <tbody>
                  {factura.lineas.map((linea) => (
                    <tr key={linea.id} className="border-b">
                      <td className="p-2">{linea.descripcion}</td>
                      <td className="p-2 text-right">{linea.cantidad}</td>
                      <td className="p-2 text-right">{formatCurrency(linea.precio_unitario)}</td>
                      <td className="p-2 text-right">{linea.tipo_iva}%</td>
                      <td className="p-2 text-right">{formatCurrency(linea.subtotal || 0)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="mt-4 pt-4 border-t">
              <div className="flex justify-end">
                <div className="space-y-2 text-right">
                  <div className="flex justify-between gap-8">
                    <span>Subtotal:</span>
                    <span>{formatCurrency(factura.subtotal || 0)}</span>
                  </div>
                  <div className="flex justify-between gap-8">
                    <span>IVA:</span>
                    <span>{formatCurrency(factura.total_iva || 0)}</span>
                  </div>
                  <div className="flex justify-between gap-8 text-lg font-bold">
                    <span>Total:</span>
                    <span>{formatCurrency(factura.total || 0)}</span>
                  </div>
                </div>
              </div>
            </div>
          </Card>

          {factura.notas && (
            <Card className="p-6">
              <h2 className="text-xl font-semibold mb-4">Notas</h2>
              <p className="whitespace-pre-wrap">{factura.notas}</p>
            </Card>
          )}
        </div>

        <div className="space-y-6">
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Estado de la Factura</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span>Estado actual:</span>
                <span
                  className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium text-white ${
                    estadoColors[factura.estado]
                  }`}
                >
                  {estadoLabels[factura.estado]}
                </span>
              </div>

              <div className="pt-4 border-t">
                <p className="text-sm text-gray-600 mb-3">Cambiar estado a:</p>
                <div className="space-y-2">
                  {Object.values(EstadoFactura).map((estado) => (
                    <Button
                      key={estado}
                      variant={factura.estado === estado ? 'default' : 'outline'}
                      size="sm"
                      className="w-full"
                      onClick={() => handleUpdateEstado(estado)}
                      disabled={factura.estado === estado}
                    >
                      {estadoLabels[estado]}
                    </Button>
                  ))}
                </div>
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Información Adicional</h2>
            <div className="space-y-2 text-sm">
              <p>
                <strong>Creada:</strong>{' '}
                {factura.created_at
                  ? new Date(factura.created_at).toLocaleString('es-ES')
                  : 'No disponible'}
              </p>
              {factura.updated_at && (
                <p>
                  <strong>Última actualización:</strong>{' '}
                  {new Date(factura.updated_at).toLocaleString('es-ES')}
                </p>
              )}
            </div>
          </Card>
        </div>
      </div>
      </div>
    </AppLayout>
  );
}