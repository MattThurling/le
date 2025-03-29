import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  build: {
    outDir: '../static/dist',  // Output directory for Django to use
    emptyOutDir: true,
    rollupOptions: {
      input: [
        './src/main.js',
         './src/templates/website/index.html',
      ],
      // Since Python collectstatic handles manifests, there is no need to add unique ids
      output: {
        entryFileNames: 'assets/[name].js',
        chunkFileNames: 'assets/[name].js',
        assetFileNames: 'assets/[name][extname]'
      }
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8000'
    }
  }
})