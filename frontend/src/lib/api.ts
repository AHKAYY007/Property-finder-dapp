export async function fetcher(url: Parameters<typeof fetch>["0"]) {
  const resp = await fetch(url);
  return await resp.json();
}
