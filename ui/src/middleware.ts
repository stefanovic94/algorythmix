import 'server-only';
import { deleteSession, getSession, setSession } from '@/app/actions/session';

import { getKindeServerSession } from '@kinde-oss/kinde-auth-nextjs/server';

import { NextRequest, NextResponse } from 'next/server';

const authRoutes = ['/auth/login'];

export const middleware = async (req: NextRequest) => {
  // heck if the current route is protected or public
  const isAuthRoute = authRoutes.includes(req.nextUrl.pathname);

  const { isAuthenticated } = getKindeServerSession();
  const authenticated = await isAuthenticated();

  // Redirect to /logout if the user is authenticated and login route is accessed
  if (authenticated && isAuthRoute) {
    await deleteSession();
    return NextResponse.redirect(new URL('/api/auth/logout', req.nextUrl));
  }

  // Redirect to /login if the user is not authenticated
  if (!authenticated && !isAuthRoute) {
    await deleteSession();
    return NextResponse.redirect(new URL('/auth/login', req.nextUrl));
  }

  if (req.nextUrl.pathname === '/') {
    return NextResponse.redirect(new URL('/dashboards', req.nextUrl));
  }

  if (!(await getSession())) {
    await setSession();
    return NextResponse.next();
  }
};

// Routes Middleware should not run on
export const config = {
  matcher: ['/((?!api|_next/static|_next/image|.*\\.png$).*)'],
};