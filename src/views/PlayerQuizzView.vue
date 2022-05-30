<template>
  <div class="flex justify-center p-4 flex-col h-screen">
    <hearts
      :left="heartsLeft"
      :total="hearts"
      :name="name"
      v-if="hearts !== -1 && heartsLeft !== -1"
    />
    <p class="text-center text-5xl py-8 text-white uppercase">
      Question {{ question }}
    </p>
    <div class="grid gap-4 grid-cols-2 h-3/4">
      <answer-button
        answer="A"
        :selected="selectedAnswer === 'A'"
        @click.native="!hasAnswered && setAnswer('A')"
      />
      <answer-button
        answer="B"
        :selected="selectedAnswer === 'B'"
        @click.native="!hasAnswered && setAnswer('B')"
      />
      <answer-button
        answer="C"
        :selected="selectedAnswer === 'C'"
        @click.native="!hasAnswered && setAnswer('C')"
      />
      <answer-button
        answer="D"
        :selected="selectedAnswer === 'D'"
        @click.native="!hasAnswered && setAnswer('D')"
      />
    </div>

    <div class="flex justify-center items-center h-1/4 m-4">
      <circle-progress
        :class="hasAnswered ? 'hidden' : 'block'"
        class="text-[#5E17EB]"
        :percent="100 * (1 - (maxTime - timeLeft) / maxTime)"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Hearts from "@/components/Hearts.vue";
import AnswerButton from "@/components/AnswerButton.vue";
import CircleProgress from "@/components/CircleProgress.vue";

@Component({
  components: {
    AnswerButton,
    CircleProgress,
    Hearts,
  },
})
export default class QuizzView extends Vue {
  hearts = -1; // Total hearts available
  heartsLeft = -1; // Player's hearts left
  question = ""; // The number of question
  hasAnswered = false; // Whether or not the player answered the question
  selectedAnswer = ""; // The player's selected answer
  maxTime = 0; // Time to answer the question
  timeLeft = Number.MAX_VALUE;
  startTime!: number;
  intervalId!: number;
  name = "N/A";

  /**
   * When the component is mounted
   */
  mounted() {
    this.startTime = new Date().getTime();

    this.intervalId = setInterval(() => {
      this.timeLeft =
        this.maxTime - (new Date().getTime() - this.startTime) / 1000;
      if (this.timeLeft <= 0) {
        clearInterval(this.intervalId);
        this.giveAnswer();
      }
    }, 1000);

    this.$socket.emit("get-player-info");
    this.sockets.subscribe("get-player-info", (data) => {
      this.hearts = parseInt(data.hearts);
      this.heartsLeft = data.left;
      this.maxTime = data.timer;
      this.question = data.question;
      this.name = data.name;
    });

    this.sockets.subscribe("question-stats", (data) => {
      this.$router.push({
        name: "stats",
        params: {
          dead: data.dead,
          alive: data.alive,
          auto: "true",
        },
      });
    });

    this.sockets.subscribe("show-leaderboard", () => {
      this.$router.push({
        name: "leaderboard",
        params: { auto: "true" },
      });
    });

    this.sockets.subscribe("next-question", () => {
      this.$router.push({
        name: "beReady",
        params: { auto: "true" },
      });
    });

    this.sockets.subscribe("invalidate", () => {
      this.$router.push({
        name: "beReady",
        params: { auto: "true" },
      });
    });
  }

  /**
   * Submit the player's answer
   * If the player didn't response in time or didn't select an answer
   * Send 'X'
   */
  giveAnswer() {
    this.$socket.emit("user-answer", {
      answer: this.selectedAnswer ? this.selectedAnswer : "X",
    });
    this.hasAnswered = true;
    // Kill the timer
    clearInterval(this.intervalId);
  }

  /**
   * Set player's answer
   * @param answer The user's selected answer
   */
  setAnswer(answer: string) {
    this.selectedAnswer = answer;
  }
}
</script>
