import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import SignupView from "../views/SignupView.vue";
import MovieDetailView from "../views/MovieDetailView.vue";
import ProfileView from "../views/ProfileView.vue";
import ProfileUpdateView from "../views/ProfileUpdateView.vue";
import MoviesView from "../views/MoviesView.vue";
import TicketingView from "../views/Ticketing/TicketingView.vue"
import SeatView from "../views/Ticketing/SeatView.vue"
import NotFoundView from "../views/NotFoundView.vue"
import { useCounterStore } from "../stores/counter.js"

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
  const store = useCounterStore()

  if ((to.name == 'ticketing' || to.name == 'seat') && (store.token === null)) {
    return {name: 'NotFound'}
  }
})

export default router;
