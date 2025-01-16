import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
    base:
        mode == "development"
            ? "http://localhost:5173/"
            : "/static/api/spa/",
    build: {
        emptyOutDir: true,
        outDir: "../api/static/api/spa",
    },
    plugins: [vue(),
        {
            name: "inject-csrf-token",
            transformIndexHtml(html) {
                return html.replace(
                    "</head>",
                    `<script>window.CSRF_TOKEN = "{{ csrf_token }}";</script>\n</head>`
                );
            },
        }
    ],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
}));
