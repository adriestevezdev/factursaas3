'use client';

import { useState, useEffect } from 'react';
import { Producto, ProductoCreate, ProductoUpdate } from '@/types';
import { useProductosService } from '@/services/productos';

interface ProductoModalProps {
  producto: Producto | null;
  onClose: () => void;
  onSuccess: () => void;
}

const IVA_OPTIONS = [
  { value: 0, label: '0%' },
  { value: 4, label: '4%' },
  { value: 10, label: '10%' },
  { value: 21, label: '21%' },
];

export default function ProductoModal({ producto, onClose, onSuccess }: ProductoModalProps) {
  const productosService = useProductosService();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const [formData, setFormData] = useState({
    nombre: '',
    descripcion: '',
    precio: '',
    tipo_iva: '21',
    es_servicio: false,
    codigo: '',
    activo: true,
  });

  useEffect(() => {
    if (producto) {
      setFormData({
        nombre: producto.nombre,
        descripcion: producto.descripcion || '',
        precio: producto.precio.toString(),
        tipo_iva: producto.tipo_iva.toString(),
        es_servicio: producto.es_servicio,
        codigo: producto.codigo || '',
        activo: producto.activo,
      });
    }
  }, [producto]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const precio = parseFloat(formData.precio);
      if (isNaN(precio) || precio < 0) {
        throw new Error('El precio debe ser un número válido');
      }

      if (producto) {
        // Update existing producto
        const updateData: ProductoUpdate = {};
        
        if (formData.nombre !== producto.nombre) updateData.nombre = formData.nombre;
        if (formData.descripcion !== (producto.descripcion || '')) {
          updateData.descripcion = formData.descripcion || undefined;
        }
        if (precio !== producto.precio) updateData.precio = precio;
        if (parseFloat(formData.tipo_iva) !== producto.tipo_iva) {
          updateData.tipo_iva = parseFloat(formData.tipo_iva);
        }
        if (formData.es_servicio !== producto.es_servicio) {
          updateData.es_servicio = formData.es_servicio;
        }
        if (formData.codigo !== (producto.codigo || '')) {
          updateData.codigo = formData.codigo || undefined;
        }
        if (formData.activo !== producto.activo) updateData.activo = formData.activo;
        
        if (Object.keys(updateData).length > 0) {
          await productosService.update(producto.id, updateData);
        }
      } else {
        // Create new producto
        const createData: ProductoCreate = {
          nombre: formData.nombre,
          precio: precio,
          ...(formData.descripcion && { descripcion: formData.descripcion }),
          ...(formData.tipo_iva !== '21' && { tipo_iva: parseFloat(formData.tipo_iva) }),
          ...(formData.es_servicio && { es_servicio: formData.es_servicio }),
          ...(formData.codigo && { codigo: formData.codigo }),
          ...(!formData.activo && { activo: formData.activo }),
        };
        await productosService.create(createData);
      }
      
      onSuccess();
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Error al guardar el producto');
      }
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    
    if (type === 'checkbox') {
      const target = e.target as HTMLInputElement;
      setFormData(prev => ({
        ...prev,
        [name]: target.checked,
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value,
      }));
    }
  };

  return (
    <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">
            {producto ? 'Editar Producto' : 'Nuevo Producto'}
          </h3>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="md:col-span-2">
              <label htmlFor="nombre" className="block text-sm font-medium text-gray-700">
                Nombre *
              </label>
              <input
                type="text"
                name="nombre"
                id="nombre"
                required
                value={formData.nombre}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="codigo" className="block text-sm font-medium text-gray-700">
                Código
              </label>
              <input
                type="text"
                name="codigo"
                id="codigo"
                value={formData.codigo}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="precio" className="block text-sm font-medium text-gray-700">
                Precio (€) *
              </label>
              <input
                type="number"
                name="precio"
                id="precio"
                required
                step="0.01"
                min="0"
                value={formData.precio}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="tipo_iva" className="block text-sm font-medium text-gray-700">
                Tipo de IVA
              </label>
              <select
                name="tipo_iva"
                id="tipo_iva"
                value={formData.tipo_iva}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              >
                {IVA_OPTIONS.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="md:col-span-2">
              <label htmlFor="descripcion" className="block text-sm font-medium text-gray-700">
                Descripción
              </label>
              <textarea
                name="descripcion"
                id="descripcion"
                rows={3}
                value={formData.descripcion}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>

            <div className="md:col-span-2 space-y-3">
              <label className="inline-flex items-center">
                <input
                  type="checkbox"
                  name="es_servicio"
                  checked={formData.es_servicio}
                  onChange={handleChange}
                  className="rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                />
                <span className="ml-2 text-sm text-gray-700">Es un servicio</span>
              </label>

              <label className="inline-flex items-center ml-6">
                <input
                  type="checkbox"
                  name="activo"
                  checked={formData.activo}
                  onChange={handleChange}
                  className="rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                />
                <span className="ml-2 text-sm text-gray-700">Activo</span>
              </label>
            </div>
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              disabled={loading}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              {loading ? 'Guardando...' : 'Guardar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}