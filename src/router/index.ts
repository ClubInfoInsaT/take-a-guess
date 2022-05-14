import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";

import PlayeyHomeView from "@/views/PlayerHomeView.vue";
import PlayerWaitingRoomView from "@/views/PlayerWaitingRoomView.vue";
import PlayerBeReadyView from "@/views/PlayerBeReadyView.vue";
import PlayerQuizzView from "@/views/PlayerQuizzView.vue";
import PlayerStatsView from "@/views/PlayerStatsView.vue";

import AdminWaitingRoomView from "@/views/AdminWaitingRoomView.vue";
import AdminSettingQuestionView from "@/views/AdminSettingQuestionView.vue";
import AdminStatsView from "@/views/AdminStatsView.vue";
import AdminHomeView from "@/views/AdminHomeView.vue";

import LeaderboardView from "@/views/LeaderboardView.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "home",
    component: PlayeyHomeView,
    beforeEnter: (to, from, next) => {
      if (from.name === null) next();
      else if (from.name !== "waiting") from.name !== "waiting" && next(false);
    },
  },
  {
    path: "/waiting",
    name: "waiting",
    component: PlayerWaitingRoomView,
    beforeEnter: (to, from, next) => {
      from.name !== "beReady" ? next() : next(false);
    },
  },
  {
    path: "/be-ready",
    name: "beReady",
    component: PlayerBeReadyView,
  },
  {
    path: "/quizz",
    name: "quizz",
    component: PlayerQuizzView,
    beforeEnter: (to, from, next) => {
      from.name !== "stats" ? next() : next(false);
    },
  },
  {
    path: "/stats",
    name: "stats",
    component: PlayerStatsView,
    beforeEnter: (to, from, next) => {
      from.name !== "leaderboard" ? next() : next(false);
    },
  },
  {
    path: "/leaderboard",
    name: "leaderboard",
    component: LeaderboardView,
  },
  {
    path: "/admin-home",
    name: "admin-home",
    component: AdminHomeView,
    beforeEnter: (to, from, next) => {
      from.name !== "admin-waiting" ? next() : next(false);
    },
  },
  {
    path: "/admin-waiting",
    name: "admin-waiting",
    component: AdminWaitingRoomView,
    beforeEnter: (to, from, next) => {
      from.name !== "admin-question-settings" ? next() : next(false);
    },
  },
  {
    path: "/admin-question-settings",
    name: "admin-question-settings",
    component: AdminSettingQuestionView,
  },
  {
    path: "/admin-stats",
    name: "admin-stats",
    component: AdminStatsView,
  },
];

const router = new VueRouter({
  mode: "hash", // mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
