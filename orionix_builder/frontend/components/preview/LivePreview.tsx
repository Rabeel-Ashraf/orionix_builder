import { useState } from 'react'
import { RefreshCw, Smartphone, Tablet, Monitor } from 'lucide-react'

export function LivePreview() {
  const [device, setDevice] = useState<'mobile' | 'tablet' | 'desktop'>('desktop')
  
  const deviceSizes = {
    mobile: 'w-80',
    tablet: 'w-96', 
    desktop: 'w-full'
  }

  return (
    <div className="glass-effect p-6 rounded-2xl">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-white">Live Preview</h3>
        <div className="flex items-center space-x-2">
          <button className="p-2 hover:bg-slate-700 rounded transition">
            <RefreshCw className="h-4 w-4 text-gray-300" />
          </button>
          <div className="flex bg-slate-800 rounded-lg p-1">
            <button
              onClick={() => setDevice('mobile')}
              className={`p-2 rounded ${device === 'mobile' ? 'bg-purple-600' : 'hover:bg-slate-700'}`}
            >
              <Smartphone className="h-4 w-4 text-white" />
            </button>
            <button
              onClick={() => setDevice('tablet')}
              className={`p-2 rounded ${device === 'tablet' ? 'bg-purple-600' : 'hover:bg-slate-700'}`}
            >
              <Tablet className="h-4 w-4 text-white" />
            </button>
            <button
              onClick={() => setDevice('desktop')}
              className={`p-2 rounded ${device === 'desktop' ? 'bg-purple-600' : 'hover:bg-slate-700'}`}
            >
              <Monitor className="h-4 w-4 text-white" />
            </button>
          </div>
        </div>
      </div>

      <div className={`${deviceSizes[device]} h-96 mx-auto bg-white rounded-lg border-4 border-gray-800 overflow-hidden`}>
        <div className="w-full h-full flex items-center justify-center text-gray-500">
          Preview will appear here
        </div>
      </div>
    </div>
  )
}
