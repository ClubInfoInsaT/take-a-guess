<template>
  <div class="flex justify-center p-4 flex-col h-screen">
    <hearts
      :left="heartsLeft"
      :total="hearts"
      v-if="hearts !== -1 && heartsLeft !== -1"
    />
    <div class="border-white rounded-xl flex flex-col">
      <div>
        <p class="text-center text-xl text-white">
          Joueurs en lice: {{ playersStillAlive() }}
        </p>
        <apexchart type="bar" :options="options" :series="alive"></apexchart>
      </div>
      <div>
        <p class="text-center text-xl text-white">
          Joueurs spectateurs: {{ deadPlayers() }}
        </p>
        <apexchart type="bar" :options="options" :series="dead"></apexchart>
      </div>
    </div>
    <div class="flex flex-col justify-center items-center mx-auto w-2/3 pt-4">
      <h3 class="uppercase text-xl text-white text-center">
        {{
          isCorrect
            ? "Bonne réponse !!"
            : "Mauvaise réponse... La réponse était la " + `'${rightAnswer}'`
        }}
      </h3>
    </div>
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
export default class PlayerStatsView extends Vue {
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
  hearts = -1;
  heartsLeft = -1;
  isCorrect: boolean | null = null;
  rightAnswer = "";

  mounted() {
    this.isCorrect = this.$route.params.isCorrect === "true"; // Parse to bool using comparaison
    this.rightAnswer = this.$route.params.rightAnswer;
    this.alive = [
      {
        name: this.chartTitle1,
        data: JSON.parse(JSON.stringify(this.$route.params.alive)),
      },
    ];
    this.dead = [
      {
        name: this.chartTitle2,
        data: JSON.parse(JSON.stringify(this.$route.params.dead)),
      },
    ];
    console.log(this.alive, this.dead);

    this.$socket.emit("get-player-info");
    this.sockets.subscribe("get-player-info", (data) => {
      this.hearts = data.hearts;
      this.heartsLeft = data.left;
      this.isCorrect = data.isCorrect;
      this.rightAnswer = data.answer;
    });

    this.sockets.subscribe("next-question", () => {
      this.$router.push({ name: "beReady" });
    });

    this.sockets.subscribe("invalidate", () => {
      this.$router.push({ name: "beReady" });
    });

    this.sockets.subscribe("show-leaderboard", () => {
      this.$router.push({ name: "leaderboard" });
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
}
</script>
