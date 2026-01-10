import { useState, FormEvent } from 'react'

export default function Upload() {
  const [file, setFile] = useState<File | null>(null)
  const [title, setTitle] = useState('')
  const [semester, setSemester] = useState('')
  const [subject, setSubject] = useState('')
  const [professor, setProfessor] = useState('')
  const [status, setStatus] = useState('')

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)
    formData.append('title', title)
    formData.append('semester', semester)
    formData.append('subject', subject)
    formData.append('professor', professor)

    try {
      setStatus('Uploading...')
      const res = await fetch('http://localhost:8000/upload/', {
        method: 'POST',
        body: formData
      })
      const data = await res.json()
      setStatus(`Uploaded: ${data.title}`)
      setFile(null)
      setTitle('')
      setSemester('')
      setSubject('')
      setProfessor('')
    } catch (err) {
      setStatus('Upload failed')
    }
  }

  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto' }}>
      <h1>Upload Notes</h1>
      <form onSubmit={handleSubmit} style={{ marginTop: '2rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>PDF File</label>
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            style={{ padding: '0.5rem', background: '#18181b', border: '1px solid #3f3f46', borderRadius: '4px', width: '100%' }}
            required
          />
        </div>
        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>Title</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            style={{ padding: '0.5rem', background: '#18181b', border: '1px solid #3f3f46', borderRadius: '4px', width: '100%', color: '#e4e4e7' }}
            required
          />
        </div>
        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>Semester</label>
          <input
            type="text"
            placeholder="e.g., Fall 2025"
            value={semester}
            onChange={(e) => setSemester(e.target.value)}
            style={{ padding: '0.5rem', background: '#18181b', border: '1px solid #3f3f46', borderRadius: '4px', width: '100%', color: '#e4e4e7' }}
            required
          />
        </div>
        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>Subject</label>
          <input
            type="text"
            placeholder="e.g., Computer Science"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            style={{ padding: '0.5rem', background: '#18181b', border: '1px solid #3f3f46', borderRadius: '4px', width: '100%', color: '#e4e4e7' }}
            required
          />
        </div>
        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>Professor (Optional)</label>
          <input
            type="text"
            value={professor}
            onChange={(e) => setProfessor(e.target.value)}
            style={{ padding: '0.5rem', background: '#18181b', border: '1px solid #3f3f46', borderRadius: '4px', width: '100%', color: '#e4e4e7' }}
          />
        </div>
        <button
          type="submit"
          style={{ padding: '0.75rem', background: '#3b82f6', border: 'none', borderRadius: '4px', color: 'white', cursor: 'pointer', fontWeight: '500' }}
        >
          Upload
        </button>
        {status && <p style={{ color: '#60a5fa' }}>{status}</p>}
      </form>
    </div>
  )
}
