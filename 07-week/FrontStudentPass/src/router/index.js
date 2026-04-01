import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../pages/HomePage.vue";
import CatalogPage from "../pages/CatalogPage.vue";
import HowItWorksPage from "../pages/HowItWorksPage.vue";

const routes = [
  { path: "/", name: "home", component: HomePage },
  { path: "/catalog", name: "catalog", component: CatalogPage },
  { path: "/how-it-works", name: "how-it-works", component: HowItWorksPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
