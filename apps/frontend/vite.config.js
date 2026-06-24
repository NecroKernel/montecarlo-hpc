import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 4173,
    watch: {
      usePolling: true // Helps Vite track changes inside a Docker volume
    }
  }
})