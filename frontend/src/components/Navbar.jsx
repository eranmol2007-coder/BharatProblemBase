import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Menu, X, Search, HelpCircle } from 'lucide-react'
import Logo from './Logo'

const links = [
  { to: '/', label: 'Home' },
  { to: '/problems', label: 'Problems' },
  { to: '/help', label: 'Help' },
  { to: '/about', label: 'About' },
]

export default function Navbar() {
  const [open, setOpen] = useState(false)
  const { pathname } = useLocation()

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/80 backdrop-blur-xl border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2.5">
            <Logo size={32} />
            <span className="text-lg font-bold text-white">BharatProblemBase</span>
          </Link>

          <div className="hidden md:flex items-center gap-1">
            {links.map(l => (
              <Link
                key={l.to}
                to={l.to}
                className={`px-3.5 py-2 rounded-lg text-sm font-medium transition-colors ${
                  pathname === l.to
                    ? 'bg-white/10 text-white'
                    : 'text-slate-400 hover:text-white hover:bg-white/5'
                }`}
              >
                {l.label}
              </Link>
            ))}
            <div className="w-px h-5 bg-white/10 mx-2" />
            <Link
              to="/problems"
              className="flex items-center gap-1.5 bg-blue-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-600 transition-colors"
            >
              <Search className="w-4 h-4" />
              Browse Problems
            </Link>
          </div>

          <button
            className="md:hidden p-2 rounded-lg text-slate-400 hover:bg-white/5"
            onClick={() => setOpen(!open)}
          >
            {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>

        {open && (
          <div className="md:hidden pb-4 space-y-1">
            {links.map(l => (
              <Link
                key={l.to}
                to={l.to}
                onClick={() => setOpen(false)}
                className={`block px-3 py-2 rounded-lg text-sm font-medium ${
                  pathname === l.to
                    ? 'bg-white/10 text-white'
                    : 'text-slate-400 hover:text-white hover:bg-white/5'
                }`}
              >
                {l.label}
              </Link>
            ))}
            <Link
              to="/problems"
              onClick={() => setOpen(false)}
              className="flex items-center gap-1.5 bg-blue-500 text-white px-3 py-2 rounded-lg text-sm font-medium mt-2"
            >
              <Search className="w-4 h-4" />
              Browse Problems
            </Link>
          </div>
        )}
      </div>
    </nav>
  )
}
