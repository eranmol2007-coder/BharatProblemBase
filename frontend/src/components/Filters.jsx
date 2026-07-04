import { Search, SlidersHorizontal, X } from 'lucide-react'

export default function Filters({ filters, setFilters, domains = [], platforms = [] }) {
  const update = (key, value) => setFilters(prev => ({ ...prev, [key]: value, page: 1 }))
  const hasFilters = filters.search || filters.domain || filters.platform || filters.difficulty

  const inputClass = "w-full px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-500/50 transition-all"

  return (
    <div className="bg-slate-900/60 backdrop-blur-xl rounded-xl border border-white/10">
      <div className="px-5 py-3 border-b border-white/10 flex items-center justify-between">
        <div className="flex items-center gap-2 text-sm font-medium text-slate-300">
          <SlidersHorizontal className="w-4 h-4 text-slate-400" />
          Filters
        </div>
        {hasFilters && (
          <button
            onClick={() => setFilters({ search: '', domain: '', platform: '', difficulty: '', page: 1, page_size: 20 })}
            className="text-xs text-slate-400 hover:text-white flex items-center gap-1 transition-colors"
          >
            <X className="w-3 h-3" /> Clear all
          </button>
        )}
      </div>
      <div className="p-5 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input
            type="text"
            placeholder="Search problems..."
            value={filters.search || ''}
            onChange={e => update('search', e.target.value)}
            className={`${inputClass} pl-9`}
          />
        </div>
        <select
          value={filters.domain || ''}
          onChange={e => update('domain', e.target.value)}
          className={inputClass}
        >
          <option value="" className="bg-slate-900">All Domains</option>
          {domains.map(d => (
            <option key={d.name} value={d.name} className="bg-slate-900">{d.name} ({d.count})</option>
          ))}
        </select>
        <select
          value={filters.platform || ''}
          onChange={e => update('platform', e.target.value)}
          className={inputClass}
        >
          <option value="" className="bg-slate-900">All Platforms</option>
          {platforms.map(p => (
            <option key={p.name} value={p.name} className="bg-slate-900">{p.name} ({p.total})</option>
          ))}
        </select>
        <select
          value={filters.difficulty || ''}
          onChange={e => update('difficulty', e.target.value)}
          className={inputClass}
        >
          <option value="" className="bg-slate-900">All Difficulties</option>
          {['Beginner', 'Intermediate', 'Advanced'].map(d => (
            <option key={d} value={d} className="bg-slate-900">{d}</option>
          ))}
        </select>
      </div>
    </div>
  )
}
