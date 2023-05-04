import { createRouter, createWebHistory } from "vue-router";
import BusinessSignUp from "../views/businessuser/BusinessSignUp.vue";
import DefaultSignUp from "../views/defaultuser/DefaultSignUp.vue";
import Dashboard from "../views/dashboard/Dashboard.vue";
import TweetDetail from "../views/dashboard/TweetDetail.vue";
import AddTweet from "../views/dashboard/AddTweet.vue";
import UserProfile from "../views/dashboard/UserProfile.vue";
import EditUserProfile from "../views/dashboard/EditUserProfile.vue";
import store from "../store"
import Login from "../views/Login.vue";

const routes = [
  // {
  //   path: "/",
  //   name: "home",
  //   component: HomeView,
  // },
  {
    path: "/business-sign-up",
    name: "business-sign-up",
    component: BusinessSignUp,
  },
  {
    path: "/default-sign-up",
    name: "default-sign-up",
    component: DefaultSignUp,
  },
  {
    path: "/login",
    name: "login",
    component: Login,
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: Dashboard,
    // meta: {
    //   requireLogin: true
    // }
  },
  {
    path: "/dashboard/user-profile",
    name: "user-profile",
    component: UserProfile,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/tweet/:id',
    name: 'TweetDetail',
    component: TweetDetail,
    // meta: {
    //   requireLogin: true
    // }
  },
  {
    path: '/dashboard/add-tweet/',
    name: 'AddTweet',
    component: AddTweet,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/user-profile/edit/:id',
    name: 'EditUserProfile',
    component: EditUserProfile,
    meta: {
      requireLogin: true
    }
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// proveravamo da li u state ima isAuthenticated i da li je required login i onda ako nije tacno
// saljemo ga na login
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router;
