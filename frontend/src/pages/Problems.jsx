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
  const [searchLoading, setSearchLoading] = useState(false)
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
    const isSearch = filters.search && !loading
    if (isSearch) setSearchLoading(true)
    else setLoading(true)
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
      setSearchLoading(false)
    }
  }, [filters])

  useEffect(() => {
    fetchData()
    const q = new URLSearchParams()
    Object.entries(filters).forEach(([k, v]) => { if (v) q.set(k, v) })
    setSearchParams(q, { replace: true })
  }, [fetchData, setSearchParams, filters])

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
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 bg-white/90 backdrop-blur-sm rounded-3xl mt-4 mb-4 shadow-[0_8px_40px_-12px_rgba(0,0,0,0.08)]">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Problem Statements</h1>
          <p className="text-sm text-slate-500 mt-1">{total.toLocaleString()} problems · {platforms.length} platforms</p>
        </div>
        <button
          onClick={handleScrape}
          disabled={scraping}
          className="flex items-center gap-2 bg-cyan-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-cyan-600 transition-colors disabled:opacity-50 shadow-sm"
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
          className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm"
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
          <>
            {searchLoading && (
              <div className="flex items-center justify-center py-2">
                <Loader2 className="w-4 h-4 animate-spin text-cyan-500 mr-2" />
                <span className="text-xs text-slate-400">Searching...</span>
              </div>
            )}
            {problems.map(p => <ProblemCard key={p.id} problem={p} />)}
          </>
        )}
      </div>

      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-4 mt-8">
          <button
            onClick={() => goPage(filters.page - 1)}
            disabled={filters.page <= 1}
            className="flex items-center gap-1 px-3 py-2 text-sm font-medium text-slate-600 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-sm"
          >
            <ChevronLeft className="w-4 h-4" /> Previous
          </button>
          <span className="text-sm text-slate-500">
            Page <span className="font-medium text-slate-900">{filters.page}</span> of {totalPages}
          </span>
          <button
            onClick={() => goPage(filters.page + 1)}
            disabled={filters.page >= totalPages}
            className="flex items-center gap-1 px-3 py-2 text-sm font-medium text-slate-600 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-sm"
          >
            Next <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  )
}
