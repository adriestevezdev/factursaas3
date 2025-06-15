import { useAuth } from '@clerk/nextjs';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export function useApiClient() {
  const { getToken } = useAuth();

  const getAuthHeaders = async (): Promise<Record<string, string>> => {
    const token = await getToken();
    
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  };

  const apiCall = async <T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> => {
    const headers = await getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        ...headers,
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  };

  return {
    get: <T>(endpoint: string) => apiCall<T>(endpoint, { method: 'GET' }),
    post: <T>(endpoint: string, data: any) =>
      apiCall<T>(endpoint, {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    put: <T>(endpoint: string, data: any) =>
      apiCall<T>(endpoint, {
        method: 'PUT',
        body: JSON.stringify(data),
      }),
    delete: <T>(endpoint: string) => apiCall<T>(endpoint, { method: 'DELETE' }),
  };
}