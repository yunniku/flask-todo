import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: '../static/dist',
    emptyOutDir: true
  },
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:5001',
      '/google': 'http://127.0.0.1:5001',
      '/calendar': 'http://127.0.0.1:5001'
    }
  }
})