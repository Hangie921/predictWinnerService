import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: ["707d-2001-b400-e387-ccb1-1876-70c5-e595-9cd4.ngrok-free.app"],
  }
})
