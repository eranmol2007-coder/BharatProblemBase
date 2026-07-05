import { useState, useCallback } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import VideoBackground from './components/VideoBackground'
import LoadingScreen from './components/LoadingScreen'
import Home from './pages/Home'
import Problems from './pages/Problems'
import PlatformDetail from './pages/PlatformDetail'
import About from './pages/About'
import Help from './pages/Help'

export default function App() {
  const [loading, setLoading] = useState(true)
  const handleLoaded = useCallback(() => setLoading(false), [])

  return (
    <BrowserRouter>
      {loading && <LoadingScreen onComplete={handleLoaded} />}
      <VideoBackground />
      <div className="relative z-10 min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/help" element={<Help />} />
            <Route path="/problems" element={<Problems />} />
            <Route path="/platform/:name" element={<PlatformDetail />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  )
}
