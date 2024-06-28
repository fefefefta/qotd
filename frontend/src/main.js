import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import 'tailwindcss/tailwind.css'
import 'daisyui/dist/full.css'
import router from './router'
// import './index.css'

const app = createApp(App)
app.use(router)
app.mount('#app')