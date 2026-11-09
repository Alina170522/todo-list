import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// base: './' — относительные пути, чтобы сайт открывался на GitHub Pages
// по адресу вида https://<логин>.github.io/<репозиторий>/
export default defineConfig({
  plugins: [vue()],
  base: './',
})
