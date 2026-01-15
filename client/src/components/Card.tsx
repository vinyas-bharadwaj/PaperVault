import type { ReactNode } from 'react'

interface CardProps {
  children: ReactNode
}

export default function Card({ children }: CardProps) {
  return (
    <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-8 backdrop-blur-sm shadow-xl">
      {children}
    </div>
  )
}
