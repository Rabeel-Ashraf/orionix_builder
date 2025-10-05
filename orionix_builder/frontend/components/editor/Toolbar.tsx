import { Square, Circle, Type, Image, Video } from 'lucide-react'

const tools = [
  { icon: Square, name: 'Rectangle', action: 'add-rectangle' },
  { icon: Circle, name: 'Circle', action: 'add-circle' },
  { icon: Type, name: 'Text', action: 'add-text' },
  { icon: Image, name: 'Image', action: 'add-image' },
  { icon: Video, name: 'Video', action: 'add-video' },
]

export function Toolbar() {
  return (
    <div className="glass-effect p-4 rounded-2xl">
      <h3 className="text-white font-semibold mb-4">Elements</h3>
      <div className="grid grid-cols-2 gap-3">
        {tools.map((tool) => (
          <button
            key={tool.name}
            className="p-3 bg-slate-800 hover:bg-slate-700 rounded-lg transition flex flex-col items-center space-y-2"
            onClick={() => console.log(`Add ${tool.name}`)}
          >
            <tool.icon className="h-5 w-5 text-white" />
            <span className="text-xs text-gray-300">{tool.name}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
