import { useState } from 'react'
import type { FormEvent } from 'react'
import Input from '../components/Input'
import Button from '../components/Button'
import Card from '../components/Card'

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
      setStatus(`✓ Uploaded: ${data.title}`)
      setFile(null)
      setTitle('')
      setSemester('')
      setSubject('')
      setProfessor('')
    } catch (err) {
      setStatus('✗ Upload failed')
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">Upload Notes</h1>
        <p className="text-zinc-400">Share your study materials with the vault</p>
      </div>
      <Card>
        <form onSubmit={handleSubmit} className="flex flex-col gap-6">
          <Input
            label="PDF File"
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            required
          />
          <Input
            label="Title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter note title"
            required
          />
          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Semester"
              type="text"
              placeholder="e.g., Fall 2025"
              value={semester}
              onChange={(e) => setSemester(e.target.value)}
              required
            />
            <Input
              label="Subject"
              type="text"
              placeholder="e.g., Computer Science"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              required
            />
          </div>
          <Input
            label="Professor (Optional)"
            type="text"
            value={professor}
            onChange={(e) => setProfessor(e.target.value)}
            placeholder="Professor name"
          />
          <Button type="submit">Upload to Vault</Button>
          {status && (
            <div className={`text-sm font-medium ${status.startsWith('✓') ? 'text-green-400' : status.startsWith('✗') ? 'text-red-400' : 'text-blue-400'}`}>
              {status}
            </div>
          )}
        </form>
      </Card>
    </div>
  )
}
