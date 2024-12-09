import React from 'react';

interface Props {
  children: Readonly<React.ReactNode>;
}

const AuthLayout = async ({ children }: Props) => (
  <div className={`relative bg-[#090f30]`}>
    <main className={`relative flex min-h-screen w-full flex-col items-center`}>
      {children}
    </main>
  </div>
);

export default AuthLayout;