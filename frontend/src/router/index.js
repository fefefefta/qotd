import { createRouter, createWebHistory } from 'vue-router';
import Today from '../views/Today.vue';
import About from '../views/About.vue';

const routes = [
  {
    path: '/',
    name: 'today',
    component: Today,
  },
  {
    path: '/about',
    name: 'about',
    component: About
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router