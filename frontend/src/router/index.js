import { createRouter, createWebHistory } from 'vue-router'

import MainLayout from '../layouts/MainLayout.vue'
import AdminLayout from '../layouts/AdminLayout.vue'
import HomeView from '../views/HomeView.vue'
import CatalogView from '../views/CatalogView.vue'
import HowItWorksView from '../views/HowItWorksView.vue'
import ProductView from '../views/ProductView.vue'
import NotFoundView from '../views/NotFoundView.vue'
import AdminDashboardView from '../views/admin/AdminDashboardView.vue'
import AdminApplicationsView from '../views/admin/AdminApplicationsView.vue'
import AdminManagersView from '../views/admin/AdminManagersView.vue'
import AdminStatisticsView from '../views/admin/AdminStatisticsView.vue'
import ManagerLayout from '../layouts/ManagerLayout.vue'
import ManagerDiscountsView from '../views/manager/ManagerDiscountsView.vue'
import ManagerCreateDiscountView from '../views/manager/ManagerCreateDiscountView.vue'
import ManagerStatisticsView from '../views/manager/ManagerStatisticsView.vue'
import { useSession } from '../composables/useSession'

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '',
        name: 'home',
        component: HomeView,
      },
      {
        path: 'catalog',
        name: 'catalog',
        component: CatalogView,
      },
      {
        path: 'how',
        name: 'how',
        component: HowItWorksView,
      },
      {
        path: 'product/:id',
        name: 'product',
        component: ProductView,
      },
    ],
  },
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAdmin: true },
    children: [
      {
        path: '',
        name: 'admin-dashboard',
        component: AdminDashboardView,
      },
      {
        path: 'applications',
        name: 'admin-applications',
        component: AdminApplicationsView,
      },
      {
        path: 'managers',
        name: 'admin-managers',
        component: AdminManagersView,
      },
      {
        path: 'statistics',
        name: 'admin-statistics',
        component: AdminStatisticsView,
      },
    ],
  },
  {
    path: '/manager',
    component: ManagerLayout,
    meta: { requiresManager: true },
    children: [
      {
        path: '',
        redirect: { name: 'manager-discounts' },
      },
      {
        path: 'discounts',
        name: 'manager-discounts',
        component: ManagerDiscountsView,
      },
      {
        path: 'discounts/create',
        name: 'manager-discount-create',
        component: ManagerCreateDiscountView,
      },
      {
        path: 'statistics',
        name: 'manager-statistics',
        component: ManagerStatisticsView,
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  const { user, readStorage } = useSession()
  readStorage()
  if (to.matched.some((r) => r.meta.requiresAdmin)) {
    if (!user.value || user.value.role !== 'admin') {
      return { name: 'home' }
    }
  }
  if (to.matched.some((r) => r.meta.requiresManager)) {
    if (!user.value || user.value.role !== 'manager') {
      return { name: 'home' }
    }
  }
})

export default router
