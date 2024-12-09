import React from 'react';

interface Props {
  children: Readonly<React.ReactNode>;
}

const DashboardLayout = async ({ children }: Props) => (
  <div className="content-wrapper">{children}</div>
);

export default DashboardLayout;