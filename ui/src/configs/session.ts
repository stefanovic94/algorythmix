const secretKey = process.env.SESSION_SECRET ?? 'mySecret';

export const sessionConfig = {
  name: 'algorythmix_session',
  secretKey,
  lifetime: 7 * 24 * 60 * 60 * 1000,
};

export default sessionConfig;