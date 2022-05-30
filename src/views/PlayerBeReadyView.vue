<template>
  <div
    class="flex justify-center items-center p-4 flex-col h-screen container mx-auto"
  >
    <p class="text-center text-2xl py-1 text-white uppercase">Prêts ?</p>
    <p class="text-center text-4xl py-1 text-white uppercase">
      Question {{ question }}
    </p>
    <hearts
      class="md:w-1/2 my-4"
      :left="heartsLeft"
      :total="hearts"
      :name="name"
    />
    <p
      class="text-center text-4xl py-1 text-white uppercase"
      v-if="heartsLeft === 0"
    >
      Mode spectateur
    </p>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Hearts from "@/components/Hearts.vue";
@Component({
  components: {
    Hearts,
  },
})
export default class BeReadyView extends Vue {
  question = "";
  hearts = 0;
  heartsLeft = 0;
  name = "N/A";

  mounted() {
    this.$socket.emit("get-player-info");
    this.sockets.subscribe("get-player-info", (data) => {
      this.hearts = parseInt(data.hearts);
      this.heartsLeft = parseInt(data.left);
      this.question = data.question;
      this.name = data.name;
    });
    this.sockets.subscribe("question-start", (data) => {
      this.$router.push({
        name: "quizz",
        params: {
          timer: data.timer,
          hearts: this.hearts.toString(),
          heartsLeft: this.heartsLeft.toString(),
          question: this.question,
          auto: "true",
        },
      });
    });
  }
}
</script>
