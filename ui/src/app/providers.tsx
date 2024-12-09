import { UserProvider } from '@/components/layout/auth/UserContext';
import React from 'react';
import { ThemeProvider } from 'next-themes';

interface Props {
  children: React.ReactNode;
}

export const RootProviders = async ({ children }: Props) => (
  <ThemeProvider attribute="class" enableSystem={true}>
    <UserProvider>{children}</UserProvider>
  </ThemeProvider>
);