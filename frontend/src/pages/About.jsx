import { motion } from 'framer-motion'
import { Compass, Brain, Globe, Database, Sparkles, Search, ArrowRight } from 'lucide-react'
import { Link } from 'react-router-dom'
import { FadeUp } from '../components/FadeUp'

const features = [
  {
    icon: Brain,
    title: 'ML-Powered Classification',
    desc: 'NLP models automatically classify problem statements into domains like AI/ML, Blockchain, IoT, and more.',
  },
  {
    icon: Globe,
    title: 'Multi-Platform Aggregation',
    desc: 'Scrapers fetch problem statements from Smart India Hackathon, Devfolio, HackerEarth, Unstop, and more.',
  },
  {
    icon: Database,
    title: 'Central Repository',
    desc: 'All problem statements stored in one searchable, filterable database.',
  },
  {
    icon: Sparkles,
    title: 'Smart Search & Filters',
    desc: 'Search by keyword, filter by domain, platform, difficulty, and status.',
  },
]

const stagger = {
  initial: { opacity: 0, y: 16 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, amount: 0.1 },
  transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] },
}

export default function About() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 bg-white/90 backdrop-blur-sm rounded-3xl mt-4 mb-4 shadow-[0_8px_40px_-12px_rgba(0,0,0,0.08)]">
      <FadeUp className="max-w-3xl mx-auto text-center mb-14">
        <div className="inline-flex items-center gap-2 bg-cyan-50 text-cyan-700 px-3.5 py-1.5 rounded-full text-sm font-medium mb-6 border border-cyan-200">
          <Compass className="w-3.5 h-3.5" />
          About BharatProblemBase
        </div>
        <h1 className="text-4xl font-bold text-slate-900 tracking-tight mb-4">Never Search for Hackathon Problems Again</h1>
        <p className="text-slate-500 leading-relaxed max-w-xl mx-auto">
          BharatProblemBase aggregates problem statements from hackathon platforms across India, using ML to organize and classify them intelligently.
        </p>
        <div className="mt-8 flex justify-center">
          <img src="/ml_illustration.svg" alt="ML Classification" className="w-full max-w-md rounded-2xl shadow-lg border border-cyan-100" />
        </div>
      </FadeUp>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-14">
        {features.map((f, i) => (
          <motion.div
            key={f.title}
            {...stagger}
            transition={{ ...stagger.transition, delay: i * 0.08 }}
            className="bg-white rounded-2xl border border-slate-200 p-6 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.06)]"
          >
            <div className="w-10 h-10 rounded-lg bg-cyan-50 flex items-center justify-center mb-4">
              <f.icon className="w-5 h-5 text-cyan-600" />
            </div>
            <h3 className="font-semibold text-slate-900 mb-2">{f.title}</h3>
            <p className="text-sm text-slate-500 leading-relaxed">{f.desc}</p>
          </motion.div>
        ))}
      </div>

      <FadeUp className="bg-white rounded-2xl border border-slate-200 p-8 mb-14 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.06)]">
        <h2 className="text-xl font-bold text-slate-900 mb-8 text-center">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            { step: '01', title: 'Scrape', desc: 'ML agents crawl hackathon platforms to discover new problem statements.' },
            { step: '02', title: 'Classify', desc: 'NLP models analyze each problem to determine domain, difficulty, and tags.' },
            { step: '03', title: 'Organize', desc: 'Problems are stored with metadata and made searchable through our platform.' },
          ].map((item, i) => (
            <motion.div
              key={item.step}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.5, delay: i * 0.12, ease: [0.22, 1, 0.36, 1] }}
              className="text-center"
            >
              <div className="text-2xl font-bold text-cyan-500/60 mb-2">{item.step}</div>
              <h4 className="font-semibold text-slate-900 mb-1">{item.title}</h4>
              <p className="text-sm text-slate-500">{item.desc}</p>
            </motion.div>
          ))}
        </div>
      </FadeUp>

      <FadeUp className="text-center">
        <h2 className="text-lg font-bold text-slate-900 mb-4">Supported Platforms</h2>
        <div className="flex justify-center mb-8">
          <img src="/network_illustration.svg" alt="Network" className="w-full max-w-sm rounded-2xl shadow-lg border border-cyan-100" />
        </div>
        <div className="flex flex-wrap justify-center gap-2 max-w-2xl mx-auto">
          {['Smart India Hackathon', 'Unstop', 'Devfolio', 'HackerEarth', 'D2C', 'HackerRank', 'CodeChef', 'MLH', 'LeetCode', 'Codeforces', 'Kaggle', 'AtCoder', 'Devpost'].map(p => (
            <span key={p} className="px-3 py-1.5 bg-white border border-slate-200 rounded-xl text-sm text-slate-600 shadow-sm">
              {p}
            </span>
          ))}
        </div>
        <Link
          to="/problems"
          className="inline-flex items-center gap-2 bg-cyan-500 text-white px-6 py-2.5 rounded-lg font-medium text-sm hover:bg-cyan-600 transition-colors mt-8 shadow-sm"
        >
          <Search className="w-4 h-4" />
          Browse Problems <ArrowRight className="w-4 h-4" />
        </Link>
      </FadeUp>
    </div>
  )
}
