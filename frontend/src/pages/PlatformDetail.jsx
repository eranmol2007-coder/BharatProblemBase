import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { api } from '../api'
import ProblemCard from '../components/ProblemCard'
import { ArrowLeft, Globe, Loader2 } from 'lucide-react'

export default function PlatformDetail() {
  const { name } = useParams()
  const [problems, setProblems] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.getProblems({ platform: name, page_size: 50 })
      .then(res => setProblems(res.items || []))
      .finally(() => setLoading(false))
  }, [name])

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
      <Link to="/" className="inline-flex items-center gap-1.5 text-sm text-slate-400 hover:text-white transition-colors mb-6">
        <ArrowLeft className="w-4 h-4" /> Back to Home
      </Link>
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
        className="flex items-center gap-4 mb-8"
      >
        <div className="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center">
          <Globe className="w-6 h-6 text-blue-400" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">{name}</h1>
          <p className="text-sm text-slate-400">{problems.length} {problems.length === 1 ? 'problem' : 'problems'}</p>
        </div>
      </motion.div>
      {loading ? (
        <div className="flex items-center justify-center py-20"><Loader2 className="w-6 h-6 animate-spin text-slate-400" /></div>
      ) : problems.length === 0 ? (
        <div className="text-center py-20 text-slate-400"><p className="font-medium">No problems from this platform yet</p></div>
      ) : (
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
      )}
    </div>
  )
}
