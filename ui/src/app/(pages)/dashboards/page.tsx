import { Metadata } from 'next';
import React from 'react';
import ProfilePopover from '@/components/layout/auth/ProfilePopover';

export const metadata: Metadata = {
    title: 'Dashboards',
};

const DashboardPage = async () => {
    return (
        <div>
            <ProfilePopover />
        </div>
    );
};

export default DashboardPage;