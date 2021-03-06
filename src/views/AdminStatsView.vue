<template>
  <div class="flex justify-center p-4 flex-col h-screen">
    <p class="text-center text-5xl py-8 text-white uppercase">Stats</p>
    <div
      class="border-white rounded-xl flex sm:flex-row flex-col gap-4 h-full w-full items-center"
    >
      <div class="w-3/4 sm:w-1/2">
        <p class="text-center text-xl text-white font-bold tracking-wider">
          Joueurs en lice: {{ playersStillAlive() }}
        </p>
        <apexchart type="bar" :options="options" :series="alive"></apexchart>
      </div>
      <div class="w-3/4 sm:w-1/2">
        <p class="text-center text-xl text-white font-bold tracking-wider">
          Joueurs spectateurs: {{ deadPlayers() }}
        </p>
        <apexchart type="bar" :options="options" :series="dead"></apexchart>
      </div>
    </div>
    <div
      class="grid grid-cols-2 justify-center mx-auto w-2/3 gap-4 py-4 h-full"
      :class="
        playersStillAlive() + deadPlayers() === totalPlayers
          ? 'block'
          : 'hidden'
      "
    >
      <button
        class="px-4 py-2 mb-2 bg-[#E40495] border-[#5E17EB] border-2 rounded-3xl fancy-shadow"
        :class="deadPlayers() !== totalPlayers ? 'block' : 'hidden'"
        @click="showResultsToPlayers()"
      >
        <span class="uppercase md:text-2xl text-sm text-white"
          >Montrer résultats</span
        >
      </button>
      <button
        class="px-4 py-2 mb-2 bg-[#E40495] border-[#5E17EB] border-2 rounded-3xl fancy-shadow"
        :class="deadPlayers() !== totalPlayers ? 'block' : 'hidden'"
        @click="goNextQuestion()"
      >
        <span class="uppercase md:text-2xl text-sm text-white">Continuer</span>
      </button>

      <button
        class="px-4 py-2 mb-2 bg-[#E40495] border-[#5E17EB] border-2 rounded-3xl fancy-shadow"
        @click="invalidate()"
      >
        <span class="uppercase md:text-2xl text-sm text-white">Invalider</span>
      </button>

      <button
        class="px-4 py-2 mb-2 bg-[#E40495] border-[#5E17EB] border-2 rounded-3xl fancy-shadow"
        @click="endGame()"
      >
        <span class="uppercase md:text-2xl text-sm text-white">Fin Partie</span>
      </button>
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  components: {},
})
export default class AdminStatsView extends Vue {
  chartTitle1 = "Answers among the remaining players";
  chartTitle2 = "Answers among the eliminated players";

  options = {
    bar: {
      horizontal: true,
    },
    chart: {
      id: "vuechart-example",
      toolbar: {
        show: false,
      },
    },
    grid: {
      show: false,
    },
    legend: {
      show: false,
    },
    plotOptions: {
      bar: {
        borderRadius: 4,
        horizontal: true,
      },
    },
    xaxis: {
      categories: ["A", "B", "C", "D", "X"],
      lines: {
        show: false,
      },
      labels: {
        show: false,
      },
      axisBorder: {
        show: false,
      },
    },
    yaxis: {
      labels: {
        style: ["#000"],
      },
      lines: {
        show: false,
      },
    },
  };
  alive = [
    {
      name: this.chartTitle1,
      data: [],
    },
  ];
  dead = [
    {
      name: this.chartTitle2,
      data: [],
    },
  ];
  totalPlayers = Number.MAX_VALUE;

  mounted() {
    this.sockets.subscribe("update-answers", (data) => {
      this.alive = [
        {
          name: this.chartTitle1,
          data: data.alive,
        },
      ];

      this.dead = [
        {
          name: this.chartTitle2,
          data: data.dead,
        },
      ];

      this.totalPlayers = data.players;
    });
  }

  /**
   * Count the number of player still alive
   */
  playersStillAlive() {
    return this.alive[0].data.reduce((a, b) => a + b, 0);
  }

  /**
   * Count the number of dead player
   */
  deadPlayers() {
    return this.dead[0].data.reduce((a, b) => a + b, 0);
  }

  showResultsToPlayers() {
    this.$socket.emit("question-stats");
  }

  /**
   * Ping the server and set up the next question
   */
  goNextQuestion() {
    this.$socket.emit("next-question");
    this.$router.push({
      name: "admin-question-settings",
      params: { auto: "true" },
    });
  }

  /**
   * Ping the server, invalidate the answer ans go he ne
   *
   */
  invalidate() {
    // TODO: Finish the invalidate function
    this.$socket.emit("invalidate");

    this.sockets.subscribe("invalidate", () => {
      this.$router.push({
        name: "admin-question-settings",
        params: { auto: "true" },
      });
    });
  }

  /**
   * Ping the server and show the leaderboard
   */
  endGame() {
    this.$socket.emit("show-leaderboard");
    this.$router.push({
      name: "leaderboard",
      params: { auto: "true" },
    });
  }
}
</script>
