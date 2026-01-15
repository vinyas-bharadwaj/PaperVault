import { useState } from 'react'
import type { FormEvent } from 'react'
import Input from '../components/Input'
import Button from '../components/Button'
import Card from '../components/Card'

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
      setResults(data)
    } catch (err) {
      console.error('Search error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">Search Notes</h1>
        <p className="text-zinc-400">Find exactly what you're looking for</p>
      </div>
      
      <Card>
        <form onSubmit={handleSearch} className="flex gap-4">
          <div className="flex-1">
            <Input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by topic, concept, or keyword..."
            />
          </div>
          <Button type="submit" disabled={loading}>
            {loading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Searching
              </span>
            ) : (
              'Search'
            )}
          </Button>
        </form>
      </Card>

      <div className="mt-8 space-y-4">
        {results.map((result, idx) => (
          <Card key={idx}>
            <div className="space-y-3">
              <h3 className="text-xl font-semibold text-white">{result.title}</h3>
              <div className="flex flex-wrap items-center gap-3 text-sm text-zinc-400">
                <span className="px-3 py-1 bg-zinc-800 rounded-full">{result.subject}</span>
                <span>{result.semester}</span>
                {result.professor && (
                  <span className="text-zinc-500">• {result.professor}</span>
                )}
                <div className="ml-auto flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-blue-500"></div>
                  <span className="text-blue-400 font-medium">{(result.score * 100).toFixed(0)}% match</span>
                </div>
              </div>
              <p className="text-zinc-300 leading-relaxed">{result.text}...</p>
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}
