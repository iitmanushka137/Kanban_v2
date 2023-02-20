import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import LoginPage from '../components/LoginPage.vue'
import RegisterPage from '../components/RegisterPage.vue'
import ListAdding from '../components/ListAdding.vue'
import UpdateList from '../components/UpdateList.vue'
import DeleteList from '../components/DeleteList.vue'
import SummaryPg from '../components/SummaryPg.vue'
import CardDelete from '../components/CardDelete.vue'
import CadrdAdding from '../components/CardAdding.vue'
import CardUpdating from '../components/CardUpdating.vue'

const routes = [
  {
    path: '/',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage
  },
  {
    path: '/home',
    name: 'home',
    component: HomePage
  },
  {
    path: '/addlist',
    name: 'listadding',
    component: ListAdding
  },
  {
    path: '/updateList/:id',
    name: 'listupdating',
    component: UpdateList
  },
  {
    path: '/delList/:id',
    name: 'delList',
    component: DeleteList
  },
  {
    path: '/addcard/:lid',
    name: 'cardadd',
    component: CadrdAdding
  },
  {
    path: '/updateCard/:cid',
    name: 'cardupd',
    component: CardUpdating
  },
  {
    path: '/delCard/:id',
    name: 'delCard',
    component: CardDelete
  },
  {
    path: '/summary',
    name: 'summary',
    component: SummaryPg
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
