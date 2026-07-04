import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { api } from '../api'
import { FadeUp } from '../components/FadeUp'
import { Search, ChevronRight, BookOpen, TrendingUp, Globe, Compass, ArrowUpRight, Clock, Sparkles } from 'lucide-react'

const stagger = {
  initial: { opacity: 0, y: 20 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, amount: 0.1 },
  transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] },
}

export default function Home() {
  const [stats, setStats] = useState(null)
  const [recent, setRecent] = useState([])
  const [platforms, setPlatforms] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      api.getStats(),
      api.getProblems({ page_size: 6, sort_by: 'created_at', sort_order: 'desc' }),
      api.getPlatforms(),
    ]).then(([s, p, pl]) => {
      setStats(s)
      setRecent(p.items || [])
      setPlatforms(pl || [])
    }).finally(() => setLoading(false))
  }, [])

  const [showAll, setShowAll] = useState(false)
  const sorted = [...platforms].sort((a, b) => b.total - a.total)

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="w-8 h-8 border-2 border-white/20 border-t-blue-400 rounded-full animate-spin" />
      </div>
    )
  }

  return (
    <div>
      <section
        style={{
          position: 'relative',
          zIndex: 1,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          height: '100vh',
          padding: '70px 32px 32px 32px',
        }}
      >
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'flex-start',
            maxWidth: '720px',
          }}
        >
          <h2
            style={{
              display: 'flex',
              flexWrap: 'wrap',
              gap: '0.25em',
              fontSize: 'clamp(26px, 3vw, 42px)',
              fontWeight: 700,
              lineHeight: 1.08,
              letterSpacing: '-0.01em',
              textTransform: 'uppercase',
              color: '#fff',
              margin: 0,
            }}
          >
            {"WE BUILD END-TO-END AI AUTOMATION SYSTEMS.".split(' ').map((word, i) => (
              <motion.span
                key={i}
                initial={{ opacity: 0, y: 32 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.2 }}
                transition={{
                  duration: 0.7,
                  delay: 0.15 + i * 0.08,
                  ease: [0.22, 1, 0.36, 1],
                }}
              >
                {word}
              </motion.span>
            ))}
          </h2>

          <FadeUp as="p" delay={0.9} y={24} style={{ marginTop: 24, fontSize: 14, lineHeight: 1.65, color: 'rgba(255,255,255,0.85)', maxWidth: 260 }}>
            We provide all-in-one AI automation services in one place.
          </FadeUp>
        </div>

        <style>{`
          @media (max-width: 900px) {
            section:first-child { padding: 90px 18px 32px 18px !important; }
          }
        `}</style>
      </section>

      {stats && (
        <section className="py-14">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[
                { icon: BookOpen, label: 'Total Problems', value: stats.total_problems.toLocaleString() },
                { icon: TrendingUp, label: 'Open Now', value: stats.open_problems },
                { icon: Globe, label: 'Platforms', value: stats.platforms },
                { icon: Compass, label: 'Domains', value: stats.domains },
              ].map((item, i) => (
                <motion.div
                  key={item.label}
                  {...stagger}
                  transition={{ ...stagger.transition, delay: i * 0.08 }}
                  className="bg-slate-900/60 backdrop-blur-xl rounded-xl border border-white/10 p-4"
                >
                  <div className="w-9 h-9 rounded-lg bg-blue-500/20 flex items-center justify-center mb-3">
                    <item.icon className="w-4 h-4 text-blue-400" />
                  </div>
                  <div className="text-2xl font-bold text-white tracking-tight">{item.value}</div>
                  <div className="text-sm text-slate-400 mt-0.5">{item.label}</div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>
      )}

      <section className="py-14">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <FadeUp className="mb-8">
            <h2 className="text-2xl font-bold text-white tracking-tight">Explore by Platform</h2>
            <p className="text-slate-400 text-sm mt-1">{platforms.length} leading hackathon platforms</p>
          </FadeUp>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
            {sorted.slice(0, showAll ? sorted.length : 5).map((p, i) => (
              <motion.div
                key={p.name}
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.1 }}
                transition={{ duration: 0.5, delay: i * 0.06, ease: [0.22, 1, 0.36, 1] }}
              >
                <Link
                  to={`/problems?platform=${encodeURIComponent(p.name)}`}
                  className="block bg-slate-900/60 backdrop-blur-xl rounded-xl border border-white/10 p-3.5 hover:border-blue-500/50 hover:-translate-y-0.5 transition-all"
                >
                  <div className="text-sm font-semibold text-white leading-tight truncate">{p.name}</div>
                  <div className="text-xs text-slate-400 mt-1 tabular-nums">{p.total.toLocaleString()} problems</div>
                  {p.open > 0 && <div className="text-xs text-emerald-400 font-medium mt-0.5">{p.open} active</div>}
                </Link>
              </motion.div>
            ))}
          </div>
          {sorted.length > 5 && (
            <motion.button
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.3 }}
              onClick={() => setShowAll(!showAll)}
              className="mt-4 w-full py-2.5 text-sm font-medium text-blue-400 hover:text-blue-300 hover:bg-white/5 rounded-lg transition-colors border border-dashed border-white/10"
            >
              {showAll ? 'Show less' : `View all ${sorted.length} platforms`}
            </motion.button>
          )}
        </div>
      </section>

      {recent.length > 0 && (
        <section className="py-14">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-end justify-between mb-8">
              <FadeUp>
                <h2 className="text-2xl font-bold text-white tracking-tight">Recently Added</h2>
                <p className="text-slate-400 text-sm mt-1">Latest problem statements from across platforms</p>
              </FadeUp>
              <Link
                to="/problems"
                className="hidden sm:flex items-center gap-1 text-sm font-medium text-blue-400 hover:text-blue-300 transition-colors"
              >
                View all <ArrowUpRight className="w-3.5 h-3.5" />
              </Link>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {recent.map((p, i) => (
                <motion.div
                  key={p.id}
                  initial={{ opacity: 0, y: 16 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, amount: 0.1 }}
                  transition={{ duration: 0.5, delay: i * 0.08, ease: [0.22, 1, 0.36, 1] }}
                  className="bg-slate-900/60 backdrop-blur-xl rounded-xl border border-white/10 p-5 hover:border-white/20 transition-all"
                >
                  <div className="flex items-center gap-2 text-xs text-slate-400 mb-2">
                    <Clock className="w-3 h-3" />
                    <span>{p.source_platform || 'General'}</span>
                    {p.source_year && <><span>·</span><span>{p.source_year}</span></>}
                  </div>
                  <h3 className="font-semibold text-white truncate">{p.title}</h3>
                  <p className="text-sm text-slate-300 mt-1.5 line-clamp-2 leading-relaxed">{p.description}</p>
                  <div className="flex flex-wrap gap-1.5 mt-3">
                    {p.domain && <span className="px-2 py-0.5 bg-blue-500/20 text-blue-300 rounded text-xs font-medium">{p.domain}</span>}
                    {p.difficulty && <span className="px-2 py-0.5 bg-white/5 text-slate-400 rounded text-xs">{p.difficulty}</span>}
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>
      )}

      <section className="py-14">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <FadeUp className="bg-slate-900/60 backdrop-blur-xl rounded-2xl p-8 md:p-12 text-center border border-white/10">
            <h2 className="text-2xl font-bold text-white mb-3">Ready to find your next project?</h2>
            <p className="text-slate-400 max-w-md mx-auto mb-8 text-sm">
              Browse thousands of problem statements from the best hackathon platforms, all in one place.
            </p>
            <Link
              to="/problems"
              className="inline-flex items-center gap-2 bg-blue-500 text-white px-6 py-2.5 rounded-lg font-semibold text-sm hover:bg-blue-600 transition-colors"
            >
              <Search className="w-4 h-4" />
              Browse All Problems
            </Link>
          </FadeUp>
        </div>
      </section>
    </div>
  )
}
