import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3003,
    proxy: {
      '/api': 'http://localhost:5003',
      '/health': 'http://localhost:5003',
      '/metrics': 'http://localhost:5003'
    }
  }
})

