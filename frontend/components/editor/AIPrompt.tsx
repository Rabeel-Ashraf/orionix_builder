import { useState } from 'react'
import { Send, Sparkles } from 'lucide-react'

export function AIPrompt() {
  const [prompt, setPrompt] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!prompt.trim()) return

    setIsGenerating(true)
    // AI generation logic here
    console.log('Generating with prompt:', prompt)
    setTimeout(() => setIsGenerating(false), 2000)
  }

  return (
    <div className="glass-effect p-6 rounded-2xl">
      <div className="flex items-center space-x-2 mb-4">
        <Sparkles className="h-5 w-5 text-purple-400" />
        <h3 className="text-lg font-semibold text-white">AI Assistant</h3>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describe the website you want to create... (e.g., 'A modern portfolio with dark theme and 3D elements')"
          className="w-full h-32 px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
        />
        
        <button
          type="submit"
          disabled={isGenerating || !prompt.trim()}
          className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-slate-600 text-white py-3 px-4 rounded-lg font-semibold transition flex items-center justify-center space-x-2"
        >
          {isGenerating ? (
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
          ) : (
            <Send className="h-5 w-5" />
          )}
          <span>{isGenerating ? 'Generating...' : 'Generate with AI'}</span>
        </button>
      </form>

      <div className="mt-4 text-sm text-gray-400">
        <p>💡 Tip: Be specific about colors, layout, and features for better results.</p>
      </div>
    </div>
  )
}
