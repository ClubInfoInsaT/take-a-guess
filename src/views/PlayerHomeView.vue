<template>
  <div class="flex items-center justify-center w-full h-screen relative">
    <alert
      v-if="toast.show"
      class="absolute bottom-0"
      :title="toast.title"
      :description="toast.description"
      :level="toast.alert"
    />
    <div
      class="container flex flex-col items-center justify-center h-full max-w-6xl pl-0 mx-auto sm:pl-8 xl:pl-0 md:flex-row md:justify-between"
    >
      <div
        class="flex flex-col items-center w-5/6 md:items-start sm:w-2/3 lg:w-3/8 lg:mt-10"
      >
        <div>
          <h1
            class="mb-4 text-5xl font-black leading-none text-center text-white lg:text-6xl xl:text-7xl md:text-left capitalize"
          >
            battle royale de la culture générale
          </h1>

          <p
            class="my-3 text-base text-center text-gray-600 xl:text-xl md:text-left"
          >
            Viens affronter tes potes dans une battle royale de questions de
            culture gé commentée et animée
          </p>
        </div>

        <div class="flex gap-4 mt-5">
          <div class="fancy-shadow rounded-3xl">
            <input
              @change="onPseudoChange"
              placeholder="Pseudo"
              class="text-center outline-none w-full h-full px-2 py-3 text-base font-bold bg-white border-2 border-[#5E17EB] rounded-3xl xl:text-xl fold-bold"
            />
          </div>

          <button
            @click="onGoClick"
            class="bg-[#E40495] border-[#5E17EB] border-2 rounded-3xl fancy-shadow"
          >
            <span
              class="text-white w-full h-full px-8 py-3 text-base font-bold xl:text-xl fold-bold uppercase"
              >go</span
            >
          </button>
        </div>
      </div>

      <div
        class="flex flex-col items-center justify-center w-5/6 h-auto mt-10 md:mt-0 md:h-full sm:w-2/3"
      >
        <logo-club-info />
      </div>
    </div>
    <p class="absolute bottom-0 text-white py-4 text-center">
      © 2022 Club Info -
      <a class="underline" href="mailto:club.info@amicale-insat.fr"
        >club.info@amicale-insat.fr</a
      >
    </p>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import Alert from "@/components/Alert.vue";
import LogoClubInfo from "@/components/LogoClubInfo.vue";
import { AlertLevel } from "@/constants/types";

@Component({
  components: {
    Alert,
    LogoClubInfo,
  },
})
export default class PlayerHomeView extends Vue {
  username!: string;

  toast = {
    title: "",
    description: "",
    alert: AlertLevel.SUCCESS,
    show: false,
  };

  // eslint-disable-next-line
  onPseudoChange(event: any) {
    if (event.target.value) {
      this.username = event.target.value;
    }
  }

  /**
   * Ping the server to join the room
   */
  onGoClick() {
    if (this.username) {
      this.$socket.emit("join-room", {
        username: this.username,
      });
    }
  }
  mounted() {
    /**
     * Send the player to the waiting room once he joined the room
     */
    this.sockets.subscribe("join-room", (data) => {
      if (data.status === "success") {
        this.$router.push({
          name: "waiting",
          params: { auto: "true", name: this.username },
        });
      } else {
        this.toast.title = data.status;
        this.toast.description = data.reason;
        this.toast.alert = AlertLevel.DANGER;
        this.toast.show = true;

        setTimeout(() => {
          this.toast.show = false;
        }, 5000);
      }
    });
  }
}
</script>
