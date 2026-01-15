import { Link, useLocation } from 'react-router-dom'

export default function Navbar() {
  const location = useLocation()

  return (
    <nav className="bg-gradient-to-r from-zinc-900/90 via-zinc-900/95 to-zinc-900/90 border-b border-zinc-800/50 backdrop-blur-xl sticky top-0 z-50 shadow-lg shadow-black/20">
      <div className="max-w-7xl mx-auto px-8 py-5 flex items-center justify-between">
        <Link to="/" className="group flex items-center gap-3 text-xl font-bold text-white">
          <div className="p-2 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg shadow-lg shadow-blue-500/30 group-hover:shadow-blue-500/50 transition-all duration-300 group-hover:scale-110">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" className="text-white">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
            </svg>
          </div>
          <span className="bg-gradient-to-r from-white to-zinc-300 bg-clip-text text-transparent group-hover:from-blue-400 group-hover:to-blue-200 transition-all duration-300">
            PaperVault
          </span>
        </Link>
        
        <div className="flex items-center gap-2">
          <Link
            to="/"
            className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
              location.pathname === '/'
                ? 'bg-zinc-800 text-white shadow-md'
                : 'text-zinc-400 hover:text-white hover:bg-zinc-800/50'
            }`}
          >
            Upload
          </Link>
          <Link
            to="/search"
            className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
              location.pathname === '/search'
                ? 'bg-zinc-800 text-white shadow-md'
                : 'text-zinc-400 hover:text-white hover:bg-zinc-800/50'
            }`}
          >
            Search
          </Link>
          
          <div className="h-8 w-px bg-zinc-700/50 mx-2"></div>
          
          <Link
            to="/login"
            className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
              location.pathname === '/login'
                ? 'bg-zinc-800 text-white shadow-md'
                : 'text-zinc-400 hover:text-white hover:bg-zinc-800/50'
            }`}
          >
            Login
          </Link>
          <Link
            to="/register"
            className={`px-5 py-2 rounded-lg font-medium transition-all duration-300 ${
              location.pathname === '/register'
                ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-lg shadow-blue-500/30'
                : 'bg-gradient-to-r from-blue-500/90 to-blue-600/90 text-white hover:from-blue-500 hover:to-blue-600 shadow-md shadow-blue-500/20 hover:shadow-lg hover:shadow-blue-500/30'
            }`}
          >
            Register
          </Link>
        </div>
      </div>
    </nav>
  )
}
