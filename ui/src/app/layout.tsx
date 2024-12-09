import { RootProviders } from '@/app/providers';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import React from 'react';

import '@/assets/globals.css';

// If loading a variable font, you don't need to specify the font weight
const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
});

export const metadata: Metadata = {
  title: {
    default: `Algorythmix`,
    template: `%s | Algorythmix`,
  },
  icons: {
    icon: {
      url: '/favicon.ico',},
  },
};

interface Props {
  children: Readonly<React.ReactNode>;
}

const RootLayout = async ({ children }: Props) => (
  <html lang="en" suppressHydrationWarning>
    <body className={`${inter.className} antialiased`}>
      <RootProviders>{children}</RootProviders>
    </body>
  </html>
);

export default RootLayout;