import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { motion, useScroll, useTransform } from 'framer-motion'
import { api } from '../api'
import { FadeUp } from '../components/FadeUp'
import HeroAnimation from '../components/HeroAnimation'
import { Search, BookOpen, TrendingUp, Globe, Compass, ArrowUpRight, Clock, Sparkles } from 'lucide-react'

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
  const { scrollY } = useScroll()
  const heroY = useTransform(scrollY, [0, 500], [0, 150])
  const heroOpacity = useTransform(scrollY, [0, 400], [1, 0])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="w-8 h-8 border-2 border-slate-200 border-t-cyan-500 rounded-full animate-spin" />
      </div>
    )
  }

  return (
    <div>
      {/* Full-screen Hero with 3D Text */}
      <motion.section
        style={{ y: heroY, opacity: heroOpacity }}
        className="relative min-h-screen flex items-center overflow-hidden pt-20"
      >
        {/* Subtle overlay for text readability */}
        <div className="absolute inset-0 bg-gradient-to-b from-white/40 via-white/20 to-white/50" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full relative z-10 grid grid-cols-1 lg:grid-cols-2 gap-12 items-center py-20">
          
          {/* Left Column - 3D Floating Text */}
          <div style={{ perspective: '1000px' }}>
            <motion.div
              initial={{ opacity: 0, rotateY: -15, translateZ: -100 }}
              animate={{ opacity: 1, rotateY: 0, translateZ: 0 }}
              transition={{ duration: 1, ease: [0.22, 1, 0.36, 1] }}
              style={{ transformStyle: 'preserve-3d' }}
            >
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-cyan-50 border border-cyan-200 text-cyan-700 text-sm font-medium mb-6 shadow-[0_4px_20px_rgba(6,182,212,0.15)]" style={{ transform: 'translateZ(40px)' }}>
                <Sparkles className="w-4 h-4" />
                <span>Over 100,000+ Problem Statements</span>
              </div>
            </motion.div>
            
            <motion.h1
              initial={{ opacity: 0, rotateY: -20, translateZ: -150 }}
              animate={{ opacity: 1, rotateY: 0, translateZ: 0 }}
              transition={{ duration: 1.2, delay: 0.1, ease: [0.22, 1, 0.36, 1] }}
              className="text-5xl lg:text-7xl font-bold text-slate-900 tracking-tight mb-6 leading-[1.1]"
              style={{ transformStyle: 'preserve-3d', transform: 'translateZ(60px)', textShadow: '0 2px 8px rgba(0,0,0,0.1), 0 20px 40px rgba(0,0,0,0.06)' }}
            >
              Discover Your Next <br />
              Hackathon Project
            </motion.h1>
            
            <motion.p
              initial={{ opacity: 0, rotateY: -15, translateZ: -80 }}
              animate={{ opacity: 1, rotateY: 0, translateZ: 0 }}
              transition={{ duration: 1, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
              className="text-lg text-slate-600 mb-8 max-w-xl leading-relaxed"
              style={{ transform: 'translateZ(30px)' }}
            >
              BharatProblemBase aggregates problem statements from Smart India Hackathon, Unstop, Devfolio, and more. Stop searching, start building.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, rotateY: -10, translateZ: -50 }}
              animate={{ opacity: 1, rotateY: 0, translateZ: 0 }}
              transition={{ duration: 0.8, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
              className="flex flex-wrap items-center gap-4"
              style={{ transform: 'translateZ(50px)' }}
            >
              <Link to="/problems" className="bg-cyan-500 hover:bg-cyan-600 text-white px-8 py-3.5 rounded-full font-semibold transition-all shadow-[0_10px_30px_-10px_rgba(6,182,212,0.5)] hover:shadow-[0_15px_40px_-10px_rgba(6,182,212,0.6)] hover:-translate-y-0.5 flex items-center gap-2">
                <Search className="w-5 h-5" />
                Browse Problems
              </Link>
              <Link to="/help" className="bg-white/80 hover:bg-white border border-slate-200 text-slate-700 px-8 py-3.5 rounded-full font-semibold transition-all hover:-translate-y-0.5 flex items-center gap-2 shadow-sm">
                <BookOpen className="w-5 h-5" />
                How it works
              </Link>
            </motion.div>
          </div>

          {/* Right Column - 3D Network Animation */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8, rotateY: 20 }}
            animate={{ opacity: 1, scale: 1, rotateY: 0 }}
            transition={{ duration: 1.5, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
            className="relative h-[400px] lg:h-[500px] w-full hidden sm:flex justify-center items-center"
            style={{ perspective: '1200px', transformStyle: 'preserve-3d' }}
          >
            <HeroAnimation />
            {/* 3D Floating accent shapes */}
            <motion.div
              animate={{ y: [-10, 10, -10], rotateX: [5, -5, 5], rotateY: [-5, 5, -5] }}
              transition={{ duration: 6, ease: "easeInOut", repeat: Infinity }}
              className="absolute top-10 right-10 w-20 h-20 bg-white/70 backdrop-blur-md border border-cyan-200/50 rounded-2xl shadow-[0_8px_30px_rgba(0,0,0,0.08)]"
              style={{ transform: 'translateZ(60px)' }}
            />
            <motion.div
              animate={{ y: [8, -8, 8], rotateX: [-3, 3, -3], rotateY: [3, -3, 3] }}
              transition={{ duration: 8, ease: "easeInOut", repeat: Infinity }}
              className="absolute bottom-16 left-8 w-28 h-28 bg-white/70 backdrop-blur-xl border border-cyan-200/50 rounded-full shadow-[0_8px_30px_rgba(0,0,0,0.08)]"
              style={{ transform: 'translateZ(40px)' }}
            />
            <motion.div
              animate={{ y: [-6, 6, -6], x: [-4, 4, -4], rotateZ: [0, 10, 0] }}
              transition={{ duration: 7, ease: "easeInOut", repeat: Infinity }}
              className="absolute top-1/2 right-4 w-14 h-14 bg-white/70 backdrop-blur-md border border-slate-200/50 rounded-xl shadow-[0_8px_30px_rgba(0,0,0,0.08)]"
              style={{ transform: 'translateZ(80px)' }}
            />
          </motion.div>
        </div>

        {/* Scroll indicator */}
        <motion.div
          animate={{ y: [0, 8, 0] }}
          transition={{ duration: 2, ease: "easeInOut", repeat: Infinity }}
          className="absolute bottom-8 left-1/2 -translate-x-1/2 z-10"
        >
          <div className="w-6 h-10 rounded-full border-2 border-slate-300 flex justify-center pt-2">
            <div className="w-1 h-2 rounded-full bg-cyan-500" />
          </div>
        </motion.div>
      </motion.section>

      {/* About Section with 3D Image */}
      <section className="py-20 relative border-t border-white/[0.08] bg-white/[0.03]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center" style={{ perspective: '1200px' }}>
            <motion.div
              initial={{ opacity: 0, x: -40, rotateY: 10 }}
              whileInView={{ opacity: 1, x: 0, rotateY: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
              style={{ transformStyle: 'preserve-3d' }}
            >
              <h2 className="text-3xl font-bold text-slate-900 tracking-tight mb-5" style={{ transform: 'translateZ(30px)' }}>Why BharatProblemBase?</h2>
              <p className="text-slate-500 leading-relaxed mb-6 text-lg" style={{ transform: 'translateZ(20px)' }}>
                Every year, thousands of problem statements are released across various hackathons, coding competitions, and hiring challenges. Navigating through multiple platforms to find the perfect problem to solve can be overwhelming.
              </p>
              <p className="text-slate-500 leading-relaxed mb-8 text-lg" style={{ transform: 'translateZ(15px)' }}>
                We've built a centralized repository that scrapes, categorizes, and organizes problems from platforms like SIH, Unstop, Devfolio, and more, saving you hours of research so you can focus on what matters most: <strong className="text-slate-900">Building solutions.</strong>
              </p>
              <ul className="space-y-4">
                {['Real-time scraping from 10+ platforms', 'Advanced filtering by domain & difficulty', 'Open-source and community-driven'].map((item, i) => (
                  <motion.li
                    key={i}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: i * 0.1 }}
                    className="flex items-center gap-3 text-base text-slate-600"
                    style={{ transform: `translateZ(${20 - i * 5}px)` }}
                  >
                    <div className="w-8 h-8 rounded-full bg-cyan-100 flex items-center justify-center shrink-0 shadow-sm">
                      <div className="w-2.5 h-2.5 rounded-full bg-cyan-500" />
                    </div>
                    {item}
                  </motion.li>
                ))}
              </ul>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 40, rotateY: -15 }}
              whileInView={{ opacity: 1, x: 0, rotateY: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 1, delay: 0.2 }}
              className="relative h-full min-h-[300px] lg:min-h-[400px]"
              style={{ perspective: '1000px' }}
            >
              <motion.div
                whileHover={{ rotateY: 5, rotateX: -3, scale: 1.02 }}
                transition={{ duration: 0.4 }}
                className="absolute inset-0 rounded-3xl border border-slate-200 overflow-hidden shadow-[0_20px_60px_-15px_rgba(0,0,0,0.1)]"
                style={{ transformStyle: 'preserve-3d', transform: 'translateZ(40px)' }}
              >
                 <img src="/about_graphic.png" alt="Platform Illustration" className="w-full h-full object-cover hue-rotate-[160deg] saturate-150" />
                 <div className="absolute inset-0 bg-gradient-to-t from-white/80 via-transparent to-transparent pointer-events-none"></div>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </section>

      {stats && (
        <section className="py-14">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8" style={{ perspective: '1200px' }}>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[
                { icon: BookOpen, label: 'Total Problems', value: stats.total_problems.toLocaleString() },
                { icon: TrendingUp, label: 'Open Now', value: stats.open_problems },
                { icon: Globe, label: 'Platforms', value: stats.platforms },
                { icon: Compass, label: 'Domains', value: stats.domains },
              ].map((item, i) => (
                <motion.div
                  key={item.label}
                  initial={{ opacity: 0, y: 40, rotateX: 15 }}
                  whileInView={{ opacity: 1, y: 0, rotateX: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: i * 0.08, ease: [0.22, 1, 0.36, 1] }}
                  whileHover={{ y: -8, rotateX: -3, scale: 1.02 }}
                  className="bg-white rounded-2xl border border-slate-200 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.06)] p-6 flex flex-col items-center text-center cursor-default"
                  style={{ transformStyle: 'preserve-3d', transform: `translateZ(${20 + i * 10}px)` }}
                >
                  <div className="w-12 h-12 rounded-full bg-cyan-50 flex items-center justify-center mb-4 shadow-sm" style={{ transform: 'translateZ(20px)' }}>
                    <item.icon className="w-6 h-6 text-cyan-600" />
                  </div>
                  <div className="text-2xl font-bold text-slate-900 tracking-tight" style={{ transform: 'translateZ(15px)' }}>{item.value}</div>
                  <div className="text-sm text-slate-500 mt-0.5">{item.label}</div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>
      )}

      <section className="py-14">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8" style={{ perspective: '1200px' }}>
          <FadeUp className="mb-8">
            <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Explore by Platform</h2>
            <p className="text-slate-500 text-sm mt-1">{platforms.length} leading hackathon platforms</p>
          </FadeUp>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
            {sorted.slice(0, showAll ? sorted.length : 5).map((p, i) => (
              <motion.div
                key={p.name}
                initial={{ opacity: 0, y: 30, rotateX: 10 }}
                whileInView={{ opacity: 1, y: 0, rotateX: 0 }}
                viewport={{ once: true, amount: 0.1 }}
                transition={{ duration: 0.5, delay: i * 0.06, ease: [0.22, 1, 0.36, 1] }}
                whileHover={{ y: -8, rotateX: -3, scale: 1.03 }}
                style={{ transformStyle: 'preserve-3d' }}
              >
                <Link
                  to={`/problems?platform=${encodeURIComponent(p.name)}`}
                   className="block bg-white rounded-2xl border border-slate-200 p-5 shadow-sm hover:shadow-[0_8px_30px_-6px_rgba(0,0,0,0.1)] transition-all"
                   style={{ transform: `translateZ(${10 + (i % 3) * 10}px)` }}
                >
                  <div className="text-sm font-semibold text-slate-900 leading-tight truncate">{p.name}</div>
                  <div className="text-xs text-slate-400 mt-1 tabular-nums">{p.total.toLocaleString()} problems</div>
                  {p.open > 0 && <div className="text-xs text-emerald-600 font-medium mt-0.5">{p.open} active</div>}
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
              className="mt-4 w-full py-2.5 text-sm font-medium text-cyan-600 hover:text-cyan-700 hover:bg-white/80 rounded-lg transition-colors border border-dashed border-slate-200"
            >
              {showAll ? 'Show less' : `View all ${sorted.length} platforms`}
            </motion.button>
          )}
        </div>
      </section>

      {recent.length > 0 && (
        <section className="py-14">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8" style={{ perspective: '1200px' }}>
            <div className="flex items-end justify-between mb-8">
              <FadeUp>
                <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Recently Added</h2>
                <p className="text-slate-500 text-sm mt-1">Latest problem statements from across platforms</p>
              </FadeUp>
              <Link
                to="/problems"
                className="hidden sm:flex items-center gap-1 text-sm font-medium text-cyan-600 hover:text-cyan-700 transition-colors"
              >
                View all <ArrowUpRight className="w-3.5 h-3.5" />
              </Link>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {recent.map((p, i) => (
                <motion.div
                  key={p.id}
                  initial={{ opacity: 0, y: 40, rotateX: 12 }}
                  whileInView={{ opacity: 1, y: 0, rotateX: 0 }}
                  viewport={{ once: true, amount: 0.1 }}
                  transition={{ duration: 0.6, delay: i * 0.08, ease: [0.22, 1, 0.36, 1] }}
                  whileHover={{ y: -8, rotateX: -2, rotateY: 2, scale: 1.01 }}
                  className="bg-white rounded-2xl border border-slate-200 p-7 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.06)] hover:shadow-[0_12px_40px_-8px_rgba(0,0,0,0.12)] transition-shadow cursor-default"
                  style={{ transformStyle: 'preserve-3d', transform: `translateZ(${10 + (i % 3) * 15}px)` }}
                >
                  <div className="flex items-center gap-2 text-xs text-cyan-600 mb-3 font-medium" style={{ transform: 'translateZ(15px)' }}>
                    <Clock className="w-3 h-3" />
                    <span>{p.source_platform || 'General'}</span>
                    {p.source_year && <><span>·</span><span>{p.source_year}</span></>}
                  </div>
                  <h3 className="font-semibold text-slate-900 truncate" style={{ transform: 'translateZ(10px)' }}>{p.title}</h3>
                  <p className="text-sm text-slate-500 mt-1.5 line-clamp-2 leading-relaxed">{p.description}</p>
                  <div className="flex flex-wrap gap-1.5 mt-3" style={{ transform: 'translateZ(8px)' }}>
                    {p.domain && <span className="px-2 py-0.5 bg-cyan-50 text-cyan-700 rounded text-xs font-medium">{p.domain}</span>}
                    {p.difficulty && <span className="px-2 py-0.5 bg-slate-100 text-slate-500 rounded text-xs">{p.difficulty}</span>}
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>
      )}

      <section className="py-14">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30, rotateX: 8 }}
            whileInView={{ opacity: 1, y: 0, rotateX: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            whileHover={{ y: -5, scale: 1.005 }}
            className="bg-white/80 backdrop-blur-xl rounded-2xl p-8 md:p-12 text-center border border-slate-200 shadow-[0_8px_40px_-12px_rgba(0,0,0,0.1)]"
            style={{ transformStyle: 'preserve-3d', perspective: '1000px' }}
          >
            <h2 className="text-2xl font-bold text-slate-900 mb-3" style={{ transform: 'translateZ(20px)' }}>Ready to find your next project?</h2>
            <p className="text-slate-500 max-w-md mx-auto mb-8 text-sm" style={{ transform: 'translateZ(10px)' }}>
              Browse thousands of problem statements from the best hackathon platforms, all in one place.
            </p>
            <Link
              to="/problems"
              className="inline-flex items-center gap-2 bg-cyan-500 hover:bg-cyan-600 text-white px-8 py-3.5 rounded-full font-semibold transition-all shadow-[0_10px_20px_-10px_rgba(6,182,212,0.5)] hover:shadow-[0_15px_30px_-10px_rgba(6,182,212,0.6)] hover:-translate-y-0.5"
              style={{ transform: 'translateZ(30px)' }}
            >
              <Search className="w-4 h-4" />
              Browse All Problems
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  )
}
