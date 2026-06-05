/**
 * API client for the HR Analytics Dashboard backend.
 * Wraps fetch calls to the FastAPI server with error handling.
 */

const API_BASE = import.meta.env.VITE_API_URL || '';

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

/**
 * Generic GET request to the API.
 * @param {string} endpoint — path like "/api/overview"
 * @returns {Promise<any>} parsed JSON response
 */
async function get(endpoint) {
  const url = `${API_BASE}${endpoint}`;

  const response = await fetch(url, {
    method: 'GET',
    headers: { 'Accept': 'application/json' },
  });

  if (!response.ok) {
    throw new ApiError(
      `API request failed: ${response.status} ${response.statusText}`,
      response.status,
    );
  }

  return response.json();
}

/** Dashboard API methods */
const api = {
  getOverview: () => get('/api/overview'),
  getExpectations: () => get('/api/expectations'),
  getSalary: () => get('/api/salary'),
  getTenure: () => get('/api/tenure'),
  getRoles: () => get('/api/roles'),
  getPresentation: async () => {
    const [pres, ben] = await Promise.all([
      get('/api/presentation'),
      get('/api/benefits/presentation-insights')
    ]);
    return { ...pres, benefits_insights: ben };
  },
  getBenefits: async () => {
    const [overview, ranking, matrix] = await Promise.all([
      get('/api/benefits/overview'),
      get('/api/benefits/ranking'),
      get('/api/benefits/matrix')
    ]);
    return { overview, ranking, matrix };
  },
  
  getConfidential: async (password) => {
    const url = `${API_BASE}/api/confidential/employees`;
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'X-Confidential-Auth': password
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new ApiError('Senha inválida', 401);
      }
      throw new ApiError(`API request failed: ${response.status}`, response.status);
    }
    return response.json();
  }
};

export default api;
export { ApiError };
