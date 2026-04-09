import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const isVitest = process.env.VITEST === 'true';

export default defineConfig({
  plugins: [isVitest ? null : react()].filter(Boolean),
  base: '/',
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '/api'),
      },
    },
  },
  test: {
    environment: 'jsdom',
    globals: true,
    css: true,
    setupFiles: './vitest.setup.js',
  },
  build: {
    chunkSizeWarningLimit: 800,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (!id.includes('node_modules')) {
            return;
          }
          if (id.includes('react') || id.includes('scheduler')) {
            return 'react-vendor';
          }
          if (id.includes('react-router')) {
            return 'router-vendor';
          }
          if (id.includes('chart.js') || id.includes('react-chartjs-2')) {
            return 'chart-vendor';
          }
          if (id.includes('@fortawesome')) {
            return 'icons-vendor';
          }
          if (id.includes('@emailjs')) {
            return 'email-vendor';
          }
          return 'vendor';
        },
      },
    },
  },
});
