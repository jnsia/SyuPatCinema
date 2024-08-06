import { createRouter, createWebHistory } from "vue-router";

import HomeView from "@/views/common/HomeView.vue";
import NotFoundView from "@/views/common/NotFoundView.vue"

import LoginView from "@/views/accounts/LoginView.vue";
import SignupView from "@/views/accounts/SignupView.vue";
import ProfileView from "@/views/accounts/ProfileView.vue";
import ProfileUpdateView from "@/views/accounts/ProfileUpdateView.vue";

import MovieDetailView from "@/views/movies/MovieDetailView.vue";
import MoviesView from "@/views/movies/MoviesView.vue";

import TicketingView from "@/views/ticketing/TicketingView.vue"
import SeatView from "@/views/ticketing/SeatView.vue"

import { useAccountsStore } from "@/stores/accounts.js"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/signup",
      name: "signup",
      component: SignupView,
    },
    {
      path: "/detail/:id",
      name: "detail",
      component: MovieDetailView,
    },
    {
      path: "/profile/:id",
      name: "profile",
      component: ProfileView,
    },
    {
      path: "/profile/update/:id",
      name: "profileUpdate",
      component: ProfileUpdateView,
    },
    {
      path: "/ticketing",
      name: "ticketing",
      component: TicketingView,
    },
    {
      path: "/seat",
      name: "seat",
      component: SeatView,
    },
    {
      path: "/movies",
      name: "movies",
      component: MoviesView,
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFoundView,
    },
  ],
});

router.beforeEach((to, from) => {
  const store = useAccountsStore()

  if ((to.name == 'ticketing' || to.name == 'seat') && (store.token === null)) {
    return {name: 'NotFound'}
  }
})

export default router;
