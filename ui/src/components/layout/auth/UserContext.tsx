'use client';

import { getUser, User as UserProfile } from '@/app/actions/auth';
import React from 'react';

interface UserProfileContextType {
  profile?: UserProfile;
}

const UserContext = React.createContext<UserProfileContextType | undefined>(
  undefined,
);

interface UserProviderProps {
  children: React.ReactNode;
}

export const UserProvider = ({ children }: UserProviderProps) => {
  const [profile, setProfile] = React.useState<UserProfile | undefined>();

  React.useEffect(() => {
    if (!profile) {
      (async () => {
        setProfile(await getUser());
      })();
    }
  }, [profile]);

  return (
    <UserContext.Provider value={{ profile }}>{children}</UserContext.Provider>
  );
};

export const useUser = (): UserProfileContextType => {
  const context = React.useContext(UserContext);
  if (!context) {
    throw new Error('useUserProfile must be used within a UserProfileProvider');
  }
  return context;
};