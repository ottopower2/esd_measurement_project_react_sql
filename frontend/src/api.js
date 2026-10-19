async function request(path, options = {}) {
  const response = await fetch(path, options);
  if (!response.ok) {
    let message;
    try {
      const error = await response.json();
      message = error.detail || JSON.stringify(error);
    } catch {
      message = await response.text();
    }
    throw new Error(message || `HTTP ${response.status}`);
  }
  return response.status === 204 ? null : response.json();
}

export const api = {
  createMeasurement: (payload) =>
    request('/esd/measurement', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }),
  listMeasurements: () => request('/measurements'),
  getMeasurement: (id) => request(`/measurements/${id}`),
  deleteMeasurement: (id) =>
    request(`/measurements/${id}`, { method: 'DELETE' }),
  screenshotUrl: (id) => `/measurements/${id}/screenshot`,
};
