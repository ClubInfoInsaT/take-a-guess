import Vue from "vue";
import App from "./App.vue";
import router from "./router";

import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faCheck,
  faHeart as fasHeart,
  faInfo,
  faTriangleExclamation,
  faXmark,
} from "@fortawesome/free-solid-svg-icons";
import { faHeart as farHeart } from "@fortawesome/free-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import VueApexCharts from "vue-apexcharts";
import VueSocketIO from "vue-socket.io";

import "./assets/tailwind.css";

Vue.config.productionTip = false;
library.add(faCheck);
library.add(fasHeart);
library.add(farHeart);
library.add(faInfo);
library.add(faTriangleExclamation);
library.add(faXmark);

// eslint-disable-next-line vue/multi-word-component-names
Vue.component("apexchart", VueApexCharts);
Vue.component("font-awesome-icon", FontAwesomeIcon);

Vue.use(VueApexCharts);

Vue.use(
  new VueSocketIO({
    debug: true,
    connection: "http://localhost:8000",
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    // options: {
    //   path: "/~leban/blanket/",
    // },
  })
);

new Vue({
  router,
  render: (h) => h(App),
  components: {},
  sockets: {
    connect: () => {
      console.log("Connected");
    },
    adminDisconnect: () => {
      console.log("The admin leave the room...");
      router.push({ name: "home", params: { auto: "true" } });
    },
    disconnect: () => {
      console.log("You've been disconnected...");
      router.push({
        name: "home",
        params: { auto: "true" },
      });
    },
  },
}).$mount("#app");
