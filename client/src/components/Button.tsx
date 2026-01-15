import type { ButtonHTMLAttributes, ReactNode } from 'react'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode
  variant?: 'primary' | 'secondary'
}

export default function Button({ children, variant = 'primary', ...props }: ButtonProps) {
  return (
    <button
      {...props}
      className={`px-6 py-3 rounded-lg font-medium transition-all ${
        variant === 'primary'
          ? 'bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/20 hover:shadow-blue-500/30 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-blue-600'
          : 'bg-zinc-800 hover:bg-zinc-700 text-white'
      }`}
    >
      {children}
    </button>
  )
}
