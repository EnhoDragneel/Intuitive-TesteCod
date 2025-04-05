import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/HomeView.vue'
import Operadoras from '../views/OperadorasView.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/operadoras', name: 'Operadoras', component: Operadoras }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
