import { useState, useEffect, useCallback } from 'react'
import { useSearchParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { api } from '../api'
import ProblemCard from '../components/ProblemCard'
import Filters from '../components/Filters'
import { RefreshCw, ChevronLeft, ChevronRight, Loader2 } from 'lucide-react'

export default function Problems() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [problems, setProblems] = useState([])
  const [total, setTotal] = useState(0)
  const [totalPages, setTotalPages] = useState(1)
  const [domains, setDomains] = useState([])
  const [platforms, setPlatforms] = useState([])
  const [loading, setLoading] = useState(true)
  const [scraping, setScraping] = useState(false)
  const [error, setError] = useState(null)

  const [filters, setFilters] = useState({
    search: searchParams.get('search') || '',
    domain: searchParams.get('domain') || '',
    platform: searchParams.get('platform') || '',
    difficulty: searchParams.get('difficulty') || '',
    page: parseInt(searchParams.get('page')) || 1,
    page_size: 20,
  })

  const fetchData = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const params = { ...filters }
      Object.keys(params).forEach(k => { if (!params[k] && params[k] !== 0) delete params[k] })
      const [res, domRes, platRes] = await Promise.all([
        api.getProblems(params),
        api.getDomains(),
        api.getPlatforms(),
      ])
      setProblems(res.items || [])
      setTotal(res.total)
      setTotalPages(res.total_pages)
      setDomains(domRes || [])
      setPlatforms(platRes || [])
    } catch (e) {
      setError(e.message?.includes('Failed to fetch') ? 'Cannot connect to server.' : `Failed to load: ${e.message}`)
    } finally {
      setLoading(false)
    }
  }, [filters])

  useEffect(() => {
    fetchData()
    const q = new URLSearchParams()
    Object.entries(filters).forEach(([k, v]) => { if (v) q.set(k, v) })
    setSearchParams(q, { replace: true })
  }, [fetchData, setSearchParams])

  const handleScrape = async () => {
    setScraping(true)
    try {
      const res = await api.triggerScrape()
      alert(`Scrape complete!\nTotal: ${res.total}\nNew: ${res.new}`)
      fetchData()
    } catch (e) {
      alert('Scrape failed: ' + e.message)
    } finally {
      setScraping(false)
    }
  }

  const goPage = (p) => setFilters(prev => ({ ...prev, page: Math.max(1, Math.min(p, totalPages)) }))

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Problem Statements</h1>
          <p className="text-sm text-slate-400 mt-1">{total.toLocaleString()} problems · {platforms.length} platforms</p>
        </div>
        <button
          onClick={handleScrape}
          disabled={scraping}
          className="flex items-center gap-2 bg-blue-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-600 transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${scraping ? 'animate-spin' : ''}`} />
          {scraping ? 'Scraping...' : 'Scrape'}
        </button>
      </div>

      <Filters filters={filters} setFilters={setFilters} domains={domains} platforms={platforms} />

      {error && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 bg-red-500/20 border border-red-500/30 text-red-300 px-4 py-3 rounded-lg text-sm"
        >
          {error}
        </motion.div>
      )}

      <div className="mt-6 space-y-3">
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="w-6 h-6 animate-spin text-slate-400" />
          </div>
        ) : problems.length === 0 ? (
          <div className="text-center py-20 text-slate-400">
            <p className="font-medium">No problems found</p>
            <p className="text-sm mt-1">Try adjusting your filters</p>
          </div>
        ) : (
          problems.map(p => <ProblemCard key={p.id} problem={p} />)
        )}
      </div>

      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-4 mt-8">
          <button
            onClick={() => goPage(filters.page - 1)}
            disabled={filters.page <= 1}
            className="flex items-center gap-1 px-3 py-2 text-sm font-medium text-slate-300 bg-slate-900/60 backdrop-blur-xl border border-white/10 rounded-lg hover:bg-white/10 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            <ChevronLeft className="w-4 h-4" /> Previous
          </button>
          <span className="text-sm text-slate-400">
            Page <span className="font-medium text-white">{filters.page}</span> of {totalPages}
          </span>
          <button
            onClick={() => goPage(filters.page + 1)}
            disabled={filters.page >= totalPages}
            className="flex items-center gap-1 px-3 py-2 text-sm font-medium text-slate-300 bg-slate-900/60 backdrop-blur-xl border border-white/10 rounded-lg hover:bg-white/10 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            Next <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  )
}
