const API_BASE = '/api';

async function fetchJSON(url, options = {}) {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  if (res.status === 204) return null;
  return res.json();
}

async function fetchWithFallback(url, fallbackPages) {
  try {
    return await fetchJSON(url);
  } catch (e) {
    if (e.message.includes('422') && fallbackPages.length > 0) {
      const next = fallbackPages[0];
      const fallbackUrl = url.replace(/page_size=\d+/, `page_size=${next}`);
      return fetchWithFallback(fallbackUrl, fallbackPages.slice(1));
    }
    throw e;
  }
}

export const api = {
  getProblems: (params = {}) => {
    const q = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => { if (v !== undefined && v !== null && v !== '') q.set(k, v); });
    const url = `/problems?${q}`;
    return fetchWithFallback(url, [100, 50, 20]);
  },
  getProblem: (id) => fetchJSON(`/problems/${id}`),
  createProblem: (data) => fetchJSON('/problems', { method: 'POST', body: JSON.stringify(data) }),
  updateProblem: (id, data) => fetchJSON(`/problems/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteProblem: (id) => fetchJSON(`/problems/${id}`, { method: 'DELETE' }),
  getPlatforms: () => fetchJSON('/problems/platforms'),
  getDomains: () => fetchJSON('/problems/domains'),
  getStats: () => fetchJSON('/problems/stats'),
  triggerScrape: () => fetchJSON('/problems/scrape', { method: 'POST' }),
  health: () => fetchJSON('/health'),
};
