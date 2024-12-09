'use server';

import { getKindeServerSession } from '@kinde-oss/kinde-auth-nextjs/server';
import { KindeUserBase } from '@kinde-oss/kinde-auth-nextjs/types';

export type User = KindeUserBase;

const getUser = async () => {
  const { getUser } = getKindeServerSession();
  return await getUser();
};

export { getUser };