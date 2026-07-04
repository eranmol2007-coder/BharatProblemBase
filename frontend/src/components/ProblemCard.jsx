import { useState } from 'react'
import { motion } from 'framer-motion'
import { ChevronDown, ChevronUp, ExternalLink, Building2, Globe, Calendar } from 'lucide-react'

const difficultyColors = {
  Beginner: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
  Intermediate: 'bg-amber-500/20 text-amber-300 border-amber-500/30',
  Advanced: 'bg-rose-500/20 text-rose-300 border-rose-500/30',
}

export default function ProblemCard({ problem }) {
  const [open, setOpen] = useState(false)

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.1 }}
      transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      className="bg-slate-900/60 backdrop-blur-xl rounded-xl border border-white/10 hover:border-white/20 transition-all"
    >
      <div className="p-5">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 text-xs text-slate-400 mb-1.5">
              <span>{problem.source_platform || 'General'}</span>
              {problem.source_year && <><span>·</span><span>{problem.source_year}</span></>}
            </div>
            <h3 className="text-base font-semibold text-white leading-snug">{problem.title}</h3>
            <p className={`text-sm text-slate-300 mt-1.5 leading-relaxed ${open ? '' : 'line-clamp-2'}`}>
              {problem.description}
            </p>
          </div>
          <button
            onClick={() => setOpen(!open)}
            className="shrink-0 mt-1 w-8 h-8 flex items-center justify-center rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-all"
          >
            {open ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>

        <div className="flex flex-wrap gap-2 mt-3.5">
          {problem.domain && (
            <span className="px-2.5 py-1 rounded-md text-xs font-medium bg-blue-500/20 text-blue-300 border border-blue-500/30">
              {problem.domain}
            </span>
          )}
          {problem.difficulty && (
            <span className={`px-2.5 py-1 rounded-md text-xs font-medium border ${difficultyColors[problem.difficulty] || 'bg-white/5 text-slate-400 border-white/10'}`}>
              {problem.difficulty}
            </span>
          )}
          {problem.is_open && (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
              Open
            </span>
          )}
        </div>

        {open && (
          <div className="mt-4 pt-4 border-t border-white/10 space-y-4">
            {problem.tags?.length > 0 && (
              <div className="flex flex-wrap gap-1.5">
                {problem.tags.map(tag => (
                  <span key={tag} className="px-2 py-0.5 bg-white/5 text-slate-400 rounded text-xs">{tag}</span>
                ))}
              </div>
            )}
            <div className="flex flex-wrap gap-4 text-sm text-slate-400">
              {problem.organization && (
                <span className="flex items-center gap-1.5"><Building2 className="w-3.5 h-3.5" />{problem.organization}</span>
              )}
              {problem.source_year && (
                <span className="flex items-center gap-1.5"><Calendar className="w-3.5 h-3.5" />{problem.source_year}</span>
              )}
              <span className="flex items-center gap-1.5"><Globe className="w-3.5 h-3.5" />{problem.source_platform || 'General'}</span>
            </div>
            {problem.source_link && (
              <a
                href={problem.source_link}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 text-sm text-blue-400 hover:text-blue-300 font-medium"
              >
                <ExternalLink className="w-3.5 h-3.5" />
                View original source
              </a>
            )}
          </div>
        )}
      </div>
    </motion.div>
  )
}
