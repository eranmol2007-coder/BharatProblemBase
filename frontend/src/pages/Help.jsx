import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { FadeUp } from '../components/FadeUp'
import { Search, Filter, RefreshCw, MousePointerClick, ArrowUpRight, HelpCircle, SlidersHorizontal, Globe } from 'lucide-react'

const stagger = {
  initial: { opacity: 0, y: 16 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, amount: 0.1 },
  transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] },
}

const sections = [
  {
    icon: Search,
    title: 'Browsing Problems',
    steps: [
      'Go to the Problems page from the navigation bar.',
      'Use the search bar to find problems by keyword.',
      'Filter by domain, platform, or difficulty using the dropdowns.',
      'Click "View all platforms" on the home page to explore by platform.',
    ],
  },
  {
    icon: Filter,
    title: 'Using Filters',
    steps: [
      'Open the Filters panel on the Problems page.',
      'Select a domain to narrow by category (AI/ML, Web, Blockchain, etc.).',
      'Pick a platform to see problems from specific sources.',
      'Choose a difficulty level — Beginner, Intermediate, or Advanced.',
      'Click "Clear all" to reset filters.',
    ],
  },
  {
    icon: MousePointerClick,
    title: 'Exploring Problem Details',
    steps: [
      'Click the expand button on any problem card to view full details.',
      'See tags, organization, source year, and the original platform.',
      'Click "View original source" to open the problem on its host site.',
    ],
  },
  {
    icon: RefreshCw,
    title: 'Refreshing Data (Scraping)',
    steps: [
      'Click the "Scrape" button on the Problems page to fetch the latest problem statements.',
      'New problems are added automatically while keeping existing ones.',
      'Scraping runs in the background and may take a few moments.',
    ],
  },
  {
    icon: SlidersHorizontal,
    title: 'Platform Pages',
    steps: [
      'Click on any platform card on the home page to see all problems from that platform.',
      'Use the back button to return to the home page.',
    ],
  },
  {
    icon: Globe,
    title: 'Supported Platforms',
    steps: [
      'BharatProblemBase aggregates from Smart India Hackathon, Unstop, Devfolio, HackerEarth, D2C, HackerRank, CodeChef, MLH, LeetCode, Codeforces, Kaggle, AtCoder, Devpost, and more.',
      'New platforms are added regularly.',
    ],
  },
]

export default function Help() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
      <FadeUp className="max-w-3xl mx-auto text-center mb-14">
        <div className="inline-flex items-center gap-2 bg-blue-500/20 text-blue-300 px-3.5 py-1.5 rounded-full text-sm font-medium mb-6 border border-blue-500/30">
          <HelpCircle className="w-3.5 h-3.5" />
          Help Guide
        </div>
        <h1 className="text-4xl font-bold text-white tracking-tight mb-4">How to Use BharatProblemBase</h1>
        <p className="text-slate-400 leading-relaxed max-w-xl mx-auto">
          Everything you need to know to find, filter, and explore hackathon problem statements.
        </p>
      </FadeUp>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-14">
        {sections.map((s, i) => (
          <motion.div
            key={s.title}
            {...stagger}
            transition={{ ...stagger.transition, delay: i * 0.08 }}
            className="bg-slate-900/60 backdrop-blur-xl rounded-xl border border-white/10 p-6"
          >
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-lg bg-blue-500/20 flex items-center justify-center shrink-0">
                <s.icon className="w-5 h-5 text-blue-400" />
              </div>
              <h3 className="font-semibold text-white">{s.title}</h3>
            </div>
            <ul className="space-y-2">
              {s.steps.map((step, j) => (
                <li key={j} className="flex items-start gap-2.5 text-sm text-slate-300">
                  <span className="w-5 h-5 rounded-full bg-blue-500/20 text-blue-400 text-xs font-medium flex items-center justify-center shrink-0 mt-0.5">{j + 1}</span>
                  {step}
                </li>
              ))}
            </ul>
          </motion.div>
        ))}
      </div>

      <FadeUp className="bg-slate-900/60 backdrop-blur-xl rounded-2xl border border-white/10 p-8 md:p-12 text-center">
        <h2 className="text-xl font-bold text-white mb-3">Still have questions?</h2>
        <p className="text-slate-400 max-w-md mx-auto mb-8 text-sm">
          Browse all available problem statements or go back to the home page to explore by platform.
        </p>
        <div className="flex flex-wrap justify-center gap-3">
          <Link
            to="/problems"
            className="inline-flex items-center gap-2 bg-blue-500 text-white px-6 py-2.5 rounded-lg font-semibold text-sm hover:bg-blue-600 transition-colors"
          >
            <Search className="w-4 h-4" />
            Browse Problems
          </Link>
          <Link
            to="/"
            className="inline-flex items-center gap-2 bg-white/10 text-white px-6 py-2.5 rounded-lg font-semibold text-sm hover:bg-white/20 transition-colors"
          >
            Home
          </Link>
        </div>
      </FadeUp>
    </div>
  )
}
