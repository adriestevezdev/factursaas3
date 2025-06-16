'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { useFacturasService } from '@/services/facturas';
import { useClientesService } from '@/services/clientes';
import { useProductosService } from '@/services/productos';
import { Factura, FacturaFormData, LineaFactura, EstadoFactura } from '@/types/factura';
import { Cliente } from '@/types';
import { Producto } from '@/types';
import { Plus, Trash2 } from 'lucide-react';

interface FacturaFormProps {
  factura?: Factura;
  isEditing?: boolean;
}

export default function FacturaForm({ factura, isEditing = false }: FacturaFormProps) {
  const router = useRouter();
  const facturasService = useFacturasService();
  const clientesService = useClientesService();
  const productosService = useProductosService();

  const [loading, setLoading] = useState(false);
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [productos, setProductos] = useState<Producto[]>([]);
  
  const [formData, setFormData] = useState<FacturaFormData>({
    cliente_id: factura?.cliente_id || 0,
    fecha: factura?.fecha || new Date().toISOString().split('T')[0],
    estado: factura?.estado || EstadoFactura.BORRADOR,
    notas: factura?.notas || '',
    lineas: factura?.lineas || []
  });

  useEffect(() => {
    loadClientes();
    loadProductos();
  }, []);

  const loadClientes = async () => {
    try {
      const data = await clientesService.getAll();
      setClientes(data);
    } catch (error) {
      console.error('Error loading clientes:', error);
    }
  };

  const loadProductos = async () => {
    try {
      const data = await productosService.getAll();
      setProductos(data);
    } catch (error) {
      console.error('Error loading productos:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (isEditing && factura?.id) {
        await facturasService.update(factura.id, formData);
      } else {
        await facturasService.create(formData);
      }
      router.push('/facturas');
    } catch (error) {
      console.error('Error saving factura:', error);
      alert('Error al guardar la factura');
    } finally {
      setLoading(false);
    }
  };

  const addLinea = () => {
    setFormData({
      ...formData,
      lineas: [
        ...formData.lineas,
        {
          producto_id: 0,
          cantidad: 1,
          precio_unitario: 0,
          tipo_iva: 21,
          descripcion: ''
        }
      ]
    });
  };

  const removeLinea = (index: number) => {
    setFormData({
      ...formData,
      lineas: formData.lineas.filter((_, i) => i !== index)
    });
  };

  const updateLinea = (index: number, field: keyof LineaFactura, value: any) => {
    const newLineas = [...formData.lineas];
    newLineas[index] = { ...newLineas[index], [field]: value };
    
    // Si se selecciona un producto, actualizar precio y descripción
    if (field === 'producto_id' && value) {
      const producto = productos.find(p => p.id === Number(value));
      if (producto) {
        newLineas[index].precio_unitario = producto.precio;
        newLineas[index].tipo_iva = producto.tipo_iva || 21;
        newLineas[index].descripcion = producto.descripcion || producto.nombre;
      }
    }
    
    setFormData({ ...formData, lineas: newLineas });
  };

  const calculateTotals = () => {
    let subtotal = 0;
    let totalIva = 0;

    formData.lineas.forEach(linea => {
      const lineaSubtotal = linea.cantidad * linea.precio_unitario;
      const lineaIva = lineaSubtotal * (linea.tipo_iva / 100);
      subtotal += lineaSubtotal;
      totalIva += lineaIva;
    });

    return {
      subtotal: subtotal.toFixed(2),
      totalIva: totalIva.toFixed(2),
      total: (subtotal + totalIva).toFixed(2)
    };
  };

  const totals = calculateTotals();

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Información General</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="cliente">Cliente *</Label>
            <select
              id="cliente"
              required
              value={formData.cliente_id}
              onChange={(e) => setFormData({ ...formData, cliente_id: Number(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="">Seleccionar cliente</option>
              {clientes.map((cliente) => (
                <option key={cliente.id} value={cliente.id}>
                  {cliente.nombre}
                </option>
              ))}
            </select>
          </div>

          <div>
            <Label htmlFor="fecha">Fecha *</Label>
            <Input
              id="fecha"
              type="date"
              required
              value={formData.fecha}
              onChange={(e) => setFormData({ ...formData, fecha: e.target.value })}
            />
          </div>

          <div>
            <Label htmlFor="estado">Estado</Label>
            <select
              id="estado"
              value={formData.estado}
              onChange={(e) => setFormData({ ...formData, estado: e.target.value as EstadoFactura })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value={EstadoFactura.BORRADOR}>Borrador</option>
              <option value={EstadoFactura.ENVIADA}>Enviada</option>
              <option value={EstadoFactura.PAGADA}>Pagada</option>
              <option value={EstadoFactura.CANCELADA}>Cancelada</option>
            </select>
          </div>
        </div>

        <div className="mt-4">
          <Label htmlFor="notas">Notas</Label>
          <Textarea
            id="notas"
            value={formData.notas}
            onChange={(e) => setFormData({ ...formData, notas: e.target.value })}
            rows={3}
          />
        </div>
      </Card>

      <Card className="p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Líneas de Factura</h2>
          <Button type="button" onClick={addLinea} variant="outline">
            <Plus className="mr-2 h-4 w-4" />
            Añadir Línea
          </Button>
        </div>

        {formData.lineas.length === 0 ? (
          <p className="text-gray-500 text-center py-4">
            No hay líneas añadidas. Haz clic en "Añadir Línea" para comenzar.
          </p>
        ) : (
          <div className="space-y-4">
            {formData.lineas.map((linea, index) => (
              <div key={index} className="border rounded-lg p-4">
                <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
                  <div className="md:col-span-2">
                    <Label>Producto</Label>
                    <select
                      value={linea.producto_id}
                      onChange={(e) => updateLinea(index, 'producto_id', Number(e.target.value))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                      required
                    >
                      <option value="">Seleccionar producto</option>
                      {productos.map((producto) => (
                        <option key={producto.id} value={producto.id}>
                          {producto.nombre}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <Label>Cantidad</Label>
                    <Input
                      type="number"
                      step="0.01"
                      min="0.01"
                      value={linea.cantidad}
                      onChange={(e) => updateLinea(index, 'cantidad', Number(e.target.value))}
                      required
                    />
                  </div>

                  <div>
                    <Label>Precio Unit.</Label>
                    <Input
                      type="number"
                      step="0.01"
                      min="0"
                      value={linea.precio_unitario}
                      onChange={(e) => updateLinea(index, 'precio_unitario', Number(e.target.value))}
                      required
                    />
                  </div>

                  <div>
                    <Label>IVA %</Label>
                    <Input
                      type="number"
                      step="0.01"
                      min="0"
                      max="100"
                      value={linea.tipo_iva}
                      onChange={(e) => updateLinea(index, 'tipo_iva', Number(e.target.value))}
                      required
                    />
                  </div>

                  <div className="flex items-end">
                    <Button
                      type="button"
                      variant="ghost"
                      onClick={() => removeLinea(index)}
                      className="text-red-500"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>

                <div className="mt-2">
                  <Label>Descripción</Label>
                  <Input
                    type="text"
                    value={linea.descripcion}
                    onChange={(e) => updateLinea(index, 'descripcion', e.target.value)}
                    placeholder="Descripción opcional"
                  />
                </div>
              </div>
            ))}
          </div>
        )}

        <div className="mt-6 border-t pt-4">
          <div className="flex justify-end space-y-2">
            <div className="text-right">
              <div className="flex justify-between gap-8">
                <span>Subtotal:</span>
                <span className="font-medium">€{totals.subtotal}</span>
              </div>
              <div className="flex justify-between gap-8">
                <span>IVA:</span>
                <span className="font-medium">€{totals.totalIva}</span>
              </div>
              <div className="flex justify-between gap-8 text-lg font-bold">
                <span>Total:</span>
                <span>€{totals.total}</span>
              </div>
            </div>
          </div>
        </div>
      </Card>

      <div className="flex gap-4">
        <Button type="submit" disabled={loading}>
          {loading ? 'Guardando...' : isEditing ? 'Actualizar Factura' : 'Crear Factura'}
        </Button>
        <Button
          type="button"
          variant="outline"
          onClick={() => router.push('/facturas')}
        >
          Cancelar
        </Button>
      </div>
    </form>
  );
}