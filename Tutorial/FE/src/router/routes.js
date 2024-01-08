
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      {
        path: 'ban-do',
        name: 'ban-do',
        component: () => import('components/ol/MapComponent.vue')
      },
      {
        path: 'du-lieu-diem',
        name: 'du-lieu-diem',
        component: () => import('pages/DuLieuDiem.vue')
      },
      {
        path: 'du-lieu-duong',
        name: 'du-lieu-duong',
        component: () => import('pages/DuLieuDuong.vue')
      },
      {
        path: 'du-lieu-vung',
        name: 'du-lieu-vung',
        component: () => import('pages/DuLieuVung.vue')
      }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
