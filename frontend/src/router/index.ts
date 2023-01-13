import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/news',
    name: 'news',
    component: () => import(/* webpackChunkName: "about" */ '../views/NewsView.vue'),
    meta:{
      keepAlive:true,
    },
  },
  {
    path:'/news/:id',
    name: 'newstwo',
    component: () => import('../views/NewstwoView.vue'),
  },
  {
    path: '/search/:id',
    name: 'search',
    component: () => import(/* webpackChunkName: "about" */ '../views/SearchView.vue'),
  },
  {
    path: '/social',
    name: 'social',
    component: () => import(/* webpackChunkName: "about" */ '../views/SocialView.vue'),
  },
  {
    path: '/social/:id',
    name: 'socialtwo',
    component: () => import(/* webpackChunkName: "about" */ '../views/SocialtwoView.vue')
  },
  {
    path: '/edit/:id',
    name: 'edit',
    component: () => import(/* webpackChunkName: "about" */ '../views/EditPostView.vue')
  },
  {
    path: '/editreply/:id',
    name: 'editreply',
    component: () => import(/* webpackChunkName: "about" */ '../views/EditReplyView.vue')
  },
  {
    path: '/send',
    name: 'send',
    component: () => import(/* webpackChunkName: "about" */ '../views/SendPostView.vue'),
    meta: {
      name: "referrer",
      content: "no-referrer" 
    }
  },
  {
    path: '/person',
    name: 'person',
    component: () => import(/* webpackChunkName: "about" */ '../views/PersonView.vue')
  },
  {
    path: '/message',
    name: 'message',
     meta: {
      // isLogin: true,
    },
    component: () => import(/* webpackChunkName: "about" */ '../views/MessageView.vue')
  },
  {
    path: '/food',
    name: 'food',
    component: () => import(/* webpackChunkName: "about" */ '../views/FoodView.vue')
  },
  {
    path: '/forget',
    name: 'forget',
    component: () => import(/* webpackChunkName: "about" */ '../views/ForgetView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
    if(to.path === '/message' || to.path === '/social' )
    {
        const jwt = localStorage.getItem('jwt');
        if(jwt)
        {
            next();
        }
        else
        {
            next({path:'/person',})
        }
    }
    else{next()}
});

export default router
