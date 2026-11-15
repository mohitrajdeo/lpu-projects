import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3002,
    proxy: {
      '/api': 'http://localhost:5002',
      '/health': 'http://localhost:5002',
      '/metrics': 'http://localhost:5002'
    }
  }
})

