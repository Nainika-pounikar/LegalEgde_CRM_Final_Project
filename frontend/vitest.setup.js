import { afterAll, beforeAll, vi } from 'vitest';

const jsonResponse = (payload, status = 200) =>
  new Response(JSON.stringify(payload), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });

beforeAll(() => {
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;

  vi.stubGlobal(
    'fetch',
    vi.fn(async (input) => {
      const url = typeof input === 'string' ? input : input?.url || '';

      if (url.includes('/api/')) {
        return jsonResponse([]);
      }

      return jsonResponse({});
    }),
  );
});

afterAll(() => {
  vi.unstubAllGlobals();
});
