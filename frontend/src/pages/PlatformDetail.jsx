import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { api } from '../api'
import ProblemCard from '../components/ProblemCard'
import { ArrowLeft, Globe, Loader2, ChevronLeft, ChevronRight } from 'lucide-react'

export default function PlatformDetail() {
  const { name } = useParams()
  const [problems, setProblems] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.getProblems({ platform: name, page, page_size: 20 })
      .then(res => {
        setProblems(res.items || [])
        setTotal(res.total)
        setTotalPages(res.total_pages)
      })
      .finally(() => setLoading(false))
  }, [name, page])

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 bg-white/90 backdrop-blur-sm rounded-3xl mt-4 mb-4 shadow-[0_8px_40px_-12px_rgba(0,0,0,0.08)]">
      <Link to="/" className="inline-flex items-center gap-1.5 text-sm text-slate-400 hover:text-cyan-600 transition-colors mb-6">
        <ArrowLeft className="w-4 h-4" /> Back to Home
      </Link>
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
        className="flex items-center gap-4 mb-8"
      >
        <div className="w-12 h-12 rounded-xl bg-cyan-50 flex items-center justify-center">
          <Globe className="w-6 h-6 text-cyan-600" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">{name}</h1>
          <p className="text-sm text-slate-500">{total.toLocaleString()} {total === 1 ? 'problem' : 'problems'} · Page {page} of {totalPages}</p>
        </div>
      </motion.div>

      {loading ? (
        <div className="flex items-center justify-center py-20"><Loader2 className="w-6 h-6 animate-spin text-slate-400" /></div>
      ) : problems.length === 0 ? (
        <div className="text-center py-20 text-slate-400"><p className="font-medium">No problems from this platform yet</p></div>
      ) : (
        <>
          <div className="space-y-3">{problems.map((p, i) => (
            <motion.div
              key={p.id}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.05 }}
              transition={{ duration: 0.4, delay: i * 0.03, ease: [0.22, 1, 0.36, 1] }}
            >
              <ProblemCard problem={p} />
            </motion.div>
          ))}</div>

          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-4 mt-8 pt-6 border-t border-slate-100">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page <= 1}
                className="flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors shadow-sm"
              >
                <ChevronLeft className="w-4 h-4" /> Previous
              </button>
              <span className="text-sm text-slate-500 font-medium">Page {page} of {totalPages}</span>
              <button
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                disabled={page >= totalPages}
                className="flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors shadow-sm"
              >
                Next <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}
