'use client';

import { useState, useEffect } from 'react';
import AppLayout from '@/components/AppLayout';
import { useProductosService } from '@/services/productos';
import { Producto } from '@/types';
import ProductoModal from './ProductoModal';

export default function Productos() {
  const [productos, setProductos] = useState<Producto[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedProducto, setSelectedProducto] = useState<Producto | null>(null);
  const [mostrarInactivos, setMostrarInactivos] = useState(false);
  const productosService = useProductosService();

  const fetchProductos = async () => {
    try {
      setLoading(true);
      const data = await productosService.getAll(0, 100, !mostrarInactivos);
      setProductos(data);
    } catch (err) {
      setError('Error al cargar los productos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProductos();
  }, [mostrarInactivos]);

  const handleCreate = () => {
    setSelectedProducto(null);
    setIsModalOpen(true);
  };

  const handleEdit = (producto: Producto) => {
    setSelectedProducto(producto);
    setIsModalOpen(true);
  };

  const handleDelete = async (id: number) => {
    if (confirm('¿Estás seguro de eliminar este producto?')) {
      try {
        await productosService.delete(id);
        await fetchProductos();
      } catch (err) {
        alert('Error al eliminar el producto');
        console.error(err);
      }
    }
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setSelectedProducto(null);
  };

  const handleModalSuccess = async () => {
    await fetchProductos();
    handleModalClose();
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR',
    }).format(value);
  };

  if (loading) {
    return (
      <AppLayout>
        <div className="flex justify-center items-center h-64">
          <div className="text-gray-500">Cargando...</div>
        </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <div className="px-4 py-6 sm:px-0">
        <div className="border-b border-gray-200 pb-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold leading-tight text-gray-900">
                Productos y Servicios
              </h1>
              <p className="mt-2 max-w-4xl text-sm text-gray-500">
                Gestiona tu catálogo de productos y servicios
              </p>
            </div>
            <button
              onClick={handleCreate}
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition duration-150 ease-in-out"
            >
              Nuevo Producto
            </button>
          </div>
          
          <div className="mt-4">
            <label className="inline-flex items-center">
              <input
                type="checkbox"
                className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
                checked={mostrarInactivos}
                onChange={(e) => setMostrarInactivos(e.target.checked)}
              />
              <span className="ml-2 text-sm text-gray-600">Mostrar productos inactivos</span>
            </label>
          </div>
        </div>

        {error && (
          <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        <div className="mt-8">
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Código
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Nombre
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Tipo
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Precio
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    IVA
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Estado
                  </th>
                  <th className="relative px-6 py-3">
                    <span className="sr-only">Acciones</span>
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {productos.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="px-6 py-4 text-center text-gray-500">
                      No hay productos registrados
                    </td>
                  </tr>
                ) : (
                  productos.map((producto) => (
                    <tr key={producto.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {producto.codigo || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        <div>
                          <div>{producto.nombre}</div>
                          {producto.descripcion && (
                            <div className="text-xs text-gray-500">{producto.descripcion}</div>
                          )}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          producto.es_servicio 
                            ? 'bg-purple-100 text-purple-800' 
                            : 'bg-green-100 text-green-800'
                        }`}>
                          {producto.es_servicio ? 'Servicio' : 'Producto'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {formatCurrency(producto.precio)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {producto.tipo_iva}%
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          producto.activo 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {producto.activo ? 'Activo' : 'Inactivo'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button
                          onClick={() => handleEdit(producto)}
                          className="text-indigo-600 hover:text-indigo-900 mr-4"
                        >
                          Editar
                        </button>
                        <button
                          onClick={() => handleDelete(producto.id)}
                          className="text-red-600 hover:text-red-900"
                        >
                          Eliminar
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {isModalOpen && (
        <ProductoModal
          producto={selectedProducto}
          onClose={handleModalClose}
          onSuccess={handleModalSuccess}
        />
      )}
    </AppLayout>
  );
}