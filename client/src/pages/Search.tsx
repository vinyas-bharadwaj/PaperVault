import { useState, FormEvent } from 'react'

interface Result {
  title: string
  subject: string
  semester: string
  professor: string | null
  text: string
  score: number
}

export default function Search() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<Result[]>([])
  const [loading, setLoading] = useState(false)

  const handleSearch = async (e: FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    try {
      setLoading(true)
      const res = await fetch(`http://localhost:8000/upload/search?query=${encodeURIComponent(query)}`, {
        method: 'POST'
      })
      const data = await res.json()
      console.log('Search results:', data)
      setResults(data)
    } catch (err) {
      console.error('Search error:', err)
      alert('Search failed - check console')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Search Notes</h1>
      <form onSubmit={handleSearch} style={{ marginTop: '2rem', display: 'flex', gap: '1rem' }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by topic, concept, or keyword..."
          style={{ flex: 1, padding: '0.75rem', background: '#18181b', border: '1px solid #3f3f46', borderRadius: '4px', color: '#e4e4e7' }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{ padding: '0.75rem 1.5rem', background: '#3b82f6', border: 'none', borderRadius: '4px', color: 'white', cursor: 'pointer', fontWeight: '500' }}
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      <div style={{ marginTop: '2rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {results.map((result, idx) => (
          <div key={idx} style={{ padding: '1.5rem', background: '#18181b', border: '1px solid #3f3f46', borderRadius: '4px' }}>
            <h3 style={{ marginBottom: '0.5rem' }}>{result.title}</h3>
            <div style={{ display: 'flex', gap: '1rem', fontSize: '0.875rem', color: '#a1a1aa', marginBottom: '1rem' }}>
              <span>{result.subject}</span>
              <span>•</span>
              <span>{result.semester}</span>
              {result.professor && (
                <>
                  <span>•</span>
                  <span>{result.professor}</span>
                </>
              )}
              <span>•</span>
              <span>Score: {(result.score * 100).toFixed(1)}%</span>
            </div>
            <p style={{ color: '#d4d4d8', fontSize: '0.875rem' }}>{result.text}...</p>
          </div>
        ))}
      </div>
    </div>
  )
}
