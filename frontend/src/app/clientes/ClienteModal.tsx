'use client';

import { useState, useEffect } from 'react';
import { Cliente, ClienteCreate, ClienteUpdate } from '@/types';
import { useClientesService } from '@/services/clientes';

interface ClienteModalProps {
  cliente: Cliente | null;
  onClose: () => void;
  onSuccess: () => void;
}

export default function ClienteModal({ cliente, onClose, onSuccess }: ClienteModalProps) {
  const clientesService = useClientesService();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const [formData, setFormData] = useState({
    nombre: '',
    nif: '',
    direccion: '',
    ciudad: '',
    codigo_postal: '',
    pais: 'España',
    email: '',
    telefono: '',
  });

  useEffect(() => {
    if (cliente) {
      setFormData({
        nombre: cliente.nombre,
        nif: cliente.nif || '',
        direccion: cliente.direccion || '',
        ciudad: cliente.ciudad || '',
        codigo_postal: cliente.codigo_postal || '',
        pais: cliente.pais,
        email: cliente.email || '',
        telefono: cliente.telefono || '',
      });
    }
  }, [cliente]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (cliente) {
        // Update existing cliente
        const updateData: ClienteUpdate = {};
        Object.entries(formData).forEach(([key, value]) => {
          if (value !== '' && value !== (cliente as any)[key]) {
            (updateData as any)[key] = value;
          }
        });
        
        if (Object.keys(updateData).length > 0) {
          await clientesService.update(cliente.id, updateData);
        }
      } else {
        // Create new cliente
        const createData: ClienteCreate = {
          nombre: formData.nombre,
          ...(formData.nif && { nif: formData.nif }),
          ...(formData.direccion && { direccion: formData.direccion }),
          ...(formData.ciudad && { ciudad: formData.ciudad }),
          ...(formData.codigo_postal && { codigo_postal: formData.codigo_postal }),
          ...(formData.pais !== 'España' && { pais: formData.pais }),
          ...(formData.email && { email: formData.email }),
          ...(formData.telefono && { telefono: formData.telefono }),
        };
        await clientesService.create(createData);
      }
      
      onSuccess();
    } catch (err) {
      setError('Error al guardar el cliente');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  return (
    <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">
            {cliente ? 'Editar Cliente' : 'Nuevo Cliente'}
          </h3>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
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
              <label htmlFor="nif" className="block text-sm font-medium text-gray-700">
                NIF/CIF
              </label>
              <input
                type="text"
                name="nif"
                id="nif"
                value={formData.nif}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email
              </label>
              <input
                type="email"
                name="email"
                id="email"
                value={formData.email}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="telefono" className="block text-sm font-medium text-gray-700">
                Teléfono
              </label>
              <input
                type="tel"
                name="telefono"
                id="telefono"
                value={formData.telefono}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>

            <div className="md:col-span-2">
              <label htmlFor="direccion" className="block text-sm font-medium text-gray-700">
                Dirección
              </label>
              <input
                type="text"
                name="direccion"
                id="direccion"
                value={formData.direccion}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="ciudad" className="block text-sm font-medium text-gray-700">
                Ciudad
              </label>
              <input
                type="text"
                name="ciudad"
                id="ciudad"
                value={formData.ciudad}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="codigo_postal" className="block text-sm font-medium text-gray-700">
                Código Postal
              </label>
              <input
                type="text"
                name="codigo_postal"
                id="codigo_postal"
                value={formData.codigo_postal}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>

            <div>
              <label htmlFor="pais" className="block text-sm font-medium text-gray-700">
                País
              </label>
              <input
                type="text"
                name="pais"
                id="pais"
                value={formData.pais}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
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