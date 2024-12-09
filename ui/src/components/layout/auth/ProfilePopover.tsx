'use client';

import { useUser } from '@/components/layout/auth/UserContext';
import { Button } from '@/components/ui/button';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { LogoutLink } from '@kinde-oss/kinde-auth-nextjs';
import { useTheme } from 'next-themes';
import React from 'react';
import { User as UserIcon, SunMoon } from 'lucide-react';
import Image from 'next/image';

const ProfilePopover = () => {
  const { setTheme, resolvedTheme } = useTheme();
  const { profile: userProfile } = useUser();

  return (
    <Popover>
      <PopoverTrigger asChild>
        <div
          className={`cursor-pointer rounded-full ring-1 ring-accent-foreground`}
        >
          {userProfile?.picture ? (
            <div className={`relative h-8 w-8 rounded-full p-1`}>
              <Image
                alt={'my profile'}
                fill={true}
                src={userProfile.picture}
                className="object-cover"
              />
            </div>
          ) : (
            <UserIcon className={`m-1`} />
          )}
        </div>
      </PopoverTrigger>
      <PopoverContent className="flex justify-between" align={'end'}>
        {userProfile && (
          <div>
            Welcome back,
            <div className={`clear-both block font-bold`}>
              {userProfile.given_name}!
            </div>
          </div>
        )}
        <Button
          onClick={() => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')}
          size={'icon'}
          variant={'outline'}
        >
          <SunMoon />
        </Button>
        <LogoutLink className={'ml-2 self-center p-3'}>Log out</LogoutLink>
      </PopoverContent>
    </Popover>
  );
};

export default ProfilePopover;