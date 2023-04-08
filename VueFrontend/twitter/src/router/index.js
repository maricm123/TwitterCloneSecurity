import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import BusinessSignUp from "../views/businessuser/BusinessSignUp.vue";
import DefaultSignUp from "../views/defaultuser/DefaultSignUp.vue";
import Dashboard from "../views/dashboard/Dashboard.vue";
import UserProfile from "../views/dashboard/UserProfile.vue";

import Login from "../views/Login.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
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
  },
  {
    path: "/dashboard/user-profile",
    name: "user-profile",
    component: UserProfile,
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
