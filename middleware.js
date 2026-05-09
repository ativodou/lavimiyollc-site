export const config = {
  matcher: '/((?!_vercel).*)',
}

export default function middleware(request) {
  const auth = request.headers.get('authorization')

  if (auth && auth.startsWith('Basic ')) {
    const password = atob(auth.slice(6)).split(':').slice(1).join(':')
    if (password === process.env.SITE_PASSWORD) {
      return // correct password — serve the page
    }
  }

  return new Response('Access denied', {
    status: 401,
    headers: {
      'WWW-Authenticate': 'Basic realm="LavimiyòLLC"',
    },
  })
}
