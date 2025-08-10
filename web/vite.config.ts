import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vite.dev/config/
export default defineConfig({
  plugins: [svelte()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: (id=>{
          // if (id
          //     .includes
          //     ('svelte@')) {
          //   return 'svelte';
          // }
          if (id
              .includes
              ('node_modules')) {
            return 'vendor';
          }
          if (id.includes('total_data.json')) {
            return 'data'
          }

          return null;
        })
      }
    }
  }
})
