import { useRef, useEffect } from 'react'

export default function VideoBackground() {
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    let animId
    let time = 0
    let mouseX = 0.5
    let mouseY = 0.5

    function resize() {
      const dpr = window.devicePixelRatio || 1
      const rect = canvas.getBoundingClientRect()
      canvas.width = rect.width * dpr
      canvas.height = rect.height * dpr
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
    }

    function handleMouse(e) {
      const rect = canvas.getBoundingClientRect()
      mouseX = e.clientX / rect.width
      mouseY = e.clientY / rect.height
    }

    function drawWave(yBase, amplitude, frequency, speed, color) {
      const w = canvas.width / (window.devicePixelRatio || 1)
      const h = canvas.height / (window.devicePixelRatio || 1)
      ctx.beginPath()
      ctx.moveTo(0, h)
      for (let x = 0; x <= w; x += 3) {
        const normalizedX = x / w
        const y = yBase
          + Math.sin(normalizedX * frequency + time * speed) * amplitude
          + Math.sin(normalizedX * frequency * 0.5 + time * speed * 1.3) * amplitude * 0.5
          + Math.sin(normalizedX * frequency * 2 + time * speed * 0.7) * amplitude * 0.25
          + (mouseY - 0.5) * 30 * Math.sin(normalizedX * 3)
        ctx.lineTo(x, y)
      }
      ctx.lineTo(w, h)
      ctx.closePath()
      ctx.fillStyle = color
      ctx.fill()
    }

    function drawAuroraLayer(yBase, amplitude, frequency, speed, color, opacity) {
      const w = canvas.width / (window.devicePixelRatio || 1)
      ctx.globalAlpha = opacity
      ctx.beginPath()
      ctx.moveTo(0, yBase)
      for (let x = 0; x <= w; x += 2) {
        const nx = x / w
        const y = yBase
          + Math.sin(nx * frequency + time * speed) * amplitude
          + Math.sin(nx * frequency * 1.5 + time * speed * 0.8) * amplitude * 0.4
          + Math.cos(nx * frequency * 0.7 + time * speed * 1.2) * amplitude * 0.3
          + Math.sin(nx * 2 + time * 0.3) * 15
        ctx.lineTo(x, y)
      }
      const gradient = ctx.createLinearGradient(0, yBase - amplitude, 0, yBase + amplitude * 2)
      gradient.addColorStop(0, 'transparent')
      gradient.addColorStop(0.3, color)
      gradient.addColorStop(0.7, color)
      gradient.addColorStop(1, 'transparent')
      ctx.strokeStyle = gradient
      ctx.lineWidth = 40
      ctx.stroke()
      ctx.globalAlpha = 1
    }

    function draw() {
      const w = canvas.width / (window.devicePixelRatio || 1)
      const h = canvas.height / (window.devicePixelRatio || 1)
      time += 0.008

      // Background gradient
      const bg = ctx.createRadialGradient(w * 0.5, h * 0.4, 0, w * 0.5, h * 0.5, w * 0.8)
      bg.addColorStop(0, '#ecfeff')
      bg.addColorStop(0.4, '#ffffff')
      bg.addColorStop(1, '#f8fafc')
      ctx.fillStyle = bg
      ctx.fillRect(0, 0, w, h)

      // Aurora layers (back to front)
      drawAuroraLayer(h * 0.15, 60, 4, 0.4, 'rgba(6, 182, 212, 0.15)', 0.6)
      drawAuroraLayer(h * 0.2, 50, 5, 0.5, 'rgba(6, 182, 212, 0.12)', 0.5)
      drawAuroraLayer(h * 0.25, 40, 6, 0.6, 'rgba(8, 145, 178, 0.1)', 0.4)

      // Flowing waves
      drawWave(h * 0.75, 30, 3, 0.5, 'rgba(6, 182, 212, 0.04)')
      drawWave(h * 0.8, 25, 4, 0.6, 'rgba(8, 145, 178, 0.03)')
      drawWave(h * 0.85, 20, 5, 0.7, 'rgba(14, 116, 144, 0.025)')

      // Floating orbs with glow
      const orbCount = 5
      for (let i = 0; i < orbCount; i++) {
        const ox = w * (0.2 + i * 0.15) + Math.sin(time * 0.5 + i * 1.5) * 80 + (mouseX - 0.5) * 40
        const oy = h * (0.3 + Math.sin(time * 0.3 + i * 2) * 0.15)
        const size = 60 + Math.sin(time + i) * 20

        const orbGlow = ctx.createRadialGradient(ox, oy, 0, ox, oy, size)
        orbGlow.addColorStop(0, `rgba(6, 182, 212, ${0.08 + Math.sin(time + i) * 0.03})`)
        orbGlow.addColorStop(0.5, `rgba(8, 145, 178, ${0.04 + Math.sin(time + i) * 0.02})`)
        orbGlow.addColorStop(1, 'rgba(6, 182, 212, 0)')
        ctx.beginPath()
        ctx.arc(ox, oy, size, 0, Math.PI * 2)
        ctx.fillStyle = orbGlow
        ctx.fill()
      }

      // Scattered sparkle dots
      for (let i = 0; i < 30; i++) {
        const sx = ((i * 137.508 + time * 20) % w)
        const sy = ((i * 97.3 + Math.sin(time * 0.5 + i) * 50) % h)
        const sparkle = 0.15 + Math.sin(time * 3 + i * 0.7) * 0.1
        ctx.beginPath()
        ctx.arc(sx, sy, 1.5, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(8, 145, 178, ${sparkle})`
        ctx.fill()
      }

      animId = requestAnimationFrame(draw)
    }

    resize()
    draw()
    window.addEventListener('resize', resize)
    canvas.addEventListener('mousemove', handleMouse)

    return () => {
      cancelAnimationFrame(animId)
      window.removeEventListener('resize', resize)
      canvas.removeEventListener('mousemove', handleMouse)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 w-full h-full"
      style={{ zIndex: 0 }}
    />
  )
}
