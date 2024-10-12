import react from '@vitejs/plugin-react';
import path from 'path';
import { defineConfig } from 'vite';

// https://vitejs.dev/config/
export default defineConfig({
    root: 'frontend',
    plugins: [react()],
    server: {
        proxy: {
            '/auth': {
                target: 'http://127.0.0.1:8000',
            },
            '/contributions': {
                target: 'http://127.0.0.1:8000',
            },
        },
    },
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './frontend/src'),
        },
    },
});
