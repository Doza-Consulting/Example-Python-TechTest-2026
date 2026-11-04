/**
 * Thin client for the EscapeQueue API. All calls use relative /api/... URLs
 * (proxied by Vite locally, routed by CloudFront when deployed).
 */

export interface Room {
  id: string;
  name: string;
  theme: string;
  minPartySize: number;
  maxPartySize: number;
  durationMinutes: number;
}

async function getJson<T>(path: string): Promise<T> {
  const res = await fetch(`/api${path}`);
  if (!res.ok) throw new Error(`${path} failed with ${res.status}`);
  return res.json() as Promise<T>;
}

export const getHealth = () => getJson<{ status: string }>("/health");

export const getRooms = async () =>
  (await getJson<{ data: Room[] }>("/rooms")).data;
