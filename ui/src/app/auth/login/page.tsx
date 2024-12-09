import { Button } from '@/components/ui/button';
import {
  RegisterLink,
  LoginLink,
} from '@kinde-oss/kinde-auth-nextjs/components';
import React from 'react';
import { LogIn } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

const LoginPage = async () => (
  <Card>
    <CardContent
      className={`flex h-64 w-96 flex-col items-center justify-between p-10`}
    >
      <LoginLink className={`w-full`}>
        <Button size={'lg'} className={`h-20 w-full`}>
          <LogIn className={'mr-2'} />
          Sign in
        </Button>
      </LoginLink>
      or
      <RegisterLink>
        <Button variant={'secondary'} size={'lg'}>
          Sign up
        </Button>
      </RegisterLink>
    </CardContent>
  </Card>
);

export default LoginPage;