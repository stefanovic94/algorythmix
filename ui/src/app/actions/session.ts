'use server';

import sessionConfig from '@/configs/session';

import { JWTPayload, jwtVerify, SignJWT } from 'jose';
import { cookies } from 'next/headers';

const encodedKey = new TextEncoder().encode(sessionConfig.secretKey);

export interface SessionPayload extends JWTPayload {
  theme: {
    mode: 'light' | 'dark' | 'system';
  };
}

const defaultSessionValues: SessionPayload = { theme: { mode: 'system' } };

export const encrypt = async (payload: SessionPayload) =>
  new SignJWT(payload)
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('7d')
    .sign(encodedKey);

export const decrypt = async (session: string | undefined = '') => {
  try {
    const { payload } = await jwtVerify(session, encodedKey, {
      algorithms: ['HS256'],
    });
    return payload as SessionPayload;
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
  } catch (error) {
    return null;
  }
};

export const setSession = async (
  payload: SessionPayload = defaultSessionValues,
) => {
  const expiresAt = new Date(Date.now() + sessionConfig.lifetime);
  const session = await encrypt({ ...payload, expiresAt });
  (await cookies()).set(sessionConfig.name, session, {
    httpOnly: true,
    secure: true,
    expires: expiresAt,
    sameSite: 'lax',
    path: '/',
  });
  return payload;
};

export const deleteSession = async () => {
  (await cookies()).delete(sessionConfig.name);
};

export const getSession = async () => {
  const cookie = (await cookies()).get(sessionConfig.name)?.value;
  return await decrypt(cookie);
};