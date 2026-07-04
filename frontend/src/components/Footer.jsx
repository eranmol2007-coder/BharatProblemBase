import { Link } from 'react-router-dom'
import Logo from './Logo'

export default function Footer() {
  return (
    <footer className="bg-slate-900/60 backdrop-blur-xl border-t border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div className="col-span-2 md:col-span-1">
            <Link to="/" className="flex items-center gap-2 text-white font-semibold mb-3">
              <Logo size={20} />
              BharatProblemBase
            </Link>
            <p className="text-sm leading-relaxed text-slate-400">
              Your one-stop platform for discovering hackathon and competition problem statements from across India.
            </p>
          </div>

          <div>
            <h4 className="text-white text-sm font-semibold mb-3">Navigate</h4>
            <ul className="space-y-2 text-sm">
              {[
                { to: '/', label: 'Home' },
                { to: '/problems', label: 'Browse Problems' },
                { to: '/help', label: 'Help' },
                { to: '/about', label: 'About' },
              ].map(l => (
                <li key={l.to}>
                  <Link to={l.to} className="text-slate-400 hover:text-white transition-colors">{l.label}</Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-white text-sm font-semibold mb-3">Platforms</h4>
            <ul className="space-y-2 text-sm">
              {['Smart India Hackathon', 'Unstop', 'Devfolio', 'HackerEarth', 'MLH'].map(p => (
                <li key={p} className="text-slate-500">{p}</li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-white text-sm font-semibold mb-3">More</h4>
            <ul className="space-y-2 text-sm">
              <li className="text-slate-500">&copy; {new Date().getFullYear()} BharatProblemBase</li>
              <li className="text-slate-500">Built with care</li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  )
}
