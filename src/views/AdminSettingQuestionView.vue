<template>
  <div class="flex justify-center p-4 flex-col h-screen">
    <p class="text-center text-5xl py-8 text-white uppercase">
      Paramètres Question {{ question }}
    </p>
    <div class="border-white rounded-xl flex flex-col gap-4 h-full text-center">
      <div class="flex flex-col mx-auto">
        <label class="uppercase md:text-2xl text-lg text-white"
          >Temps de réponse:</label
        >
        <input
          class="py-2 my-2 rounded-xl outline-none text-center text-xl"
          type="number"
          min="1"
          @change="onTimerChange"
        />
        <p class="md:text-2xl text-lg text-white">secondes</p>
      </div>

      <div class="my-8 h-full">
        <p class="uppercase md:text-2xl text-lg text-white">
          Choix de la bonne réponse:
        </p>

        <div class="my-4 grid gap-4 grid-cols-2 h-3/4">
          <answer-button answer="A" :selected="A" @click.native="toggleA()" />
          <answer-button answer="B" :selected="B" @click.native="toggleB()" />
          <answer-button answer="C" :selected="C" @click.native="toggleC()" />
          <answer-button answer="D" :selected="D" @click.native="toggleD()" />
        </div>
      </div>
    </div>
    <div class="flex justify-center">
      <button
        class="px-4 py-2 bg-[#E40495] border-[#5E17EB] border-2 rounded-3xl fancy-shadow"
        @click="onGoClick()"
      >
        <span class="uppercase text-3xl text-white">Go ! </span>
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import AnswerButton from "@/components/AnswerButton.vue";

@Component({
  components: {
    AnswerButton,
  },
})
export default class AdminWaitingRoomView extends Vue {
  private timer!: string;
  A = false;
  B = false;
  C = false;
  D = false;
  rightAnswer = "";
  question = "";

  // eslint-disable-next-line
  onTimerChange(e: any) {
    this.timer = e.target.value;
  }

  toggleA() {
    this.A = !this.A;
    if (this.A) {
      this.rightAnswer = "A";
      this.B = false;
      this.C = false;
      this.D = false;
    }
  }

  toggleB() {
    this.B = !this.B;
    if (this.B) {
      this.rightAnswer = "B";
      this.A = false;
      this.C = false;
      this.D = false;
    }
  }

  toggleC() {
    this.C = !this.C;
    if (this.C) {
      this.rightAnswer = "C";
      this.A = false;
      this.B = false;
      this.D = false;
    }
  }

  toggleD() {
    this.D = !this.D;
    if (this.D) {
      this.rightAnswer = "D";
      this.A = false;
      this.B = false;
      this.C = false;
    }
  }

  onGoClick() {
    if (this.rightAnswer && this.timer) {
      this.$socket.emit("set-question-settings", {
        answer: this.rightAnswer,
        timer: this.timer,
      });
    } else {
      console.log("A: ", this.rightAnswer, "T:", this.timer);
    }
  }

  mounted() {
    this.$socket.emit("get-game-info");

    this.sockets.subscribe("get-game-info", (data) => {
      this.question = data.question;
    });

    this.sockets.subscribe("set-question-settings-response", (data) => {
      console.log("Data: ", data);
      if (data.status === "success") {
        this.$router.push({
          name: "admin-stats",
          params: { auto: "true" },
        });
      }
      // TODO: Show error to the admin
    });
  }
}
</script>
