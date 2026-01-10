import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Upload from './pages/Upload'
import Search from './pages/Search'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <div style={{ minHeight: '100vh' }}>
        <nav style={{ padding: '1rem 2rem', borderBottom: '1px solid #27272a' }}>
          <div style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
            <h2 style={{ margin: 0 }}>PaperVault</h2>
            <Link to="/">Upload</Link>
            <Link to="/search">Search</Link>
          </div>
        </nav>
        <Routes>
          <Route path="/" element={<Upload />} />
          <Route path="/search" element={<Search />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
