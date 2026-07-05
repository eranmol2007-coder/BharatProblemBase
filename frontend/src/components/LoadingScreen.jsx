import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const NODES = [
  { x: 0, y: -60, delay: 0 },
  { x: 52, y: -30, delay: 0.1 },
  { x: 52, y: 30, delay: 0.2 },
  { x: 0, y: 60, delay: 0.3 },
  { x: -52, y: 30, delay: 0.4 },
  { x: -52, y: -30, delay: 0.5 },
  { x: 0, y: 0, delay: 0.15 },
]

const CONNECTIONS = [
  [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 0],
  [6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5],
]

export default function LoadingScreen({ onComplete }) {
  const [show, setShow] = useState(true)

  useEffect(() => {
    const timer = setTimeout(() => {
      setShow(false)
      setTimeout(onComplete, 600)
    }, 2200)
    return () => clearTimeout(timer)
  }, [onComplete])

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          initial={{ opacity: 1 }}
          exit={{ opacity: 0, scale: 1.05 }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="fixed inset-0 z-[9999] flex flex-col items-center justify-center bg-white"
        >
          {/* Background subtle gradient */}
          <div className="absolute inset-0 bg-gradient-to-br from-cyan-50/50 via-white to-blue-50/30" />

          {/* 3D Scene Container */}
          <div className="relative" style={{ perspective: '600px' }}>
            <motion.div
              animate={{ rotateY: [0, 360] }}
              transition={{ duration: 4, ease: 'linear', repeat: Infinity }}
              style={{ transformStyle: 'preserve-3d' }}
              className="relative w-40 h-40"
            >
              {/* Network connections */}
              <svg
                viewBox="-80 -80 160 160"
                className="absolute inset-0 w-full h-full"
                style={{ transform: 'translateZ(20px)' }}
              >
                {CONNECTIONS.map(([a, b], i) => (
                  <motion.line
                    key={i}
                    x1={NODES[a].x}
                    y1={NODES[a].y}
                    x2={NODES[b].x}
                    y2={NODES[b].y}
                    stroke="#06b6d4"
                    strokeWidth="0.8"
                    initial={{ pathLength: 0, opacity: 0 }}
                    animate={{ pathLength: 1, opacity: 0.4 }}
                    transition={{ duration: 0.8, delay: 0.3 + i * 0.05, ease: 'easeOut' }}
                  />
                ))}
              </svg>

              {/* Network nodes */}
              {NODES.map((node, i) => (
                <motion.div
                  key={i}
                  className="absolute"
                  style={{
                    left: `calc(50% + ${node.x}px)`,
                    top: `calc(50% + ${node.y}px)`,
                    transform: `translate(-50%, -50%) translateZ(${i === 6 ? 30 : 15}px)`,
                  }}
                  initial={{ scale: 0, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ duration: 0.5, delay: node.delay, ease: [0.22, 1, 0.36, 1] }}
                >
                  {/* Glow */}
                  <motion.div
                    animate={{
                      boxShadow: [
                        '0 0 8px 2px rgba(6, 182, 212, 0.3)',
                        '0 0 16px 4px rgba(6, 182, 212, 0.5)',
                        '0 0 8px 2px rgba(6, 182, 212, 0.3)',
                      ],
                    }}
                    transition={{ duration: 2, repeat: Infinity, delay: i * 0.2 }}
                    className={`rounded-full ${i === 6 ? 'w-5 h-5 bg-cyan-500' : 'w-3 h-3 bg-cyan-400'}`}
                  />
                  {/* Center dot */}
                  <div className={`absolute inset-0 m-auto rounded-full bg-white ${i === 6 ? 'w-2 h-2' : 'w-1 h-1'}`} />
                </motion.div>
              ))}

              {/* Floating ring */}
              <motion.div
                animate={{ rotateX: [0, 360], rotateZ: [0, -360] }}
                transition={{ duration: 6, ease: 'linear', repeat: Infinity }}
                className="absolute inset-[-10px] border border-cyan-200/40 rounded-full"
                style={{ transformStyle: 'preserve-3d', transform: 'translateZ(25px)' }}
              />
              <motion.div
                animate={{ rotateX: [0, -360], rotateZ: [0, 360] }}
                transition={{ duration: 8, ease: 'linear', repeat: Infinity }}
                className="absolute inset-[-25px] border border-cyan-100/30 rounded-full"
                style={{ transformStyle: 'preserve-3d', transform: 'translateZ(10px)' }}
              />
            </motion.div>
          </div>

          {/* Text */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
            className="relative mt-10 text-center"
          >
            <h2 className="text-xl font-bold text-slate-800 tracking-tight">BharatProblemBase</h2>
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8 }}
              className="text-sm text-slate-400 mt-2"
            >
              Aggregating hackathon problems...
            </motion.p>
          </motion.div>

          {/* Loading bar */}
          <div className="relative mt-6 w-48 h-1 bg-slate-100 rounded-full overflow-hidden">
            <motion.div
              initial={{ x: '-100%' }}
              animate={{ x: '100%' }}
              transition={{ duration: 1.2, repeat: Infinity, ease: 'easeInOut' }}
              className="absolute inset-y-0 w-1/2 bg-gradient-to-r from-transparent via-cyan-400 to-transparent rounded-full"
            />
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
