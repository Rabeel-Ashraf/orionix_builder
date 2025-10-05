import { useState } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, Plus, Settings, CreditCard, LogOut } from 'lucide-react'

export default function Dashboard() {
  const [projects, setProjects] = useState([
    { id: 1, name: 'Portfolio Website', lastModified: '2 hours ago' },
    { id: 2, name: 'E-commerce Store', lastModified: '1 day ago' },
    { id: 3, name: 'Blog Platform', lastModified: '3 days ago' },
  ])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Navigation */}
      <nav className="glass-effect">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-2">
              <Sparkles className="h-8 w-8 text-purple-400" />
              <span className="text-xl font-bold text-white">Orionix Builder</span>
            </div>
            <div className="flex items-center space-x-4">
              <button className="text-gray-300 hover:text-white transition">
                <CreditCard className="h-5 w-5" />
              </button>
              <button className="text-gray-300 hover:text-white transition">
                <Settings className="h-5 w-5" />
              </button>
              <button className="text-gray-300 hover:text-white transition">
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-white mb-2">Dashboard</h1>
          <p className="text-gray-300">Welcome back! Manage your projects and credits.</p>
        </motion.div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="glass-effect p-6 rounded-2xl"
          >
            <h3 className="text-gray-300 text-sm font-medium mb-2">Credits Available</h3>
            <p className="text-3xl font-bold text-white">42</p>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="glass-effect p-6 rounded-2xl"
          >
            <h3 className="text-gray-300 text-sm font-medium mb-2">Active Projects</h3>
            <p className="text-3xl font-bold text-white">{projects.length}</p>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="glass-effect p-6 rounded-2xl"
          >
            <h3 className="text-gray-300 text-sm font-medium mb-2">Plan</h3>
            <p className="text-3xl font-bold text-white">Free</p>
          </motion.div>
        </div>

        {/* Projects Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="glass-effect p-6 rounded-2xl"
        >
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-white">Your Projects</h2>
            <button className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg font-semibold transition flex items-center space-x-2">
              <Plus className="h-4 w-4" />
              <span>New Project</span>
            </button>
          </div>

          <div className="grid gap-4">
            {projects.map((project) => (
              <div
                key={project.id}
                className="bg-slate-800 hover:bg-slate-700 p-4 rounded-lg transition cursor-pointer"
              >
                <h3 className="text-white font-semibold mb-1">{project.name}</h3>
                <p className="text-gray-400 text-sm">Last modified {project.lastModified}</p>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}
