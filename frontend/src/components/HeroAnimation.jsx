import { useRef, useEffect } from 'react'

const DOMAINS = ['AI/ML', 'Web', 'IoT', 'Blockchain', 'Cloud', 'Cybersecurity', 'Healthcare', 'Fintech', 'EdTech', 'Agritech']
const NODE_COUNT = 50
const CONNECTION_DIST = 160

function createNode(w, h) {
  return {
    x: Math.random() * w,
    y: Math.random() * h,
    vx: (Math.random() - 0.5) * 0.3,
    vy: (Math.random() - 0.5) * 0.3,
    r: Math.random() * 2 + 1.5,
    pulse: Math.random() < 0.15,
    pulseT: Math.random() * Math.PI * 2,
    label: Math.random() < 0.06 ? DOMAINS[Math.floor(Math.random() * DOMAINS.length)] : null,
    labelOpacity: 0,
    labelTarget: Math.random() < 0.5 ? 1 : 0,
  }
}

export default function HeroAnimation() {
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    let animId
    let nodes = []

    function resize() {
      const dpr = window.devicePixelRatio || 1
      const rect = canvas.getBoundingClientRect()
      canvas.width = rect.width * dpr
      canvas.height = rect.height * dpr
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)

      if (nodes.length === 0) {
        nodes = Array.from({ length: NODE_COUNT }, () => createNode(rect.width, rect.height))
      }
    }

    function draw() {
      const w = canvas.width / (window.devicePixelRatio || 1)
      const h = canvas.height / (window.devicePixelRatio || 1)
      ctx.clearRect(0, 0, w, h)

      // Update nodes
      for (const n of nodes) {
        n.x += n.vx
        n.y += n.vy
        if (n.x < 0 || n.x > w) n.vx *= -1
        if (n.y < 0 || n.y > h) n.vy *= -1
        n.x = Math.max(0, Math.min(w, n.x))
        n.y = Math.max(0, Math.min(h, n.y))
        n.pulseT += 0.015

        // Toggle label visibility slowly
        if (Math.random() < 0.002) n.labelTarget = n.labelTarget ? 0 : 1
        if (n.label) {
          n.labelOpacity += (n.labelTarget - n.labelOpacity) * 0.02
        }
      }

      // Draw connections
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const dx = nodes[i].x - nodes[j].x
          const dy = nodes[i].y - nodes[j].y
          const dist = Math.sqrt(dx * dx + dy * dy)
          if (dist < CONNECTION_DIST) {
            const alpha = (1 - dist / CONNECTION_DIST) * 0.35
            ctx.beginPath()
            ctx.moveTo(nodes[i].x, nodes[i].y)
            ctx.lineTo(nodes[j].x, nodes[j].y)
            ctx.strokeStyle = `rgba(6, 182, 212, ${alpha})`
            ctx.lineWidth = 0.8
            ctx.stroke()
          }
        }
      }

      // Draw pulses traveling along connections
      for (let i = 0; i < nodes.length; i++) {
        if (!nodes[i].pulse) continue
        const n = nodes[i]
        const pulsePhase = (Math.sin(n.pulseT) + 1) / 2
        for (let j = 0; j < nodes.length; j++) {
          if (i === j) continue
          const dx = nodes[j].x - n.x
          const dy = nodes[j].y - n.y
          const dist = Math.sqrt(dx * dx + dy * dy)
          if (dist < CONNECTION_DIST * 0.8) {
            const px = n.x + dx * pulsePhase
            const py = n.y + dy * pulsePhase
            const glow = ctx.createRadialGradient(px, py, 0, px, py, 6)
            glow.addColorStop(0, 'rgba(6, 182, 212, 0.7)')
            glow.addColorStop(1, 'rgba(6, 182, 212, 0)')
            ctx.beginPath()
            ctx.arc(px, py, 6, 0, Math.PI * 2)
            ctx.fillStyle = glow
            ctx.fill()
          }
        }
      }

      // Draw nodes
      for (const n of nodes) {
        // Outer glow
        const glow = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.r * 5)
        glow.addColorStop(0, 'rgba(8, 145, 178, 0.2)')
        glow.addColorStop(1, 'rgba(6, 182, 212, 0)')
        ctx.beginPath()
        ctx.arc(n.x, n.y, n.r * 5, 0, Math.PI * 2)
        ctx.fillStyle = glow
        ctx.fill()

        // Core dot
        ctx.beginPath()
        ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2)
        ctx.fillStyle = 'rgba(8, 145, 178, 0.85)'
        ctx.fill()

        // Bright center
        ctx.beginPath()
        ctx.arc(n.x, n.y, n.r * 0.4, 0, Math.PI * 2)
        ctx.fillStyle = 'rgba(207, 250, 254, 0.9)'
        ctx.fill()

        // Domain label
        if (n.label && n.labelOpacity > 0.01) {
          ctx.font = '600 11px "Helvetica Now Var", sans-serif'
          ctx.textAlign = 'center'
          ctx.fillStyle = `rgba(14, 116, 144, ${n.labelOpacity * 0.9})`
          ctx.fillText(n.label, n.x, n.y - 14)
        }
      }

      animId = requestAnimationFrame(draw)
    }

    resize()
    draw()
    window.addEventListener('resize', resize)

    return () => {
      cancelAnimationFrame(animId)
      window.removeEventListener('resize', resize)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 w-full h-full"
      style={{ opacity: 0.85 }}
    />
  )
}
