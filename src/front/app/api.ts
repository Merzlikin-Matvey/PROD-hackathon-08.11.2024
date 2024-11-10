export async function fetchTours() {
  const response = await fetch('/api/tours', {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  if (!response.ok) {
    throw new Error('Failed to fetch tours');
  }
  const data = await response.json();
  return data.tours;
}