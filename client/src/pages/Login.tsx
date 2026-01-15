import { useState } from 'react'
import type { FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import Input from '../components/Input'
import Button from '../components/Button'
import Card from '../components/Card'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [status, setStatus] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    
    try {
      setLoading(true)
      setStatus('')
      
      const res = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password })
      })
      
      if (!res.ok) {
        const error = await res.json()
        setStatus(`✗ ${error.detail || 'Login failed'}`)
        return
      }
      
      const data = await res.json()
      localStorage.setItem('token', data.access_token)
      setStatus('✓ Login successful')
      
      setTimeout(() => {
        navigate('/search')
      }, 500)
    } catch (err) {
      setStatus('✗ Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <div className="mb-8 text-center">
        <h1 className="text-4xl font-bold text-white mb-2">Welcome Back</h1>
        <p className="text-zinc-400">Sign in to access your vault</p>
      </div>
      
      <Card>
        <form onSubmit={handleSubmit} className="flex flex-col gap-6">
          <Input
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="your@email.com"
            required
          />
          
          <Input
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            required
          />
          
          <Button type="submit" disabled={loading}>
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Signing in
              </span>
            ) : (
              'Sign In'
            )}
          </Button>
          
          {status && (
            <div className={`text-sm font-medium text-center ${status.startsWith('✓') ? 'text-green-400' : 'text-red-400'}`}>
              {status}
            </div>
          )}
          
          <div className="text-center text-sm text-zinc-400">
            Don't have an account?{' '}
            <a href="/register" className="text-blue-400 hover:text-blue-300 transition-colors">
              Sign up
            </a>
          </div>
        </form>
      </Card>
    </div>
  )
}
