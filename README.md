# flask-vite

Example of integration for Flask and Vite (Vue 3) - Multi-Page App. 

### Vite config

```javascript
import { defineConfig } from 'vite';
import { resolve } from 'node:path';
import { fileURLToPath, URL } from 'node:url';
import vue from '@vitejs/plugin-vue';

export default defineConfig(({ mode }) => {
  return {
    plugins: [vue()],
    root: resolve('./'),
    base: mode === 'production' ? '/static/dist/' : '/',
    appType: 'mpa',
    build: {
      target: 'esnext',
      outDir: resolve('./static/dist'),
      assetsDir: '',
      manifest: true,
      sourcemap: true,
      publicDir: false,
      emptyOutDir: true,
      rollupOptions: {
        input: {
          home: resolve(__dirname, 'src/pages/home/home.js'),
          library: resolve(__dirname, 'src/pages/library/library.js'),
          gallery: resolve(__dirname, 'src/pages/gallery/gallery.js'),
        },
      },
    },
    server: {
      host: 'localhost',
      port: 5173,
      strictPort: true,
      open: false,
      origin: 'http://localhost:8000',
    },
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
  }
});
```


### Inspired by 
`fastapi-vite` @ [https://github.com/cofin/fastapi-vite] \
`flask_vite` @ [https://github.com/damonchen/flask_vite]
