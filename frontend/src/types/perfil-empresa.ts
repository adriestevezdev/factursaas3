export interface PerfilEmpresa {
  id: number;
  user_id: string;
  nombre: string;
  nif: string;
  direccion?: string;
  codigo_postal?: string;
  ciudad?: string;
  provincia?: string;
  pais: string;
  telefono?: string;
  email?: string;
  web?: string;
  prefijo_factura: string;
  siguiente_numero: string;
  formato_numero: string;
  iban?: string;
  banco?: string;
  texto_legal?: string;
  condiciones_pago?: string;
  created_at: string;
  updated_at?: string;
}

export interface PerfilEmpresaFormData {
  nombre: string;
  nif: string;
  direccion?: string;
  codigo_postal?: string;
  ciudad?: string;
  provincia?: string;
  pais?: string;
  telefono?: string;
  email?: string;
  web?: string;
  prefijo_factura?: string;
  siguiente_numero?: string;
  formato_numero?: string;
  iban?: string;
  banco?: string;
  texto_legal?: string;
  condiciones_pago?: string;
}