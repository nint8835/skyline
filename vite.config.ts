import { heyApiPlugin } from '@hey-api/vite-plugin';
import react from '@vitejs/plugin-react';
import path from 'path';
import { defineConfig } from 'vite';

// https://vitejs.dev/config/
export default defineConfig({
    root: 'frontend',
    plugins: [
        react(),
        heyApiPlugin({
            vite: {
                apply: 'serve',
            },
            config: {
                input: 'http://localhost:8000/openapi.json',
                output: 'frontend/src/queries/api',
                plugins: [
                    {
                        name: '@hey-api/client-fetch',
                        baseUrl: false,
                    },
                    '@hey-api/typescript',
                    'zod',
                    {
                        name: '@hey-api/sdk',
                        validator: true,
                    },
                    {
                        name: '@tanstack/react-query',
                        includeInEntry: true,
                        useQuery: true,
                        useMutation: true,
                        mutationKeys: true,
                    },
                ],
            },
        }),
    ],
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
