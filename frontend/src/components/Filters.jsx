import { useState, useEffect, useRef } from 'react'
import { Search, SlidersHorizontal, X } from 'lucide-react'

export default function Filters({ filters, setFilters, domains = [], platforms = [] }) {
  const hasFilters = filters.search || filters.domain || filters.platform || filters.difficulty

  const [localSearch, setLocalSearch] = useState(filters.search || '')
  const [suggestions, setSuggestions] = useState([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [highlightIdx, setHighlightIdx] = useState(-1)
  const [searching, setSearching] = useState(false)
  const inputRef = useRef(null)
  const wrapperRef = useRef(null)
  const debounceRef = useRef(null)
  const abortRef = useRef(null)

  useEffect(() => {
    setLocalSearch(filters.search || '')
  }, [filters.search])

  useEffect(() => {
    const q = localSearch.trim()
    if (q.length < 1) { setSuggestions([]); setShowSuggestions(false); return }
    if (abortRef.current) abortRef.current.abort()
    const controller = new AbortController()
    abortRef.current = controller
    setSearching(true)
    fetch(`/api/problems/suggest?q=${encodeURIComponent(q)}`, { signal: controller.signal })
      .then(r => r.json())
      .then(data => {
        setSuggestions(data || [])
        setShowSuggestions(true)
        setHighlightIdx(-1)
      })
      .catch(() => {})
      .finally(() => setSearching(false))
    return () => controller.abort()
  }, [localSearch])

  const commitSearch = (value) => {
    setFilters(prev => ({ ...prev, search: value, page: 1 }))
  }

  const handleInput = (e) => {
    const val = e.target.value
    setLocalSearch(val)
    clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => commitSearch(val), 350)
  }

  const clearAll = () => {
    setLocalSearch('')
    setSuggestions([])
    setShowSuggestions(false)
    setFilters({ search: '', domain: '', platform: '', difficulty: '', page: 1, page_size: 20 })
  }

  useEffect(() => {
    const handler = (e) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) setShowSuggestions(false)
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  const handleKeyDown = (e) => {
    if (!showSuggestions || !suggestions.length) {
      if (e.key === 'Enter') { e.preventDefault(); clearTimeout(debounceRef.current); commitSearch(localSearch); setShowSuggestions(false) }
      return
    }
    if (e.key === 'ArrowDown') { e.preventDefault(); setHighlightIdx(i => (i + 1) % suggestions.length) }
    else if (e.key === 'ArrowUp') { e.preventDefault(); setHighlightIdx(i => (i - 1 + suggestions.length) % suggestions.length) }
    else if (e.key === 'Enter') {
      e.preventDefault()
      if (highlightIdx >= 0) {
        const val = suggestions[highlightIdx].title
        setLocalSearch(val)
        clearTimeout(debounceRef.current)
        commitSearch(val)
      } else {
        clearTimeout(debounceRef.current)
        commitSearch(localSearch)
      }
      setShowSuggestions(false)
    } else if (e.key === 'Escape') { setShowSuggestions(false) }
  }

  const selectSuggestion = (s) => {
    setLocalSearch(s.title)
    clearTimeout(debounceRef.current)
    commitSearch(s.title)
    setShowSuggestions(false)
  }

  const inputClass = "w-full px-3 py-2.5 bg-white border border-slate-200 rounded-xl text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-cyan-500/30 focus:border-cyan-500 transition-all shadow-sm"

  return (
    <div className="bg-white/80 backdrop-blur-2xl rounded-2xl border border-slate-200/60 shadow-[0_4px_24px_0_rgba(0,0,0,0.06)] ring-1 ring-inset ring-white/50 mb-6">
      <div className="px-6 py-3.5 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center gap-2 text-sm font-medium text-cyan-700">
          <SlidersHorizontal className="w-4 h-4 text-cyan-500" />
          Filters
        </div>
        {hasFilters && (
          <button onClick={clearAll} className="text-xs text-slate-400 hover:text-cyan-600 flex items-center gap-1 transition-colors">
            <X className="w-3 h-3" /> Clear all
          </button>
        )}
      </div>
      <div className="p-5 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <div className="relative" ref={wrapperRef}>
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-cyan-400 z-10" />
          <input
            ref={inputRef}
            type="text"
            placeholder="Search problems..."
            value={localSearch}
            onChange={handleInput}
            onFocus={() => { if (suggestions.length) setShowSuggestions(true) }}
            onKeyDown={handleKeyDown}
            className={`${inputClass} pl-9`}
            autoComplete="off"
          />
          {showSuggestions && suggestions.length > 0 && (
            <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-slate-200 rounded-xl shadow-lg z-50 max-h-80 overflow-y-auto">
              {suggestions.map((s, i) => (
                <button
                  key={s.id}
                  onMouseDown={(e) => { e.preventDefault(); selectSuggestion(s) }}
                  className={`w-full text-left px-4 py-2.5 text-sm flex items-center gap-3 transition-colors ${
                    i === highlightIdx ? 'bg-cyan-50 text-cyan-700' : 'text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  <Search className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                  <span className="truncate flex-1">{s.title}</span>
                  <span className="text-xs text-slate-400 shrink-0">{s.domain}</span>
                </button>
              ))}
            </div>
          )}
        </div>
        <select value={filters.domain || ''} onChange={e => { setFilters(prev => ({ ...prev, domain: e.target.value, page: 1 })) }} className={inputClass}>
          <option value="" className="bg-white">All Domains</option>
          {domains.map(d => <option key={d.name} value={d.name} className="bg-white">{d.name} ({d.count})</option>)}
        </select>
        <select value={filters.platform || ''} onChange={e => { setFilters(prev => ({ ...prev, platform: e.target.value, page: 1 })) }} className={inputClass}>
          <option value="" className="bg-white">All Platforms</option>
          {platforms.map(p => <option key={p.name} value={p.name} className="bg-white">{p.name} ({p.total})</option>)}
        </select>
        <select value={filters.difficulty || ''} onChange={e => { setFilters(prev => ({ ...prev, difficulty: e.target.value, page: 1 })) }} className={inputClass}>
          <option value="" className="bg-white">All Difficulties</option>
          {['Beginner', 'Intermediate', 'Advanced'].map(d => <option key={d} value={d} className="bg-white">{d}</option>)}
        </select>
      </div>
    </div>
  )
}
